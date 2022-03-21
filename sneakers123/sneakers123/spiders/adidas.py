from scrapy import Request, Spider
from pathlib import Path
from urllib.parse import urljoin
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sneakers123.items import Sneakers123Item
from scrapy.utils.project import get_project_settings

class AdidasSpider(Spider):
    name = 'adidas'
    settings = get_project_settings()
    version = settings.get("VERSION")
    allowed_domains = ['sneakers123.com']
    start_urls = ['https://sneakers123.com/en/sneaker/adidas/']
    BASE_URL = 'https://sneakers123.com/en/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(options=chrome_options)
    
    def start_requests(self):
        for url in self.start_urls:
            self.browser.get(url)
            sleep(3)
            pace = [i for i in range(875, 4375, 875)]
            for step in pace:
                self.browser.execute_script(f"window.scrollTo(0, {step})")
                sleep(3)
            product_release_imgs = self.browser.find_elements(By.XPATH, "//div[@class='product-photo']/img")
            product_details_links = self.browser.find_elements(By.XPATH, "//section[contains(@class, 'card-container sneaker-thumbnail')]/a")
            for link, img_reference in zip(product_details_links, product_release_imgs):
                link = link.get_attribute("href")
                img_reference = img_reference.get_attribute("src")
                if img_reference in ['https://sneakers123.com/sneakers123-thumb.jpg', 'https://sneakers123.com/_nuxt/img/ac3b878.jpg']:
                    img_reference = ""
                url = urljoin(self.BASE_URL, link)
                yield Request(url=url, method="GET", callback=self.parse, cb_kwargs={'image_reference' : img_reference})
            element_total_num_pages = self.browser.find_element(By.XPATH, "//a[@aria-label='Go to last page']")
            total_num_pages = int(element_total_num_pages.get_attribute("href").split("/")[-1])
            for page in [i for i in range(2, total_num_pages+1,1)]:
                url = f"https://sneakers123.com/en/sneaker/adidas/page/{page}"
                self.browser.get(url)
                sleep(3)
                pace = [i for i in range(875, 4375, 875)]
                for step in pace:
                    self.browser.execute_script(f"window.scrollTo(0, {step})")
                    sleep(3)
                product_release_imgs = self.browser.find_elements(By.XPATH, "//div[@class='product-photo']/img")
                product_details_links = self.browser.find_elements(By.XPATH, "//section[contains(@class, 'card-container sneaker-thumbnail')]/a")
                for link, img_reference in zip(product_details_links, product_release_imgs):
                    link = link.get_attribute("href")
                    img_reference = img_reference.get_attribute("src")
                    if img_reference in ['https://sneakers123.com/sneakers123-thumb.jpg', 'https://sneakers123.com/_nuxt/img/ac3b878.jpg']:
                        img_reference = ""
                    url = urljoin(self.BASE_URL, link)
                    yield Request(url=url, method="GET", callback=self.parse, cb_kwargs={'image_reference' : img_reference})


    def parse(self, response, image_reference):
        brand_division = ""
        image_urls = response.xpath("//div[@id='scrollBlock1']//img/@src").getall()
        image_urls, image_reference = self.process_image_thumbs(image_urls, image_reference=image_reference)
        if len(image_urls) == 0:
            image_reference = ""
        product_name = response.xpath("//h1[@class='product-name']/text()").get()
        brand = response.xpath("//td[contains(text(), 'Brand')]/..//td[2]/a/text()").get()
        model =  response.xpath("//td[contains(text(), 'Model')]/..//td[2]/a/text()").get()
        sku = response.xpath("//td[contains(text(), 'Style Code')]/..//td[2]/text()").get()
        gender = response.xpath("//td[contains(text(), 'Gender')]/..//td[2]//span/a/text()").getall()
        color = response.xpath("//td[contains(text(), 'Color')]/..//td[2]//span/a/text()").getall()
        date_added = response.xpath("//td[contains(text(), 'Date added')]/..//td[2]/text()").get()
        breadcrumbs = response.xpath("//ul[@class='breadcrumbs container']//li/a/text()").getall()
        if breadcrumbs:
            brand_division = breadcrumbs[-2]
        image_uris = []
        if len(image_urls) > 0:
            image_uris = [f"{self.settings.get('IMAGES_STORE')}{sku}_{filename.split('/')[-1]}" for filename in image_urls]
        item = Sneakers123Item(**{
            'image_urls' : image_urls,
            'image_uris' : image_uris,
            'image_reference' :  image_reference,
            'brand' : brand,
            'brand_division' : brand_division, 
            'product_name' : product_name,
            'model' : model,
            'sku' : sku,
            'gender' : gender,
            'color' : color,
            'date_added' : date_added, 
            'breadcrumbs' : breadcrumbs,
            'url' : response.url,
            'spider' : self.name,
            'spider_version' : self.version
        })
        yield item
    
    def process_image_thumbs(self, images, image_reference):
        image_urls = []
        for thumb in images:
            raw = thumb.split("/")
            file_type = Path(raw[-1]).suffix
            filename = raw[-1].split("-thumb")[-2]
            src = f"https://{raw[2]}/{raw[3]}/{raw[4]}/{filename}{file_type}"
            image_urls.append(src)
        if image_reference != "":
            thumb_reference = image_reference.split("/")
            file_type = Path(thumb_reference[-1]).suffix
            filename = thumb_reference[-1].split("-thumb")[-2]
            try:
                image_reference = f"https://{thumb_reference[2]}/{thumb_reference[3]}/{thumb_reference[4]}/{filename}{file_type}"
            except IndexError:
                image_reference = ""
        return image_urls, image_reference
