import scrapy
from scrapy.utils.response import open_in_browser
class SeriouseatsSpider(scrapy.Spider):
    name = "seriouseats"
    start_urls = ["http://www.seriouseats.com/"]
    def parse(self, response):
        print("yes i will reach")
       
        url = 'http://www.seriouseats.com/search?q=chicken'
        yield scrapy.Request(url, callback=self.parse_search_results)
    
    def parse_search_results(self, response):
        open_in_browser(response)
        print(response)
        print("url of this page")
        print(response.url) 
        url = response.css('a.card::attr(href)').getall()
        image = response.css('img.card__image::attr(src)').getall()
        title = response.css('span.card__title>span::text').getall()
        print(image)
        print("hjcfasdhkzhkdfasdkgh")
        print(len(image))
        for i in range(0,24):
            print(url[i])
            yield response.follow(url[i], callback=self.parse_recipepage)   
        next_page = response.css("a.pagination__item-link--next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_search_results)

    def parse_recipepage(self, response):
        j =0
        j = j+1
        print(j)
        print("the maximum length is 24")
        
