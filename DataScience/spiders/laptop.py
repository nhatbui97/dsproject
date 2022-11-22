import scrapy
from scrapy.http.request.form import FormRequest
from scrapy import cmdline    

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    allowed_domains = ['www.notebookcheck.net']

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }
    
    lst_year = []
    from_year = 2008
    to_year = 2009
    OS = {'Windows': '1', 'MacOS': '2', 'Linux': '3'}
    Windows_Manufacturers = ['18', '11', '5', '146', '9', '447', '3', '35', '36', '15', '505']

    def start_requests(self):
        yield scrapy.Request('https://www.notebookcheck.net/Laptop-Search.8223.0.html', self.set_year_n_device)



    def set_year_n_device(self, response):
        return [FormRequest(url=response.url,
                            formdata={'year_from': str(year),
                                        'year_till': str(year),
                                        'class': '-1', 
                                        'os_type': self.OS['Windows'], 
                                        'orderby': '10',
                                        'manufacturer': manu },
                            callback=self.link_laptop) for year in range(self.from_year, self.to_year)
                                                       for manu in self.Windows_Manufacturers]



    def link_laptop(self, response):
        self.lst_year += list(response.css('td:nth-of-type(1) span::text').getall())
        links = response.css('tr td >a')
        for link in links:
            link = link.css(':link').get()
            yield scrapy.Request(link[link.index('"') + 1 : link.index('"', 9)], self.get_data)



    def get_data(self, response):

        laptop_name = response.css('div.specs_header::text').get().replace(' (', '')

        CPU = response.css('div.specs_element:contains("Processor") div.specs_details a::text').get()
        
        GPU = response.css('div.specs_element:contains("Graphics adapter") div.specs_details a::text').get()
        
        Memory = list(response.css('div.specs_element:contains("Memory") div.specs_details::text').getall())
        if len(Memory) != 0 and'Memory' in Memory[0]:
            Memory.pop(0)
        
        Storage = response.css('div.specs_element:contains("Storage") div.specs_details::text').get()

        Display = response.css('div.specs_element:contains("Display") div.specs_details::text').get()

        Weight = response.css('div.specs_element:contains("Weight") div.specs_details::text').get()
        if Weight != None:
            if 'kg' in Weight:
                Weight = Weight[:Weight.index('kg')]
            else:
                Weight = '0.' + Weight[:Weight.index('g')]

        Price = response.css('div.specs_element:contains("Price") div.specs_details::text').get()

        yield{
            'laptop_name': laptop_name,
            'CPU': CPU,
            'GPU': GPU,
            'Memory': Memory,
            'Storage': Storage,
            'Display': Display,
            'Weight(kg)': Weight,
            'Price': Price,
        }
        
cmdline.execute("scrapy crawl laptop -o windows_laptop.csv".split())

lst_year = LaptopSpider.lst_year
for i in len(lst_year):
    if lst_year[i] == '01.01.1970':
        lst_year[i] = None

import pandas as pd
data = pd.read_csv('windows_laptop.csv', index_col=False)
data['year'] = lst_year
data['OS'] = 'Windows'
data.to_csv('windows_laptop.csv', index=False)

