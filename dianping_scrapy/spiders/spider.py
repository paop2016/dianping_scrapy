from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider,RedisCrawlSpider
from dianping_scrapy import items
import json,copy
import re
class ShopIDSpider(Spider):
    name = 'shop_id_spider'
    # redis_key = 'dianping:start_urls'
    start_urls=[
        # 北京地区所有的咖啡厅地址
        'https://www.dianping.com/search/category/2/30/g132'

        # 爬取代理ip地址
        # 'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20174196535JKCgA9/6eeefc68aaf911e6802371d9ec16a600?returnType=2',
        # 'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20174195726EIkWH6/81bc8438000c11e7942200163e1a31c0?returnType=2',
        # 'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20174192691wTPiKN/f7b7a819f78511e6942200163e1a31c0?returnType=2',
        # 'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20174194991FjeR70/f77e2395108111e79ff07cd30abda612?returnType=2'
    ]

    url_head='http://www.dianping.com'
    # 测试当前ip，User-Agent
    def parse1(self,response):
        print(response.body.decode('utf-8'))
        yield Request(url='http://ip.filefab.com/index.php', callback=self.parse, dont_filter=True)
    # 爬取代理ip
    def parse2(self, response):
        dic=json.loads(response.body.decode('utf-8'))['RESULT']
        ip = 'http://' + dic['wanIp'] + ':' + dic['proxyport']
        print(ip)


    def parse(self, response):
        selector=Selector(response)
        urls=selector.xpath("//li/div[@class='txt']/div[@class='tit']/a[@data-hippo-type='shop']/@href").extract()
        for url in urls:
            item=items.ShopItem()
            id=url.split('/')[-1]
            item['id']=id
            yield Request(url=self.url_head+url,callback=self.parseDetail,dont_filter=True,meta={'item':item})

        nextUrl=selector.xpath("//a[@class='next']/@href").extract()
        if nextUrl:
            nextUrl=nextUrl[0]
            yield Request(url=self.url_head+nextUrl, callback=self.parse,dont_filter=True)

    def parseDetail(self,response):
        item=response.meta['item']
        selector=Selector(response)
        try:
            name=selector.xpath("//h1[@class='shop-name']/text()").extract()[0].strip()
        except Exception:
            name=selector.xpath("//h1[@class='shop-title']/text()").extract()[0].strip()
            print(str(selector.xpath("//h1[@class='shop-name']/text()").extract())+'>>>>>>'+item['id'])
        item['name']=name
        yield Request(url='http://www.dianping.com/shop/'+item['id']+'/review_more',callback=self.parseComment,dont_filter=True,meta={'item':item})

    def parseComment(self,response):
        item = response.meta['item']
        selector = Selector(response)
        comments=selector.xpath("//div[@class='comment-list']//li//div[@class='J_brief-cont']")
        for comment in comments:
            comment=comment.xpath('text()').extract()[0].strip()
            # 如果有'便宜'关键字在其中，则yield
            if '便宜' in comment:
                item['comments']=item.get('comments','')+'||'+comment
        nextUrl=selector.xpath("//a[@class='NextPage']/@href").extract()
        if nextUrl:
            nextUrl=nextUrl[0]
            yield Request(url='http://www.dianping.com/shop/'+item['id']+'/review_more'+nextUrl,callback=self.parseComment,dont_filter=True,meta={'item':item})
        else:
            if item.get('comments',''):
                yield item