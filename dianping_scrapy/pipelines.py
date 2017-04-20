# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo,pymysql
class DianpingScrapyPipeline(object):
    def __init__(self):
        # db = pymongo.mongo_client.MongoClient(settings['MONGOD_HOST'], settings['MONGOD_PORT'])[settings['MONGOD_DBNAME']]
        # self.collection = db[settings['MONGOD_DOCNAME']]
        # self.collection.remove()

        self.connention=pymysql.connect(**settings['MYSQL_CONFIG'])
        self.cursor=self.connention.cursor()
        self.cursor.execute("drop table if exists comment")
        self.cursor.execute("CREATE TABLE comment (shop_id char(15) CHARACTER SET utf8 NOT NULL,shop_name char(50) CHARACTER SET utf8  NOT NULL,comments VARCHAR(15000)  CHARACTER SET utf8 NOT NULL)CHARACTER SET = utf8")
    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        shop_id=item['id']
        name=item['name']
        comments=item['comments']
        self.cursor.execute("INSERT INTO comment(shop_id,shop_name,comments) VALUES ('"+shop_id+"','"+name+"','"+comments+"')")
        self.connention.commit()
        return item