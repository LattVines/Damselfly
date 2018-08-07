import scrapy

#to run from command line, use
#>>scrapy crawl spammers


#and to run and export use this
#scrapy crawl spammers -o spammers.json
#if you run it twice, it appends and will break the json file

class SpammerSpider(scrapy.Spider):
    name = "spammers"#this is the name that appears above when running
    #each of these urls will be interated
    start_urls = []

    def read_city_names(self):
        f = open('SearchTerms.csv', 'r')
        #creating a big list of query URLs for itch.io
        #based on city names read from the list.
        #why? Because I found that a lot of spam accounts sit on searches for city names.
        for line in f:
            self.start_urls.append('https://itch.io/search?q=' + line.strip())
        f.close()
    
    def __init__(self):
         self.read_city_names();
        


    
    #the default callback
    def parse(self, response):
        discovered_profiles = []
        for creator in response.css('div.user_name'):
            discovered_profiles.append(creator.css("a::attr(href)").extract())

        for profile in discovered_profiles:
            next_page = profile[0]#a list, but it's the first element
            if next_page is not None:
                yield response.follow(next_page, self.scrape_user_profile)


    def scrape_user_profile(self, response):
        profile_content = response.css('div.user_profile.formatted').extract()
        yield {'profile url' : str(response.url), 'profile content' : profile_content }

       


