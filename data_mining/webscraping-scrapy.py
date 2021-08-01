import scrapy

class BlogSpider(scrapy.Spider):
    name = 'bikespider'
    start_urls = ['https://bazar.bg/obiavi/gradski-velosipedi/varna?condition=2']

    def parse(self, response, kwargs):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)
