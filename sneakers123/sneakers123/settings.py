from shutil import which
BOT_NAME = 'sneakers123'
SPIDER_MODULES = ['sneakers123.spiders']
NEWSPIDER_MODULE = 'sneakers123.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
VERSION = '0-2-0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless']  # '--headless' if using chrome instead of firefox
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}
MAGIC_FIELDS = {
    "timestamp": "$isotime",
    "spider": "$spider:name",
    "url": "$response:url",
}
SPIDER_MIDDLEWARES = {
    "scrapy_magicfields.MagicFieldsMiddleware": 100,
}
#SPIDERMON
SPIDERMON_ENABLED = True

EXTENSIONS = {
    'sneakers123.extensions.SentryLogging' : -1,
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

ITEM_PIPELINES = {
    "sneakers123.pipelines.DiscordMessenger" : 100,
    "sneakers123.pipelines.Sneakers123ImagePipeline" : 200,
    "sneakers123.pipelines.GCSPipeline": 300,
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 400,
}

SPIDERMON_VALIDATION_MODELS = (
    'sneakers123.validators.Sneakers123Item',
)

SPIDERMON_SPIDER_CLOSE_MONITORS = (
'sneakers123.monitors.SpiderCloseMonitorSuite',
)

SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = False
SPIDERMON_PERIODIC_MONITORS = {
'sneakers123.monitors.PeriodicMonitorSuite': 30, # time in seconds
}
#THROTTLE
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 5

SPIDERMON_SENTRY_DSN = ""
SPIDERMON_SENTRY_PROJECT_NAME = ""
SPIDERMON_SENTRY_ENVIRONMENT_TYPE = ""

#GCP
GCS_PROJECT_ID = ""
GCP_CREDENTIALS = ""
GCP_STORAGE = ""
GCP_STORAGE_CRAWLER_STATS = ""
#FOR IMAGE UPLOAD
IMAGES_STORE = f''
IMAGES_THUMBS = {
    '400_400': (400, 400),
}

#DISCORD
DISCORD_WEBHOOK_URL = ""
DISCORD_THUMBNAIL_URL = ""
SPIDERMON_DISCORD_WEBHOOK_URL = ""
#LOG
LOG_LEVEL = "INFO"