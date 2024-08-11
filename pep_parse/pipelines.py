# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from collections import defaultdict
from datetime import datetime as dt

from pep_parse.settings import BASE_DIR, RESULTS_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.number_statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.number_statuses[item['status']] += 1
        return item

    def close_spider(self, spider):
        result_dir = BASE_DIR / RESULTS_DIR
        result_dir.mkdir(exist_ok=True)
        with open(
            result_dir / f'status_summary_'
            f'{dt.now().strftime("%d-%m-%Y_%H:%M:%S")}.csv',
            'w',
            encoding='utf-8',
        ) as f:
            writer = csv.writer(f, dialect=csv.excel, quoting=csv.QUOTE_NONE)
            writer.writerows(
                [('status', 'quantity'), *self.number_statuses.items()]
            )
