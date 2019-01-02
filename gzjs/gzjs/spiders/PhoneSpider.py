import scrapy
import logging
import re
import json
from gzjs.items import GzjsItem


class phoneSpider(scrapy.Spider):  #需要继承scrapy.Spider类

    name = "phoneSpider"  # 定义蜘蛛名
    custom_settings = {
        'ITEM_PIPELINES': {
            'gzjs.pipelines.GzjsPipeline': 300
        }
    }
    # 简化方法
    start_urls = []
    for i in range(1,92):
        start_urls.append('http://gzjs.bazhuayu.com/?pageIndex=' + str(i))
    
    # start_urls = ['http://gzjs.bazhuayu.com/?pageIndex=1']
    
    ''' 自定义回调函数
    def start_requests(self): # 由此方法通过下面链接爬取页面
    
        # 定义爬取的链接
        urls = [
            'http://gzjs.bazhuayu.com/?pageIndex=1',
            'http://gzjs.bazhuayu.com/?pageIndex=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) 
    '''

    # response网页响应内容
    def parse(self, response):
        '''
        filename = 'phone-%s.html' % response.url.split("=")[-1]   #截取的分割符为=，[-1]从数组后面读取
        with open(filename, 'wb') as f:        
            f.write(response.body)             
        self.logger.info('保存文件: %s', filename)      
        '''
        # css()制定xpath的规则,页面样式用css(),跳转手机详细页面
        for link in response.css('li.item a::attr(href)').extract():
            # link的响应内容回调 parse_phone,网址用follow()
            yield response.follow(link, callback=self.parse_phone)

    def parse_phone(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        item = GzjsItem()

        pattern = '\w+'
        original = extract_with_css('div.item + a::text')
        # 有些商品没有品牌名
        if original is None:
            original = extract_with_css('div.desc::text').strip('商品名称：')

        original = re.search(pattern, original).group().upper()
        # 提取品牌名，Appleiphone
        pattern = 'APPLE|360|SONY|中兴'
        if(re.search(pattern, original) != None):
            original = re.search(pattern, original).group()
        # 特殊归类
        if(original == 'HUAWEI'):
            original = '华为'
        if(original == '苹果'):
            original = 'APPLE'

        # 一旦item[]被赋值，则直接调用pipelines里的处理代码，所以只能赋值一次
        item['brand'] = original 

        
        item['name'] = extract_with_css('div.desc::text').strip('商品名称：')
        # match只从字符串开头匹配
        item['price'] = extract_with_css('span.number::text')
        item['pid'] = extract_with_css('div.desc + div::text').strip('商品编号：')

        original = extract_with_css('.tab-item + div::text').strip('评价')

        if (re.search('万', original) != None):
            extra = 10000
        else:
            extra = 1
        pattern = '\d+\.\d|\d+'
        # search全串搜索
        item['salesVolume'] = float(re.search(pattern,
                                              original).group()) * extra
        '''
        logging.info("brand: %s", item['brand'])
        logging.info('PhoneLink: %s', response)
        logging.info("ID: %s", item['pid'])
        logging.info("name: %s", item['name'])
        logging.info("price: %s", item['price'])
        logging.info("salesVolume: %s", item['salesVolume'])
        '''

        yield item

'''
        yield scrapy.Request(
            url="http://gzjs.bazhuayu.com/comment/" + item['pid'],
            method="POST",
            callback=self.parse_evaluate)

    def parse_evaluate(self, response):
        rs =  json.loads(response.body)
        logging.info("evaluates:",rs)
        pass
'''