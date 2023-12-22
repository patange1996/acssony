import scrapy
import json


class AcssonyNoofferSpider(scrapy.Spider):
    name = 'wtb_nooffer'
    #allowed_domains = ['https://acssony.si/index.php?route=product/search']
    start_urls = ['https://acssony.si/index.php?route=product/search&limit=100&search=sony&bfilter=m0:10;&page=1']

    def parse(self, response):
        products = response.xpath("//div[@class='item single-product']")
        for i in products:
            link = i.xpath(".//a[@class='product-name']/@href").get().split("?")[0]
            yield scrapy.Request(link, callback=self.parse_page, meta={"link":link}, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"})
        next_page = response.xpath("(//a[contains(text(),'>')])[1]/@href").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        link = response.meta["link"]
        try:
            resp = json.loads(response.xpath("normalize-space((//script[@type='application/ld+json'])[1]/text())").get())
        except ValueError:
            #sku = response.xpath("//div[@id='tab-description']/h1/text()").get()
            resp = {"model" : "Error json" , "@type" : "Error json", }
        stock = response.xpath("(//p[starts-with(@class,'info')])[1]/span/text()").get()
        price = response.xpath("//span[starts-with(@class,'live-price')]/text()").get()

        try:
            final_sku = str(resp['model'].split('-')[0]) + str(resp['model'].split('-')[1])
        except IndexError:
            final_sku = resp['model']

        #product page identification
        if resp['@type'] == "Product":
            isproduct = "true"
        else:
            isproduct = "false"

        #isunavailable
        if stock == "Po naročilu" or stock == None:
            isunavailable = "true"
        else:
            isunavailable = "false"
        yield {
            "WTB": None,
            "retailer": "AcsSony",
            "retailer_link": response.url.split("?")[0],
            "isunavailable": isunavailable,
            "price": price,
            "sku": final_sku,
            "isproduct": isproduct,
            "iswtb": None,
            "domain_name": None

        }

