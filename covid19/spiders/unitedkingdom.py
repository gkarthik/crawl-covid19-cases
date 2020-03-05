import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class UKSpider( scrapy.Spider ):
    name = "unitedkingdomnational"
    allowed_domains = ["https://www.gov.uk/"]
    obj = ["UnitedKingdom"]
    case_categories = ["total", "negative", "positive"]
    names = ["United Kingdom"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        case_paragraph = response.xpath( '//*[@id="contents"]/div[2]/div/p[1]/text()' ).get()
        date = case_paragraph.split( "," )[0]
        date = dt.strptime( date, "As of %I%p on %d %B %Y")

        case_paragraph = ",".join( case_paragraph.split( "," )[1:] )
        case_paragraph = case_paragraph.replace( ",", "" )

        values = [i for i in case_paragraph.split( " " ) if i.isnumeric()]
        for i, value in enumerate( values ):
            item_dict[self.case_categories[i]] = value

        del item_dict["total"]

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = item_dict

        print( item.toAsciiTable() )
        return item
