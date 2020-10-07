#--------------------------------------------------------------------------
# Read "FARFETCH_MEN_SHOES_README.txt" file for little guide and explation.        
# 10/2020 
# Aditya Anand,India                                          
# mail     : adityash212@gmail.com                                 
# github   : https://github.com/adityash97/                        
# linkedin : https://www.linkedin.com/in/aditya-anand-7a9a4214b/   
#---------------------------------------------------------------------------
import scrapy
import pandas as pd # pandas to create .csv file

'''
To crate csv file 'scrapy' could also be used but it was not creating file in desired structure.
So i have used 'Panads'.
'''

class FARFETCH_MEN_SHOES(scrapy.Spider): #class 'FARFETCH_MEN_SHOES' inheriting 'scrapy.Spider' class
    name = "FARFETCH_MEN_SHOES"  # name of program
    Page_no = 2                  # To point on next page.
    Path = "/Users/aditya/Desktop/Desktop/dataScience/ScrapeWeb/FARFETCH_MEN_SHOES/FARFETCH_MEN_SHOES/" #path to save csv file
    Names        = []            # For ame of Product
    Brands       = []            # For Brand of Product
    Prices       = []            # For Price of Product
    ImageUrls    = []            # For Image Url of Product
    ProductLinks = []            # For Link of Product
    
    start_urls = [
        'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx'  # Starting url
    ]
    def createCsv(self):
        # 'data' is a dictionary which contains all the scrapped data in key-value pair.
        data ={
            'Name': self.Names,
            'Brand': self.Brands,
            'Price €': self.Prices,
            'ImageUrl':self.ImageUrls,
            'ProductUrl':self.ProductLinks
        }
        df = pd.DataFrame(data = data)  # Making 'data' as Pandas DataFrame and storing back into 'df' variable
        df.to_csv(self.Path+"FARFETCH_MEN_SHOES.csv") #Storing 'df' as '.csv' file.

    def parse(self, response):          # 'response' is having all our responsed data

        if response.status == 200:      #if status is 200 means we got response.

            '''There were two url for a product. So to take first url i wrote some business logic'''
            imagUrl = response.xpath('//meta/@content').extract()
            oddOnly = 1
            len =0
            # Business logic to take one image url
            for i in imagUrl:
                if(i.startswith('https://cdn-images') and oddOnly%2 != 0):
                    self.ImageUrls.append(i)  #Storing url of products in 'imageUrls'
                oddOnly += 1                  #taking only first link from two link

            #Storing name of products in 'names'
            names =  response.xpath("//a[@class='_5ce6f6']//p[@class='_d85b45']/text()").extract()
            for name in names:
                self.Names.append(name)

            #Storing brand of products in 'brands'
            brands = response.xpath('//h3[@class="_346238"]/text()').extract()
            for brand in brands:
                self.Brands.append(brand)

            #Storing price of products in 'prices'
            prices = response.xpath("//div[@class = '_6356bb']//span/text()").extract()
            for price in prices:
                self.Prices.append(price)

            #Storing productlink of products in 'productLinks'
            productLink = response.xpath("//a[@class = '_5ce6f6']")       #productLinks pointing to response data
            links = productLink.xpath("@href").extract()                  #extracting link from productlink
            productLinks = ["https://www.farfetch.com"+i for i in links]  # Appending string to complete a valid product link
            for prodUrl in productLinks:
                self.ProductLinks.append(prodUrl)
            '''
            Uncomment below 'yield {}' to see output in console 
            '''
            # yield  {
            #         'Name': names,
            #         'Brand': brands,
            #         'Price €': prices,
            #         'ImageUrl':self.ImageUrls,
            #         'ProductUrl':productLinks
            # } # to see at console.
            
            '''
            'next_page' is containing address(url) of next page.
            'self.Page_no' is being incrementd every time to point on next page.
            '''
            next_page = "https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page="+str(self.Page_no) 
            if(self.Page_no<87): # total no. of pages are 86.
                self.Page_no+=1  
                yield response.follow(next_page,callback=self.parse) # calling back 'self.parse'. Kind of Recursion.
            else:
                '''
                If we reach to page no 86 then above 'if condition' will be False and control
                will come in 'else' part and will a 'FARFETCH_MEN_SHOES.csv.csv' file by calling
                'createCsv()' function.
                '''
                print("Creating csv") 
                self.createCsv()
        else:
            print("*"*8,"Some Error","*"*8)
            print("Status Code : ",response.status)
                