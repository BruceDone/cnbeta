__author__ = 'Bruce'
# coding=utf-8
from scrapy.spiders import Spider
import re
from cnbeta.items import CnbetaItem
from scrapy.http.request import Request
# please pay attention to the encoding of info,otherwise raise error
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class cnbeta_tag(Spider):
    name = 'cnbeta_tag'

    def __init__(self, url='', *args, **kwargs):
        self.allowed_domains = ['cnbeta.com']
        self.start_urls = [
            'http://www.cnbeta.com/topics.htm?letter=%s' % p for p in 'abcdefghijklmnopqrstuvwxyz'
            # 'http://www.cnbeta.com/topics.htm?letter=a'
            ]
        # call the father base function
        self.url = url
        super(cnbeta_tag, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        use for init the first tag information and id,title
        """
        a_list = response.xpath('//div[@class="content_body topic_list fl"]/div[2]//dd//a')
        if not a_list:
            self.logger.info(msg='can not find any a list tag information')
            return
        for a in a_list:
            item = CnbetaItem()
            url = ''.join(a.xpath('@href').extract())
            item['url'] = url
            item['desc'] = ''.join(a.xpath('text()').extract())
            ma = re.match('.*?(\d+).*?', url)
            if ma:
                item['uid'] = ma.group(1)
            else:
                item['uid'] = '-1'
            yield item
