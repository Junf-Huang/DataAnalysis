import json
import logging
import re

import jsonpath
import scrapy
from snownlp import SnowNLP
# 一定要两个
import jieba
import jieba.analyse

from gzjs.items import CommentItem


class commentSpider(scrapy.Spider):  #需要继承scrapy.Spider类

    name = "commentSpider"  # 定义蜘蛛名
    start_urls = []
    for i in range(1, 92):
        start_urls.append('http://gzjs.bazhuayu.com/?pageIndex=' + str(i))
    custom_settings = {
        'ITEM_PIPELINES': {
            'gzjs.pipelines.CommentPipeline': 300
        }
    }

    def parse(self, response):
        for link in response.css('li.item a::attr(href)').extract():
            yield response.follow(link, callback=self.parse_phone)
    
    def parse_phone(self, response):

        pid = response.css('div.desc + div::text').extract_first().strip('商品编号：')
        yield scrapy.Request(
            url="http://gzjs.bazhuayu.com/comment/" + pid,
            method="POST",
            callback=self.parse_evaluate)
        

    def parse_evaluate(self, response):

        pid = re.search('\d+',response.url).group()
        # json数据
        uncodestr =  json.loads(response.body)
        # 查找指定的节点
        content_list = jsonpath.jsonpath(uncodestr,"$..content")

        # 提取关键词
        contents = ''
        
        # 好感度统计
        pos = 0
        for i in content_list:
            contents += i
            s = SnowNLP(i)
            if(s.sentiments >= 0.55):
                pos +=1
        sentiment = str(pos/len(content_list))

        keywords = ''
        # allowPOS根据东明粗更好查找突出功能，看视频学习、听歌玩游戏等
        # 将关键词与评论匹配，字符串的匹配算法（kmp），统计各个关键词出现次数的频率，再根据重要性定下权重，
        # 乘以权重，计算综合分数，排序取优
        score = 0
        str_list = ['看视频', '学习', '听歌', '游戏']
        
        jieba.analyse.set_stop_words("stop_words.txt")
        dictword = jieba.analyse.extract_tags(contents, topK=20, allowPOS=('vn', 'v'))
        for word in dictword:
            keywords += word + ','
            # 根据特征介绍手机
            if word in str_list:
                score += 1
        score = score/len(str_list)
        if(score >= 0.5):
            print("推荐度",score)
            print("Recommend:", pid)

        
        item = CommentItem()
        item['pid'] = pid
        item['sentiment'] = sentiment
        item['keywords'] = keywords

        # scrapy函数执行是广度顺序，所以全局变量的位置得放在最深度，不然变量为空
        '''
        print("pid", item['pid'])
        print("sentiment", item['sentiment'])
        print("keywords", item['keywords'])
        '''
        yield item
        
        ''' 费时
        s = SnowNLP(contents)
        self.item['summary'] = s.summary()
        logging.info("summary: %s", s.summary())
        '''




        


        
