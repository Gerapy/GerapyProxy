# -*- coding: utf-8 -*-
from scrapy import FormRequest, Spider
import logging
import json

logger = logging.getLogger(__name__)


class HttpbinSpider(Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    delay = 3
    max_page = 100
    url = f'https://httpbin.org/delay/{delay}'
    
    def start_requests(self):
        """
        send start requests for <max_page> times
        :return:
        """
        for i in range(1, self.max_page + 1):
            yield FormRequest(url=self.url, formdata={
                'page': str(i)
            }, callback=self.parse, meta={
                'page': i
            })
    
    def parse(self, response):
        """
        print origin
        :param response:
        :return:
        """
        data = json.loads(response.text)
        logger.info(f'request from %s successfully, current page %s',
                    data.get('origin'),
                    response.meta.get('page'))
