For Next_Men_Clearance.py file.

Requirements :
    1.python 3.x
    2.Scrapy
    3.Pandas

Command to execute directly:
    1.scrapy runspider filename.py


Command to execute when "Next_Men_Clearance.py" is being paste in scrapy folder structure :
    1. scrapy crwal name (name => Class variable. Given in "Next_Men_Clearance" class)



To Save .csv file in desired path :
    1. Edit class variable 'path' inside 'Next_Men_Clearance' class in "Next_Men_Clearance.py" file.


Explatation :
As "https://www.next.co.uk/" is dynamic website and content are being loded by
Javascript.
So rather then playing with HTML DOM , I am using JSON response data to scrape 
this website.
After scraping all the pages at last csv file will be created.



       