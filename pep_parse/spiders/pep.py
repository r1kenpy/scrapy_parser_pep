import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse(self, response):
        all_pep = response.css(
            'section[id^="numerical-index"] tbody a::attr("href")'
        ).getall()

        for pep in all_pep:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = re.match(
            r'PEP (\d+)\W+(.+)',
            response.css('section[id^="pep-content"] h1::text').get(),
        ).groups()

        yield PepParseItem(
            {
                'number': number,
                'name': name,
                'status': response.css('abbr::text').get(),
            }
        )
