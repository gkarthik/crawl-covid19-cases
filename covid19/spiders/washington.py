import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging
import requests
import json

class WashingtonSpider( scrapy.Spider ):
    name = "washington"
    allowed_domains = ['https://www.snohd.org']
    names = ["Snohomish County"]
    case_categories = ["positive", "presumedPositive", "probable", "negative", "pending"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests(self):
        yield scrapy.Request( "https://www.snohd.org/484/Novel-Coronavirus-2019", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        date = response.xpath( '//*[@id="t38905a33-579e-4a6e-9cdc-f6f62d9440c6c2"]/text()' ).get()
        date = date.split( ": " )[1]
        date = date.replace( ".", "" )
        date = date.upper()
        date = dt.strptime( date, "%I:%M %p %m/%d/%y" )

        case_table = response.xpath( '//*[@id="tableWidget38905a33-579e-4a6e-9cdc-f6f62d9440c6"]/div/table/tbody' )
        for i, row in enumerate( case_table.xpath( 'tr' ) ):
            value = row.xpath( 'td[2]/text()' ).get()
            item_dict[self.case_categories[i]] = int( value )

        # Snohomish County seperates presumed positive cases from probably cases based on source of the initial positive
        # test. Presumed positive cases have a positive test from a state lab, and probable cases have a positive test
        # from UW. Confirmed are only those which have been confirmed by CDC.

        item_dict["presumedPositive"] += item_dict.pop( "probable" )

        item["date"] = date.strftime( "%Y-%m-%d %I:%M %p" )
        item["Local"] = item_dict

        print( item.toAsciiTable() )
        return item