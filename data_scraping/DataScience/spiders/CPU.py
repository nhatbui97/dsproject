import scrapy
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('f3db8c309963dd4e3fdd7f8c9520a3a2')

class CpuSpider(scrapy.Spider):
    name = 'CPU'
    allowed_domains = ['www.techpowerup.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }


    def start_requests(self):
        for i in range(2000, 2023):
            for j in ['AMD', 'Intel']:
                yield scrapy.Request(client.scrapyGet(url='https://www.techpowerup.com/cpu-specs/?mfgr=' + 
                    j + '&released=' + str(i) + '&sort=name'), self.parse)

        yield scrapy.Request(client.scrapyGet(url='https://www.techpowerup.com/cpu-specs/?mfgr=VIA&sort=name'), self.parse)


    def parse(self, response):
        rows = response.xpath('//table[@class="processors"]/tr')
        for row in rows:
            yield{
                'CPU': row.xpath('./td/a/text()').get(),
                'Cores': row.xpath('./td[3]/text()').get(),
                'Clock': row.xpath('./td[4]/text()').get(), 
                'Process': row.xpath('./td[6]/text()').get(),
                'L3 Cache': row.xpath('./td[7]/text()').get(),
                'TDP': row.xpath('./td[8]/text()').get(),     
            }

#from scrapy import cmdline
#cmdline.execute("scrapy crawl CPU -o file:///c:/Users/NhatBui/Desktop/dsproject/raw_data/cpu.csv:csv".split())