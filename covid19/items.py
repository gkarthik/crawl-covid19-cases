# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from functools import reduce
from datetime import datetime as dt

class CasesCategory(scrapy.Item):
    positive = scrapy.Field(serialier = int)
    presumedPositive = scrapy.Field(serializer = int)
    negative = scrapy.Field(serialzer = int)
    pending = scrapy.Field(serializer = int)
    pui = scrapy.Field(seqializer = int)
    name = scrapy.Field()

class TestingStats(scrapy.Item):
    date = scrapy.Field()
    Local = scrapy.Field(serializer = CasesCategory)
    FederalQuarantine = scrapy.Field(serializer = CasesCategory)
    Repatriated = scrapy.Field(serializer = CasesCategory)
    NonLocal = scrapy.Field(serializer = CasesCategory)
    Combined = scrapy.Field(serializer = CasesCategory)

    def getTotal(self, key = "positive"):
        categories = sorted([i for i in self.keys() if i!= "date"])
        return sum([int(self[i][key]) for i in categories if key in self[i].keys() and self[i][key] != "NA"])

    def getCategoryTotal(self, key):
        case_categories = [i for i in self[key].keys() if i != "name"]
        return sum([int(self[key][i]) for i in case_categories if self[key][i] != "NA"])

    def toAsciiTable(self):
        # Get case categories for which data exists
        categories = sorted([i for i in self.keys() if i!= "date"])
        # Get all non null keys from lib import funs CasesCategory
        case_categories = [list(self[i].keys()) for i in categories]
        case_categories = reduce(lambda x,y: x+y,case_categories)
        case_categories = sorted(list(set([i for i in case_categories if i != "name"])))
        row_format = "|{:^30}" * (len(categories) + 1) + "|\n"
        rows = []
        rows.append([""])
        rows[0].extend([self[i]["name"] for i in categories])
        rows.extend([[i.capitalize()] + [self[j][i] if j in self.keys() and i in self[j].keys() else "NA" for j in categories] for i in case_categories])
        rows.append(["Total"] + [self.getCategoryTotal(j) for j in categories])
        row_str = "Last updated: {}".format(dt.strftime(dt.strptime(self["date"], "%Y-%m-%d %H:%M %p"), "%Y-%m-%d"))
        row_str += "\n```\n"
        for i in rows:
            print(i)
            row_str += row_format.format(*i)
        row_str += "```\n"
        row_str += "Total cases: {}".format(sum([self.getCategoryTotal(j) for j in categories]))
        return row_str
