__author__ = 'Bruce'
# coding=utf-8
from scrapy.spiders import Spider
import re
import datetime
from cnbeta.items import IndexItem
from cnbeta.settings import PAGE_LIST
from cnbeta.settings import JSON_TEMPLATE
import json
from scrapy.http.request import Request

# please pay attention to the encoding of info,otherwise raise error
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class cnbeta_index(Spider):
    name = 'cnbeta_index'

    def __init__(self, keyword='', *args, **kwargs):
        self.allowed_domains = ['cnbeta.com']
        self.start_urls = [
            JSON_TEMPLATE % p['uid'] for p in PAGE_LIST
            ]
        self.keyword = keyword
        super(cnbeta_index, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        use for init the first tag information and id,title
        """
        json_str = response.body
        if not json_str:
            self.logger.info(msg='can not find any json str please check the url')
            return
        info = re.sub('jQuery.*?[(]', '', json_str).rstrip(')')
        s = json.loads(info)['result']['list']
        if s and len(s) > 0:
            for t in s:
                try:
                    item = IndexItem()
                    for k,v in t.items():
                        item[k] = v
                    yield item
                except:
                    continue
