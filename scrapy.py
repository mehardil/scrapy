import scrapy 
import re
from scrapy.crawler import CrawlerProcess
class biolase_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        'FEED_FORMAT' : 'csv',
        'OBEY_ROBOTS' : False,
        'FEED_URI' : 'Biolase-samples-data.csv',
         'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'yourproject.middlewares.ProxyMiddleware': 100,
            'yourproject.middlewares.RandomUserAgentMiddleware': 400,
        },
   }
     
    name= 'scraper'
    start_urls =['https://www.biolase.com/products/']
    def parse(self, response):
        links =response.css(".elementor-flip-box__button::attr(href)").getall()
        
        
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
    def parse_product(self, response):
        desc =response.xpath("//*[@class='elementor-text-editor elementor-clearfix']//text()").getall()
        desc = ''.join(desc)
        desc = desc.replace('\t','')
        desc = desc.replace('\n','')
        att_url =response.css('.elementor-widget-container>a.premium-button::attr(href)').getall()
        att_url =[url for url in att_url if url.endswith('.pdf')]
        att_url = set(att_url)
        att_url = ''.join(att_url)
        
        data_dict = {}
        data_dict['Seller Platform']= 'Biolase'
        data_dict['Seller SKU']= ''
        data_dict['Manufacture Name']='Biolase'
        data_dict['Manufacture Code']=''
        data_dict['Product Title']=response.css(".page-title>h1::text").get().strip()
        data_dict['Description']=desc
        data_dict['Packaging']=''
        data_dict['Qty']=''
        data_dict['Category']=response.url.split('/')[4]
        data_dict['Subcategory']=''
        data_dict['Product Page URL']= response.url
        data_dict['Attachement']= att_url
        data_dict['Image URL']=response.css(".elementor-image>img::attr(src)").getall()
        yield data_dict


process = CrawlerProcess()
process.crawl(biolase_scraper)
process.start()