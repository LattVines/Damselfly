import scrapy

#to run from command line, use
#>>scrapy crawl spammers


#and to run and export use this
#scrapy crawl spammers -o spammers.json
#if you run it twice, it appends and will break the json file

class SpammerSpider(scrapy.Spider):
    name = "spammers"#this is the name that appears above when running
    #each of these urls will be interated
    start_urls = [
        'https://itch.io/search?q=seo', #an example of a search that has a spam account
        'https://itch.io/search?q=tijuana'
    ]


    #the default callback
    def parse(self, response):
        discovered_profiles = []
        for creator in response.css('div.user_name'):
            discovered_profiles.append(creator.css("a::attr(href)").extract())

        for profile in discovered_profiles:
            next_page = profile[0]
            if next_page is not None:
                yield response.follow(next_page, self.parse_user_profile)


    def parse_user_profile(self, response):
        yield {'profile content': response.css('div.inner_column p').extract()}

        #yield {'profile content': extract_with_css('inner_column::text')}


'''
#attempting to rewrite to parse into user accounts detected
    #the default callback
    def parse(self, response):
        for creator in response.css('div.user_name'):
            yield {
                'user_url' : creator.css("a::attr(href)").extract()
                }

            #this currently isn't going to find the next page
            #this was an example. I am going to need
            #to find a way to generate the pages or something.
            #but technically, this urls above are going to be what I go into
            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
'''



'''
attempt one at parsing deeper

    #the default callback
    def parse(self, response):
        for href in response.css('div.user_name + a::attr(href)'):
            print("parse " + str(href))
            yield {"user_href" : href }
            #yield response.follow(href, self.parse_user_page)


    def parse_user_profile(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        print("parse_user_profile " + str(href))
        yield {
            'account page text': extract_with_css('user_profile::text'),
        }
'''




        

