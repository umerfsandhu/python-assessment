import scrapy

from .. import items
from ..items import AldiProjectItem
class AldiSpider(scrapy.Spider):
    name = 'Aldi'
    start_urls = [
        'https://www.aldi.com.au/en/groceries/'
    ]
    base_url = 'https://www.aldi.com.au/'

    #extracted links for Subcategories
    def parse(self,response):
        for subCat in response.xpath('//div[@class="productworld--list-item ym-gl ym-g16"]/a/@href').extract():
            yield response.follow(subCat, callback=self.parse_subcategories)

    #extracted values of Product
    def parse_subcategories(self,response):
        productname = response.xpath('//div[@class="box--description--header"]/text()').extract()
        product_title = [elem.strip('\t\n') for elem in productname]  # removing extra spaces and lines
        productImage= response.xpath('//div[@class="box m-text-image"]/div/div[1]/img/@src').extract()
        packSize= response.xpath('//div[@class="box--price"]/span[@class="box--amount"]/text()').extract()
        price= response.xpath('//div[@class="box--price"]/span[@class="box--value"]/text()').extract() #price in $
        priDeci = response.xpath('//div[@class="box--price"]/span[@class="box--decimal"]/text()').extract()  # price in cents

        pricePerUnit = response.xpath('//div[@class="box--price"]/span[@class="box--baseprice"]/text()').extract()
           # items['productTitle'] = productTitle
           # items['productImage'] = productImage
            #items['packSize'] = packSize
            #items['price'] = price
            #items['pricePerUnit'] = pricePerUnit
        for item in zip(product_title, productImage, packSize, price,priDeci,pricePerUnit):
            product = {

                'product_title': item[0],
                'productImage': item[1],
                'packSize': item[2],
                'price': item[3]+item[4],
                'pricePerUnit': item[5]

            }

            yield product




