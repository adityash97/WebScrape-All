#--------------------------------------------------------------------------
# Read "Oneill_Serpstack_README.txt" file for little guide and explation.      
# 10/2020
# Aditya Anand,India                                          
# mail     : adityash212@gmail.com                                 
# github   : https://github.com/adityash97/                        
# linkedin : https://www.linkedin.com/in/aditya-anand-7a9a4214b/   
#---------------------------------------------------------------------------
import scrapy
import json
import csv
import pandas as pd

class Oneill_Serpstack(scrapy.Spider):
    name = 'Oneill_Serpstack'
    start_urls =[
        "http://api.serpstack.com/search?access_key=5f50ee37700b8d5712a5abe4d51095ba&query=oneill.com/fr '0A4972-9950"

    ]
    def __init__(self):
        self.Initial_Count = 0
        self.Google_Code = []  #work Done
        self.Url = []
        self.Price = []
        self.Api_Count = 0
        # Using 3 Api Keys. can only make 100 calls for each api. So doing 50 call from each.
        self.Apis ={
            0:'0050fdbb472c6c7135441d8a6a1aec6c',
            1:'a21546670751da2c676512a97d4d5666',
            2:'b609ed2c4bcfa532a605153a046690c5'
        }
        self.File_Path = "/Users/aditya/Desktop/Desktop/dataScience/ScrapeWeb/Greendeck Business Analyst Assignment Task 4 - Sheet1.csv"
        self.Output_Path =  "/Users/aditya/Desktop/Desktop/dataScience/ScrapeWeb/Oneill_Serpstack/"
        self.count = 0
        # Storing all Google Search Code into Pyhtn List.
        with open(self.File_Path,'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for i in reader:
                    self.Google_Code.append(i[2])
                    
    # Working with json response and extracting product url.
    def parse(self,response):
        print("*"*20,"Parse is called","*"*20)
        inserted = 0 # to detect if prouct url is inserted into 'Url' or not
        url = ''
        data = json.loads(response.text)
        if data['organic_results']: # If organic_result is not available then url won't be able to extract.
            for value in range(len(data['organic_results'])):
                if data['organic_results'][value]['domain'] == 	"www.oneill.com":
                    if self.Google_Code[self.Initial_Count] in data['organic_results'][value]['url']:  #insert google code dynamically
                        print("Initial Count",self.Initial_Count)
                        url = data['organic_results'][value]['url']
                        inserted +=1  #if url inserted then 'inserted' will be incremented
                        break


        if(inserted == 0): # It means url is not found and also price cannot be scraped
            print ("*"*20,"Appending Default. Url Not Found","*"*20)
            self.Url.append("Url Not Found")  
            self.Price.append("No Url to scrape price")
            if(self.Initial_Count < len(self.Google_Code)-1):
                self.Initial_Count +=1
                self.apiCountTracker() # To track which api key should be used now.
                print("Initial Count :",self.Initial_Count) # To notify which record no is being used.
                # Append access key and Google Code to make next url.
                next_url = f"http://api.serpstack.com/search?access_key={self.Apis[self.Api_Count]}&query=oneill.com/fr '{self.Google_Code[self.Initial_Count]}"
                yield scrapy.Request(next_url,callback=self.parse)  # calling back parse
            else:
                yield {
                    "Url":self.Url,
                    "Price":self.Price
                }
  
        else:
            # Means url is inserted and Product url is found so Price can be scraped now.
            print("*"*10,"Current Product Url = ",data['organic_results'][value]['url'],"*"*10) # Current Product Url
            self.Url.append(url)
            next_url = url
            yield scrapy.Request(next_url,callback=self.scrapePrice) #Calling scrapePrice to scrape Price 


    # Will track which key should be used
    def apiCountTracker(self):
                if(self.Initial_Count < 50):
                    self.Api_Count = 0 # Will Take key at 0.
                elif self.Initial_Count > 50 and self.Initial_Count < 100:
                    self.Api_Count = 1 # Will Take key at 1.
                else:
                    self.Api_Count = 2 # Will Take key at 2.


    # To Scrape Price
    def scrapePrice(self,response):
        price = response.css("span.sales")[0].extract().split() #css selector
        for p in price:
            if p.startswith('content'):
                try: # if price is scraped 
                    float(p[9:14])  
                    self.Price.append("€"+p[9:14])
                except: # if program not able to scrape price. I was getting 'null' for some records.
                    print("Not able to scrape Price.")
                    self.Price.append("Not able to scrape Price.")
        if(self.Initial_Count < len(self.Google_Code)-1): #checking are we reached to bootom or not
                self.Initial_Count +=1
                self.apiCountTracker()
                next_url = f"http://api.serpstack.com/search?access_key={self.Apis[self.Api_Count]}&query=oneill.com/fr '{self.Google_Code[self.Initial_Count]}"
                yield scrapy.Request(next_url,callback=self.parse)
        else: # If 'if' condition fails means we reached at bottom. Time to create csv file
            data = {
                "Url":self.Url,
                "Price":self.Price
            }
            df = pd.read_csv(self.File_Path)
            df['Product Url'] = self.Url
            df['Product Price'] = self.Price
            df.to_csv(self.Output_Path+'output.csv')
            yield data # To display on console.