import scrapy
from scrapy.http.request.form import FormRequest

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    allowed_domains = ['www.notebookcheck.net']
    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }
    
    #scrape info
    lst_year = []
    from_year = 2005
    to_year = 2023
    OS = {'Windows': '1', 'MacOS': '2', 'Linux': '3'}
    Windows_Manufacturers = ['18', '11', '5', '146', '9', '447', '3', '35', '36', '15', '505']


    def start_requests(self):
        yield scrapy.Request('https://www.notebookcheck.net/Laptop-Search.8223.0.html', self.form_rq)



    def form_rq(self, response):
        lst_rq = []
        for year in range(self.from_year, self.to_year):
            for manu in self.Windows_Manufacturers:
                rq = FormRequest(url=response.url,
                                formdata={'year_from': str(year),
                                        'year_till': str(year),
                                        'class': '-1', 
                                        'os_type': self.OS['Windows'], 
                                        'orderby': '10',
                                        'manufacturer': manu },
                                callback=self.link_laptop,
                                cb_kwargs=dict(main_url=response.url))
                rq.cb_kwargs['year'] = year
                lst_rq.append(rq)
        return lst_rq



    def link_laptop(self, response, main_url, year):
        links = response.css('tr td >a')
        for link in links:
            link = link.css(':link').get()
            rq = scrapy.Request(link[link.index('"') + 1 : link.index('"', 9)],
                                callback=self.get_data,
                                cb_kwargs=dict(main_url=response.url))
            rq.cb_kwargs['year'] = year
            yield rq



    def get_data(self, response, main_url, year):

        Laptop_name = response.css('div.specs_header::text').get().replace(' (', '')

        Year = str(year)

        CPU = response.css('div.specs_element:contains("Processor") div.specs_details a::text').get()
        
        GPU = response.css('div.specs_element:contains("Graphics adapter") div.specs_details a::text').get()
        
        Memory = list(response.css('div.specs_element:contains("Memory") div.specs_details::text').getall())
        if len(Memory) != 0 and 'Memory' in Memory[0]:
            Memory.pop(0)
        
        Storage = response.css('div.specs_element:contains("Storage") div.specs_details::text').get()

        Display = response.css('div.specs_element:contains("Display") div.specs_details::text').get()

        Weight = response.css('div.specs_element:contains("Weight") div.specs_details::text').get()
        if Weight != None:
            if ' kg' in Weight:
                Weight = Weight[:Weight.index(' kg')]
            elif ' g' in Weight:
                Weight = '0.' + Weight[:Weight.index(' g')]

        Price = response.css('div.specs_element:contains("Price") div.specs_details::text').get()

        yield{
            'Laptop_name': Laptop_name,
            'Year': Year,
            'CPU': CPU,
            'GPU': GPU,
            'Memory': Memory,
            'Storage': Storage,
            'Display': Display,
            'Weight(kg)': Weight,
            'Price': Price,
        }
        

#from scrapy import cmdline
#cmdline.execute("scrapy crawl laptop -o file:///dsproject/raw_data/MacOS_laptop.csv:csv".split())