import scrapy

from scrapy.exceptions import CloseSpider


BASE_URLS = [
    'https://www.xsport.ua'
]
PAGES_COUNT = 20


class Scraper(scrapy.Spider):
    name = 'xsport'
    start_urls = BASE_URLS
    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1.pipelines.XsportPipeline': 1,
        }
    }

    XPATHS = {
        'img': '//img/@src',
        'text': '//*[not(self::script)]/text()',
        'link': '//a/@href'
    }

    def parse(self, response):
        counter = 0
        text = self.extract_text(response)
        images = self.extract_images(response)
        links = self.extract_links(response)

        yield {
            'text': text,
            'images': images,
            'url': response.url
        }
        for link in links:
            print(link)
            yield response.follow(link, callback=self.parse)
            if counter == PAGES_COUNT:
                raise CloseSpider('Finished successfuly.')
            else:
                counter += 1

    def extract_links(self, response):
        result = []
        for link in response.xpath(self.XPATHS['link']):
            clear_link = link.extract().strip()
            if clear_link:
                if clear_link.startswith('/') or BASE_URLS[0] in clear_link:
                    result.append(clear_link)
        return result

    def extract_text(self, response):
        result = []
        for text in response.xpath(self.XPATHS["text"]):
            clear_text = text.extract().strip()
            if clear_text:
                result.append(clear_text)

        return result

    def extract_images(self, response):
        result = []

        for image_url in response.xpath(self.XPATHS['img']):
            clear_image_url = image_url.extract().strip()
            if clear_image_url:
                result.append(clear_image_url)
        return result
