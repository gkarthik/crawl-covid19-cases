import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class CanadaOntarioSpider( scrapy.Spider ):
    name = "canadaontario"
    allowed_domains = ["https://www.publichealthontario.ca"]
    obj = ["Ontario"]
    case_categories = ["negative", "pending", "positive"]
    names = ["Ontario, CAN"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.publichealthontario.ca/en/diseases-and-conditions/infectious-diseases/respiratory-diseases/novel-coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        date = response.xpath( '//*[@id="pho-main-content-grid"]/div[5]/div/div/p[4]/text()' ).get()
        date = date.replace( ".", "" )
        date = dt.strptime( date, "%B %d, %Y at %H:%M %p ET")

        case_table = response.xpath( '//*[@id="pho-main-content-grid"]/div[5]/div/div/table/tbody' )
        for i, row in enumerate( case_table.xpath( 'tr' )[1 :-2] ) :
            value = row.xpath( "td[2]/text()" ).get()
            item_dict[self.case_categories[i]] = int( value )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = item_dict

        print( item.toAsciiTable() )
        return item
