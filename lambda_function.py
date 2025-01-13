from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import gradescrape.gradescrape.spiders.gradespider as gradespider
import sys

def lambda_handler(event, context):
    '''
    Function AWS lambda will run

    Runs gradespider
    '''
    gradespider.GradespiderSpider.custom_settings={'DOWNLOAD_DELAY':3}
    process = CrawlerProcess(get_project_settings())
    process.crawl(gradespider.GradespiderSpider)
    process.start()
    sys.exit(0) #Only way I could find inorder to run on EC2 lambda: https://stackoverflow.com/questions/42388541/scrapy-throws-error-reactornotrestartable-when-runnning-on-aws-lambda