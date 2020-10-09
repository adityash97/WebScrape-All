#--------------------------------------------------------------------------
# Read "Next_Men_Clearance_README.txt" file for little guide and explation.      
# 10/2020
# Aditya Anand,India                                          
# mail     : adityash212@gmail.com                                 
# github   : https://github.com/adityash97/                        
# linkedin : https://www.linkedin.com/in/aditya-anand-7a9a4214b/   
#---------------------------------------------------------------------------

import scrapy        # To scrape data
import json          # To work with JSON response
import pandas as pd  # To create csv file


'''
To crate csv file 'scrapy' could also be used but it was not creating file in desired structure.
So i have used 'Panads'.
'''

class Next_Men_Clearance(scrapy.Spider):
    name = "Next_Men_Clearance"
    start_urls = [
        "https://www.next.co.uk/clearance/filters/search?w=*&af=gender:men"  # To get total no. of product(men) dynamically.
    ]
    page_url = "https://www.next.co.uk/clearance/results/search?w=*&af=gender:men gender:men &srt=0" # Url which need to be scraped
    path = '/Users/aditya/Desktop/Desktop/dataScience/ScrapeWeb/Next_Men_Clearance/' # Path to save csv file
    total_no_products = 0 # Intially 0. It will be updated dynamically
    Name            = [] 
    Brand           = []  
    OriginalPrice   = []  
    DiscountedPrice = []
    ImageUrl        = []

    # To create a csv file
    def toCsv(self): 
        data = {
                'Name':self.Name,
                'Brand':self.Brand,
                'OriginalPrice':self.OriginalPrice,
                'DiscountedPrice':self.DiscountedPrice,
                'ImageUrl':self.ImageUrl
            }
        df = pd.DataFrame(data=data)
        df.to_csv(self.path+'Next_Men_Clearance.csv')

    # To get the total no of product(only once)
    def parse(self,response): 
        if(response.status == 200):
            data = json.loads(response.text)
            # Traversing through json data to get total no of products.
            for i in range(len(data['SearchFilters'])):
                if(data['SearchFilters'][i]['Name']== "gender"):
                    for men in range(len(data['SearchFilters'][i]['FilterOptions'])):
                        if(data['SearchFilters'][i]['FilterOptions'][men]['Value'] == "gender:men"):
                                self.total_no_products =  data['SearchFilters'][i]['FilterOptions'][men]['Count'] # Total available product
                                print("Length of total No of produt(men): ",self.total_no_products) 
                                yield scrapy.Request(self.page_url,callback=self.scrape)  # Calling 'scrape' method to scrape data from 'page_url'
                                break
        else:
            print("*"*8,"Some Error","*"*8)
            print("Status Code :",response.status)

    # To Scrape Data from 'page_url'
    def scrape(self, response):                 
        data = json.loads(response.text)
        for i in range(len(data)) :
            # print((data[i]['SearchPosition'])) 
            self.Name.append(data[i]['Name'])   # for name
            self.Brand.append(data[i]['Brand']) #for brand
            if(data[i]['History']):  
                self.OriginalPrice.append(data[i]['History']['PriceHistory'][0]['Price'])       #for original price 
                if(len(data[i]['History']['PriceHistory'])>1 ): #If not then only 1 price is avilable in 'data[i]['History']['PriceHistory'](<== list)'
                    self.DiscountedPrice.append(data[i]['History']['PriceHistory'][1]['Price']) # for discounted price
                else:
                    self.DiscountedPrice.append(None)
            else:  # If no "data[i]['History']" available then "it has Special Offer".
                self.OriginalPrice.append("£"+data[i]['ItemOptions'][0]['OriginalPrice']) #for original price 
                self.DiscountedPrice.append("£"+data[i]['ItemOptions'][0]['WasPrice'])    # for discounted price
            self.ImageUrl.append("https://xcdn.next.co.uk/COMMON/Items/Default/Default/ItemImages/Sale" + data[i]['SearchImage']) #image url
        if(int(data[len(data)-1]['SearchPosition']) < int(self.total_no_products)): 
            next_url = "https://www.next.co.uk/clearance/results/search?w=*&af=gender:men gender:men &srt="+str(data[len(data)-1]['SearchPosition']) # Making call to next page if above condition satisfied.
            print("Next Url called :\n",next_url) # Check console for URL.
            yield response.follow(url=next_url,callback=self.scrape)  # Calling 'next_url'.
        else: # If above 'if' fails then it means we reach to end of page and now we need to create csv file.
            self.toCsv()