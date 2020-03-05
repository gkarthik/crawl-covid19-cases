import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class CanadaNationalSpider( scrapy.Spider ):
    name = "canadaonational"
    allowed_domains = ["https://www.canada.ca"]
    obj = ["CanadaNational"]
    case_categories = ["positive", "negative"]
    names = ["Canada National"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request(
            "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html",
            callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/main/div[3]/p[14]/text()' ).get()
        date = date.split( ", the" )[0].replace( u"\xa0", " " )

        date = dt.strptime( date, "As of %B %d, %Y" )
        print( date )

        total = 0

        case_table = response.xpath( '/html/body/main/div[3]/div[5]/table/tbody/tr' )
        for i, row in enumerate( case_table.xpath( 'td/text()' )[:3] ):
            if i == 2:
                total = int( row.get() )
            else:
                item_dict[self.case_categories[i]] = int( row.get() )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )

        # Commenting this out because its not clear if pending cases are listed or not.
        #item_dict["pending"] = total - ( item_dict["positive"] + item_dict["negative"] )

        item["Local"] = item_dict

        print( item.toAsciiTable() )
        return item