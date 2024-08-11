import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for pep in response.css(
            'section[id^="numerical-index"] tbody a::attr("href")'
        ).getall():
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = re.match(
            r'PEP (\d+)\W+(.+)',
            response.css('section[id^="pep-content"] h1::text').get(),
        ).groups()

        yield PepParseItem(
            number=number,
            name=name,
            status=response.css('abbr::text').get()
        )
