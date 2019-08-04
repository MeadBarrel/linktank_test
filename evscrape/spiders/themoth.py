from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import *

from ..items import EvscrapeItem
from datetime import datetime


def parse_date(date_string):
    current_date = datetime.today()
    date = datetime.strptime(date_string, '%B %d %I:%M%p')
    return date.replace(year=current_date.year + int(date.month < current_date.month))


class Loader(ItemLoader):
    default_output_processor = TakeFirst()


class TheMothSpider(CrawlSpider):
    name = 'themoth'

    start_urls = ['https://themoth.org/events/results?eventLocations=65&typesOfEvents=&eventDate=']

    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="event-list"]/div[@class="moth-event"]/div[@class="event-details"]/div[@class="event-content"]/h4/a'),
            callback='parse_event',follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="paginator"]/div[@class="right"]/a'),
            follow=True
        )
    ]

    def parse_event(self, response):
        loader = Loader(EvscrapeItem(), response)

        loader.add_xpath('Title', 'string(//h2)')
        loader.add_xpath('Description', '//div[@class="event-description"]')

        time_from_xpath = (
            'concat(normalize-space(//span[@class="month"]/text()), " ", '
            'normalize-space(//span[@class="numeric-day"]/text()), " ", '
            'normalize-space(//p[@class="event-time"]/strong[1]))')
        loader.add_xpath('DateFrom', time_from_xpath, Compose(TakeFirst(), parse_date))
        loader.add_xpath('StartTime', time_from_xpath, Compose(TakeFirst(), parse_date))
        loader.add_value('EventWebsite', response.url)
        loader.add_xpath('Location', 'string(//div[@class="venue-detail"]/h3)', 
            Compose(TakeFirst(), lambda s: s.lstrip('Venue: ')))
        loader.add_xpath('Address', 'string(//div[@class="venue-detail"]/p[1])')
        loader.add_xpath('TicketURL', '//a[@class="btn accent" and text()="Buy Tickets"]/@href')

        # hard-coded values
        loader.add_value('OrganizationName', 'The Moth')
        loader.add_value('City', 'New York')
        loader.add_value('State', 'NY')
        loader.add_value('Zip', '10004')
        loader.add_value('ID', 7072)
        loader.add_value('contactName', 'David Mutton')
        loader.add_value('contactEmail', 'david@themoth.org')

        return loader.load_item()
