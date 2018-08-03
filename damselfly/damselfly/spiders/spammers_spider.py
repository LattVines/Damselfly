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

    def read_city_names(self):
        f = open('Cities.csv', 'r')
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
                yield response.follow(next_page, self.parse_user_profile)


    def parse_user_profile(self, response):
        profile_content = response.css('div.user_profile.formatted').extract()
        result = self.inspect_profile_for_spam( profile_content, response.url)
        yield {'profile url' : str(response.url), 'link count': result }


    def inspect_profile_for_spam(self, profile_content, profile_url):
        #note: profile_content is a list
        url_count = 0
        for item in profile_content:
            url_count += item.count('http')
        return url_count
        


