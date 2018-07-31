import scrapy

#to run from command line, use
#>>scrapy crawl quotes


#and to run and export use this
#scrapy crawl quotes -o quotes.json
#if you run it twice, it appends and will break the json file

class QuotesSpider(scrapy.Spider):
    name = "quotes"#this is the name that appears above when running
    #each of these urls will be interated
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    #the default callback
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text' : quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
                }

            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


'''
#An example of parsing in different directions depending
#on what you are looking for

class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

'''
