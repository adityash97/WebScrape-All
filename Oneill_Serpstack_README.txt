For Oneill_Serpstack.py file.

Requirements :
    1.python 3.x
    2.Scrapy
    3.json
    4.Pandas


Command to execute directly:
    1.scrapy runspider filename.py


Command to execute when "Next_Men_Clearance.py" is being paste in scrapy folder structure :
    1. scrapy crwal name (name => Class variable. Given in "Oneill_Serpstack" class)

To Save .csv file in desired path :
    1. Edit class variable 'Output_Path' inside 'Oneill_Serpstack' class in "Oneill_Serpstack.py" file.


Algorithm:

def __init__():
    Url =[]
    Price = []
    Google_Code = []

    with open('.csvfile','w')
        store all Google Search Code from csv to python list(Google_Code)

def parse:
    inserted = 0
    Make request for url in start_urls
    if request is successfull:
        extract product url by filtering the urls coming from response.
        url = extracted_url
        Insert the url in Url(pyhton list)
        inserted+=1


    match 'inserted', if inserted == 0:
        then Insert in Url and Price "Url Not Found" and "No Url to scrape price" respectively
        beacuse if we don't have url we can't scrape price.
    else:
        store 'url' in 'Url'
        yield scrapy.Request(url,callback = scrapePrice)

def scrapePrice():
    price = using css selector to extarct price

    try:
        float(price)
        insert 'price' into 'Price'
    expect:
        # means price is not scraped (at the time i was running the program i was getting 'null')
        insert "Not able to scrape Price." into 'Price'

    create next url using available code inside 'Google_Code' and call parse again
    if code in not available inside 'Google_Code':
        then we travered all codes and time to create csv file.
    else: 
        yield scrapy(next_url,callback = parse)
    


Explatation :
Using Serpstack api to get deatils of product on "https://www.oneill.com" and then extracting 
Product Url and storing it in Python List.
After getting Product Url scraping the price from the url and storing price into Python List.

After getting all the output creating csv File from Pyhton List.
