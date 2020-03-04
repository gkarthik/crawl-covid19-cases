# -*- coding: utf-8 -*-
import scrapy
from covid19.items import SanDiegoCovid19Stats
import requests
import json
import covid19.config
from covid19.config import slack_sandiego_post_url

class sandiegoSpider(scrapy.Spider):
    name = 'sandiego'
    allowed_domains = ['www.sandiegocounty.gov']
    start_urls = ['https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV.html']
    objs = ["SanDiegoCounty", "FederalQuarantine", "NonSanDiegoCounty"]
    case_categories = ["positive", "pending", "negative"]
    names = ["San Diego County", "Federal Quarantine", "Non-San Diego County Residents"]
    
    def parse(self, response):
        cases_table = response.xpath("//table/tbody")
        item = SanDiegoCovid19Stats()
        for ind, row in enumerate(cases_table[0].xpath("tr")[:-2]):
            if ind == 0:        # Updated date
                cells = row.xpath("td//text()")
                update_date_text = "".join([i.extract() for i in cells])
                date = update_date_text[update_date_text.find("Updated ") + len("Updated"):].strip()
                item["date"] = date
            elif ind >= 2:      # Case counts
                for cell_ind, cell in enumerate(row.xpath("td//text()").extract()[1:]):
                    if self.objs[cell_ind] not in item.keys():
                        item[self.objs[cell_ind]] = {
                            "name": self.names[cell_ind]
                        }
                    item[self.objs[cell_ind]][self.case_categories[ind - 2]] = cell
        res = requests.post(slack_sandiego_post_url, data = json.dumps({"text": item.toAsciiTable()}), headers = {"Content-type": "application/json"})
        self.logger.info("Reuest response: {}".format(res.text))
        return item