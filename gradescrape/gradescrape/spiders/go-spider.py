from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import gradespider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(gradespider.GradespiderSpider)
process.start()