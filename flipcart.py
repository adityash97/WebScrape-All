import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

no_of_page_to_be_scraped = 13
first_range = 10000
second_range = 20000
url = f'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3D{first_range}&p%5B%5D=facets.price_range.to%3D{second_range}'


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
productUrls = []
productImageUrls = []
productNames = []
productRatings = []
productSpecs = []
discountedPrices = []
originalPrices = []
discounts = []


def makeCsv():
    header = ['No','productName', 'productUrl',
              'productImageUrl', 'productRating', 'productSpec', 'discountedPrice', 'originalPrice', 'discounts']
    with open('trustchecker.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(productNames)):
            content = [i+1,productNames[i], productUrls[i], productImageUrls[i], productRatings[i], productSpecs[i], discountedPrices[i], originalPrices[i], discounts[i]]
            writer.writerow(content)


def scrapeData(page):
    print(f"Scraping page no : {page} ")
    products = driver.find_elements(by=By.CLASS_NAME, value='_1fQZEK')
    for data in products:
        try:
            # print(page)
            product_url = data.get_property('href')
            productUrls.append(product_url)
            product_image_url = data.find_element(
                by=By.TAG_NAME, value='img').get_property('src')
            productImageUrls.append(product_image_url)
            product_name = data.find_element(
                by=By.CLASS_NAME, value='_4rR01T').text
            productNames.append(product_name)
            try:
                product_rating = data.find_element(by=By.CLASS_NAME, value='_3LWZlK').text
            except:
                product_rating="NA"
            productRatings.append(product_rating)
            product_spec = []
            for spec in data.find_element(by=By.CLASS_NAME, value='fMghEO').find_elements(by=By.CLASS_NAME, value='rgWa7D'):
                product_spec.append(spec.text)
            productSpecs.append(product_spec)
            try:
                discounted_price = data.find_element(
                by=By.CLASS_NAME, value='_30jeq3').text
            except:
                discounted_price="NA"
            discountedPrices.append(discounted_price)
            try:
                original_price = data.find_element(by=By.CLASS_NAME, value='_3I9_wc').text
            except:
                original_price = 'NA'
            originalPrices.append(original_price)
            try:
                discount = data.find_element(by=By.CLASS_NAME, value='_3Ay6Sb').text
            except:
                discount = "NA"
            discounts.append(discount)
        except Exception as e:
            # print(e)
            pass
    if(page < no_of_page_to_be_scraped):
        page += 1
        print(f"calling next page {page}")
        try:
            driver.find_elements(by=By.CLASS_NAME, value='_1LKTO3')[-1].click()
        except Exception as e:
            # print(f"Unable to go to next page : {e}")
            makeCsv()
            driver.quit()
        print("Delaying 5 sec")
        time.sleep(5)
        scrapeData(page)
    else:
        makeCsv()
        driver.quit()


scrapeData(1)  # 1 is the initial page no.


