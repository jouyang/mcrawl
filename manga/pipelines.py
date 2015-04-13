# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class MangaPipeline(object):

	def process_item(self, item, spider):
		if item["author"]:
			item["author"] = item["author"][0].strip()
		if item["title"]:
			item["title"] = item["title"][0].strip()
		if item["cover"]:
			item["cover"] = item["cover"][0].strip()

		return item