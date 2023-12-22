import scrapy
from urllib.parse import urlparse
import json
import pkgutil
import json


class WtbSpider(scrapy.Spider):
    name = 'wtb'
    #allowed_domains = ['http://wtb.app.channeliq.com','track.app.channeliq.com','www.samsclub.com']

    def start_requests(self):
        content = pkgutil.get_data('wtb_practise', 'wtbs_doc/wtbs.json')
        content_json = json.loads(content)

        '''
        with open('wtb_practise/wtbs_doc/wtbs.txt', 'r') as f:
            self.urls = f.read()
        self.final_urls = self.urls.split("\n")
        #self.audit = "AcsSony"
        '''
        final_urls= content_json['Links']
        for i in final_urls:

            yield scrapy.Request(i, callback=self.parse)


    def parse(self, response):
        wtb = response.url
        try:
            wtb_sku = wtb.split("/")[5].split(".")[0]
        except:
            wtb_sku = wtb.split("/")[5]
        iswtb = "false"
        noretailer_handling = True
        #response.xpath("//a[@class='ciq-buy-now-button']/span/text()").get() == "SHOP NOW":
        #if 1==1:
        n=1
        retailer = response.xpath("//tr[starts-with(@class,'ciq-online')]")
        for i in retailer:
            if response.xpath(f"(//td[@class='ciq-online-offers-retailer-logo'])[{n}]/img/@title").get() == "AcsSony":
                noretailer_handling = False
                iswtb = "true"
                name = response.xpath(f"(//td[@class='ciq-online-offers-retailer-logo'])[{n}]/img/@title").get()
                link = i.xpath(".//a[@class='ciq-buy-now-button']/@href").get()
                n=n+1
                yield scrapy.Request(url=link, callback=self.ret_parse_AcsSony, meta={"name": name, "wtb": wtb, "iswtb":iswtb, "wtb_sku": wtb_sku}, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"})

        if noretailer_handling:
            no_offer_link = f"https://acssony.si/index.php?route=product/search&search={wtb_sku}"
            yield scrapy.Request(
                no_offer_link,
                callback=self.ret_parse_nooffer,
                meta={"wtb": wtb, "wtb_sku" : wtb_sku, "iswtb":iswtb},
                headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
            )

    def ret_parse_AcsSony(self,response):
        name = response.meta["name"]
        wtb=response.meta["wtb"]
        iswtb = response.meta["iswtb"]
        wtb_sku = response.meta["wtb_sku"]
        domain_name=urlparse(response.url).netloc
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
            "WTB" : wtb,
            "wtb_sku" : wtb_sku,
            "retailer": name.strip(),
            "retailer_link": response.url.split("?")[0],
            "isunavailable" : isunavailable,
            "price": price,
            "sku": final_sku,
            "isproduct" : isproduct,
            "iswtb": iswtb,
            "domain_name" : domain_name
        }
    def ret_parse_nooffer(self,response):
        product = response.xpath("//div[@class='item single-product']").extract()
        iswtb = response.meta["iswtb"]
        wtb = response.meta["wtb"]
        wtb_sku = response.meta["wtb_sku"]
        if len(product) == 1:
            product_link = response.xpath("//a[@class='product-name']/@href").get()
            yield scrapy.Request(
                product_link,
                callback=self.ret_parse_AcsSony,
                meta={"wtb": wtb, "wtb_sku" : wtb_sku, "iswtb":iswtb, "name" : "False"},
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
                }
            )
        else:
            yield {
                "WTB": wtb,
                "wtb_sku": wtb_sku,
                "retailer": None,
                "retailer_link": None,
                "isunavailable": None,
                "price": None,
                "sku": None,
                "isproduct": None,
                "iswtb": iswtb,
                "domain_name": None
            }