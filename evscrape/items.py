# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import *
import html
from w3lib.html import remove_tags
from htmllaundry import sanitize, strip_markup
from htmllaundry.cleaners import CommentCleaner


def format_date(dt):
    return dt.strftime('%m/%d/%Y')

def format_time(dt):
    return dt.strftime('%I:%M %p')

def interrupt_breaks(s):
    return html.unescape(s).replace('\xa0', ' ')

def sanitize_comment(s):
    return sanitize(s, cleaner=CommentCleaner)


class SpeakerItem(scrapy.Item):
    FirstName = scrapy.Field(output_processor=Compose(TakeFirst(), str.strip))
    LastName = scrapy.Field(output_processor=Compose(TakeFirst(), str.strip))
    JobTitle = scrapy.Field(output_processor=Compose(TakeFirst(), strip_markup, html.unescape, interrupt_breaks, str.strip))
    Affiliation = scrapy.Field(output_processor=Compose(TakeFirst(), strip_markup, html.unescape, interrupt_breaks, str.strip))
    Bio = scrapy.Field(output_processor=Compose(TakeFirst(), strip_markup, html.unescape, interrupt_breaks, str.strip))
    Photo = scrapy.Field()
    URL = scrapy.Field()
    Twitter = scrapy.Field()


class EvscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    BriefDescription = scrapy.Field(output_processor=Compose(TakeFirst(), html.unescape, interrupt_breaks))
    Description = scrapy.Field(output_processor=Compose(TakeFirst(), sanitize_comment))
    DateFrom = scrapy.Field(output_processor=Compose(TakeFirst(), format_date))
    DateTo = scrapy.Field(output_processor=Compose(TakeFirst(), format_date))
    StartTime = scrapy.Field(output_processor=Compose(TakeFirst(), format_time))
    EndTime = scrapy.Field(output_processor=Compose(TakeFirst(), format_time))
    EventWebsite = scrapy.Field()
    OrganizationName = scrapy.Field(output_processor=Compose(TakeFirst(), html.unescape))
    PhotoURL = scrapy.Field()
    Location = scrapy.Field()
    Room = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Zip = scrapy.Field()
    ID = scrapy.Field()
    Keywords = scrapy.Field(output_processor = Compose(MapCompose(str.strip), Join(', ')))
    EventType = scrapy.Field(output_processor = Join(','))
    eventPriceLow = scrapy.Field()
    eventPriceHigh = scrapy.Field()
    eventPriceMembers = scrapy.Field()
    eventPriceStudents = scrapy.Field()
    contactEmail = scrapy.Field()
    contactPhone = scrapy.Field(output_processor=Compose(TakeFirst(), str.strip))
    Speakers = scrapy.Field(output_processor = Join(','))
    contactName = scrapy.Field()
    Address = scrapy.Field()
    TicketURL = scrapy.Field()
    speakers = scrapy.Field(output_processor = MapCompose(dict))