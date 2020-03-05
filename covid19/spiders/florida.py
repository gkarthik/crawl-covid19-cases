# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
import requests
import json
import covid19.config
from covid19.config import slack_sandiego_post_url
from datetime import datetime as dt
import re

class FloridaSpider(scrapy.Spider):
    name = 'florida'
    allowed_domains = ['www.floridahealth.gov']
    start_urls = ["http://www.floridahealth.gov/diseases-and-conditions/COVID-19/"]
    # Ajax request from http://www.floridahealth.gov/diseases-and-conditions/COVID-19/index.html

    def parse(self, response):
        div = response.xpath("//*[@class=\"split_70-30_left\"]/*[@class=\"wysiwyg_content clearfix\"]")
        text = div[1].xpath("block/div//text()").extract()
        item = TestingStats()
        date_text = div[1].xpath("block/p/sup//text()").extract_first()[6:]
        date = dt.strptime(date_text.replace("p.m.", "PM").replace("a.m.", "AM"), "%H:%M %p ET %d/%m/%Y")
        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["Local"] = {
            "name": "Florida",
            "positive": re.findall(r"^[0-9]+", text[0])[0],
            "presumedPositive": re.findall(r"^[0-9]+", text[1])[0]
        }
        item["Repatriated"] = {
            "name": "Repatriated Cases",
            "positive": re.findall(r"^[0-9]+", text[2])[0]
        }
        item["NonLocal"] = {
            "name": "Non Florida",
            "positive": re.findall(r"^[0-9]+", text[3])[0]
        }
        item["Combined"] = {
            "name": "Florida State",
            "negative": re.findall(r"^[0-9]+", text[4])[0],
            "pending": re.findall(r"^[0-9]+", text[5])[0],
            "pui": re.findall(r"^[0-9]+", text[6])[0]
        }
        print(item.toAsciiTable())
        return item

