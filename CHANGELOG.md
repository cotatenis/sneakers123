# Change Log
Arquivo para documentação das mudanças realizadas ao longo do projeto. O formato desse arquivo é baseado no [Keep a Changelog](http://keepachangelog.com/)
e o presente projeto adota o [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2021-11-17
- [COT-401](https://ecoanalytics.atlassian.net/browse/COT-401)
### Adicionado
- Sobrescrito a função `image_downloaded` do objeto `ImagesPipeline` para garantir a persistência de apenas imagens que ainda não estão salvas no storage.
