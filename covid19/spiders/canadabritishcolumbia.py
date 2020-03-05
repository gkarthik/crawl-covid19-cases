import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class CanadaBritishColumbiaSpider( scrapy.Spider ) :

    name = "canadabritishcolumbia"
    allowed_domains = ["http://www.bccdc.ca/"]
    obj = ["BritishColumbia"]
    case_categories = ["positive", "pending", "negative"]
    names = ["British Columbia, CAN" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        confirmed_paragraph = response.xpath( '//*[@id="ctl00_PlaceHolderMain_SubPlaceholder_ctl07__ControlWrapper_RichHtmlField"]/div[1]/div[1]/ul/li[1]/text()' ).get()
        totals_paragraph = response.xpath( '//*[@id="ctl00_PlaceHolderMain_SubPlaceholder_ctl07__ControlWrapper_RichHtmlField"]/div[1]/div[1]/ul/li[2]/p/text()' ).get()
        confirmed = int( confirmed_paragraph.split( "\xa0" )[0] )
        total_tested = int( totals_paragraph.split( " " )[0].replace( ",", "" ) )
        date =  " ".join( totals_paragraph[:-2].split( " " )[8:10] )
        date = dt.strptime( date, "%B %d, %Y." )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = { "name" : self.names[0],
                          "positive" : confirmed,
                          "negative" : total_tested - confirmed }
        print( item.toAsciiTable() )
        return item