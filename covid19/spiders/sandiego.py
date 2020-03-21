# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
import requests
import json
import covid19.config
from covid19.config import slack_sandiego_post_url
from datetime import datetime as dt

class sandiegoSpider(scrapy.Spider):
    name = 'sandiego'
    allowed_domains = ['www.sandiegocounty.gov']
    start_urls = ['https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV/status.html']
    objs = ["Local", "FederalQuarantine", "NonLocal", "Total"]
    case_categories = ["0-9 years", "10-19 years", "20-29 years", "30-39 years", "40-49 years", "50-59 years", "60-69 years", "70-79 years", "80+ years", "Age unknown", "Hospitalized", "Deaths"]
    names = ["San Diego County", "Federal Quarantine", "Non-San Diego County Residents"]
    
    def parse(self, response):
        cases_table = response.xpath("//table/tbody")
        item = TestingStats()
        for ind, row in enumerate(cases_table[0].xpath("tr")[:-2]):
            if ind == 0:        # Updated date
                cells = row.xpath("td//text()")
                update_date_text = "".join([i.extract() for i in cells])
                date = update_date_text[update_date_text.find("Updated ") + len("Updated"):].strip()
                date = dt.strptime(date, "%B %d, %Y")
                item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
            elif ind in [4,5,6,7,8,9,10,11,12,13, 18, 19]:      # Case counts
                for cell_ind, cell in enumerate(row.xpath("td//text()").extract()[1:-1]):
                    cell = cell.replace(u'\xa0', u' ')
                    if cell == " ":
                        continue
                    if self.objs[cell_ind] not in item.keys():
                        item[self.objs[cell_ind]] = {
                            "name": self.names[cell_ind]
                        }
                    item[self.objs[cell_ind]][self.case_categories[ind - 2]] = cell
        res = requests.post(slack_sandiego_post_url, data = json.dumps({"text": item.toAsciiTable()}), headers = {"Content-type": "application/json"})
        self.logger.info("Reuest response: {}".format(res.text))
        return item
