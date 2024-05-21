# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class SdamgiaTaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    task_id = scrapy.Field()
    topic_id = scrapy.Field()
    task_type = scrapy.Field()
    is_based_on_text = scrapy.Field()
    exam_type = scrapy.Field()
    task_text = scrapy.Field()
    task_images = scrapy.Field()
    solution_text = scrapy.Field()
    solution_images = scrapy.Field()
    answer = scrapy.Field()
    url = scrapy.Field()
    fipi_links = scrapy.Field()
    sources_links = scrapy.Field()
    task_points = scrapy.Field()
    criteria_table = scrapy.Field()
    html_task = scrapy.Field()
