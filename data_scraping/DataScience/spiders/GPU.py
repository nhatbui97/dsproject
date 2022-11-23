import scrapy
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('f3db8c309963dd4e3fdd7f8c9520a3a2')

class GpuSpider(scrapy.Spider):
    name = 'GPU'
    allowed_domains = ['www.techpowerup.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }


    def start_requests(self):
        for year in range(1986, 2003):
                yield scrapy.Request(client.scrapyGet(url='https://www.techpowerup.com/gpu-specs/?released='
                    + str(year) + '&sort=name'), self.parse)

        for manu in ['Sony', 'Matrox', 'XGI']:
                yield scrapy.Request(client.scrapyGet(url='https://www.techpowerup.com/gpu-specs/?mfgr=' 
                    + manu + '&sort=name'), self.parse)

        for year in range(2003, 2024):
            for manu in ['AMD', 'ATI', 'Intel', 'NVIDIA']:
                yield scrapy.Request(client.scrapyGet(url='https://www.techpowerup.com/gpu-specs/?mfgr='
                    + manu + '&released=' + str(year) + '&sort=name'), self.parse)



    def parse(self, response):  
        rows = response.xpath('//table[@class="processors"]/tr')
        for row in rows:
            yield{
                'GPU': row.xpath('./td/a/text()').get(),
                'GPU memory': row.xpath('./td[5]/text()').get(),
                'GPU clock': row.xpath('./td[6]/text()').get(), 
                'GPU memory clock': row.xpath('./td[7]/text()').get(),     
            }

#from scrapy import cmdline
#cmdline.execute("scrapy crawl GPU -o file:///c:/Users/NhatBui/Desktop/dsproject/raw_data/gpu.csv:csv".split())