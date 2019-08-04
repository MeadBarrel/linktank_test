# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem


class SubstituteDescriptionPipeline(object):
    def process_item(self, item, spider):
        if item.get('Description') is None and item.get('BriefDescription'):
            item['Description'] = item.get('BriefDescription')
        return item


class EvscrapePipeline(object):
    def process_item(self, item, spider):
        try:
            assert item.get('Title') is not None, "Title is missing"
            assert item.get('Description') is not None, "Description is missing"
            assert item.get('DateFrom') is not None, "DateFrom is missing"
            assert item.get('StartTime') is not None, "StartTime is missing"
            assert item.get('EventWebsite') is not None, "EventWebsite is missing"
            assert item.get('ID') is not None, "ID is missing"
            assert item.get('OrganizationName') is not None, "OrganizationName is missing"
        except AssertionError as e:
            raise DropItem("Assetion failed: %s" % e)
        
        return item


class FilterSpeakersPipeline(object):
    def process_item(self, item, spider):
        if not item.get('speakers'): 
            return item

        item['speakers'] = list(
            filter(
                lambda speaker: speaker.get('FirstName') is not None,
                item['speakers']
            )
        )
    
        return item