gradespider.GradespiderSpider.custom_settings={'DOWNLOAD_DELAY':3}
runner = CrawlerRunner(get_project_settings())
d = runner.crawl(gradespider.GradespiderSpider)

# Ensure the reactor does not try to restart by waiting for the crawl to finish
d.addCallback(lambda _: reactor.stop())
d.addErrback(lambda _: reactor.stop())

# Block until the crawler is done
reactor.run()  # This will now work in AWS Lambda without causing ReactorNotRestartable
sys.exit(0)