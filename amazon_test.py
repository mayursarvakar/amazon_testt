from  selenium import  webdriver as wb
from selenium.webdriver.chrome.options import Options
#
from selenium.webdriver.common.by import By
import csv
import time
# import pandas as pd
# from datetime import datetime as dt
import json
# import mysql.connector


# df=pd.read_csv("unscrape_amazon.csv")
# start_time = dt.now()

# df=df[:5]

# print(df)
# print(type(df))
# country=df['id']
# Use Selenium or bs4 to Scarpe the following details from the page.
# 1. Product Title
# 2. Product Image URL
# 3. Price of the Product
# 4. Product Details

wbb=wb.Chrome(executable_path="/media/mayur/EE208F7D208F4B91/disk d/web_script/chromedriver")

# ============================================================================================
#creating blank csv-------------------------------------
with open("amazon_op.csv","a",newline='',encoding='UTF-8') as fp:
    writer=csv.writer(fp)
    writer.writerow(['Index','Product_Title','Price_of_the_Product','Product_Details','Product_Image_URL','scarp_url'])

#creating blank json---------------------
with open("amazon_op_js.json", "w", newline='', encoding='UTF-8') as fp:
    json.dump([], fp)

#creating database and table
# dbame="amazondb2"
# mydb=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="sapna@4201",
# )
#
# my_cursoor=mydb.cursor()
#
# try:
#     my_cursoor.execute(f"CREATE DATABASE {dbame}")
#     my_cursoor.close()
# except:
#     print(f"{dbame} Database alerady Created")
#
# my_cursoor.close()
#
#
# # ============enter_table_name
# table_name="amazaon_table5"
# mydb2=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="sapna@4201",
#     database= dbame
# )
# my_cursoor2=mydb2.cursor()
# # my_cursoor.execute("SHOW DATABASES")
# #
# try:
#     my_cursoor2.execute(f"CREATE TABLE {table_name}  (index VARCHAR(50),prod INTEGER (10))")
#
# # Index','Product_Title','Price_of_the_Product','Product_Details','Product_Image_URL','scarp_url'
# except Exception as e:
#     print(e)
#     print(f"{table_name} table alerady Created ")
#
# mydb2.commit()
# my_cursoor2.close()
# ==================================================================



#test
# wbb.get("https://www.amazon.it/dp/000106875X")
# price=(wbb.find_element(By.CSS_SELECTOR,"#price").text).replace(" €","")
# print(price)

wbb.get("https://www.amazon.de")
time.sleep(5)
wbb.get("https://www.amazon.es")
time.sleep(5)
wbb.get("https://www.amazon.fr")
time.sleep(5)
wbb.get("https://www.amazon.it")
time.sleep(5)

df2=pd.read_csv("Amaazon_test_links.csv")
# df2=df2[:5]

count=0
json_data=[]
for country,asin in zip(df2['country'],df2['Asin']):
    scarp_url = f"https://www.amazon.{country}/dp/{asin}"
    wbb.get(scarp_url)
    if "productTitle" in wbb.page_source:
        count=count+1
        # time.sleep(10)

        # page_source=wbb.page_source
        # if "#productTitle" in page_source:


        Product_Title = wbb.find_element(By.CSS_SELECTOR, "#productTitle").text if  wbb.find_element(By.CSS_SELECTOR, "#productTitle") else ""

        #======product_url
        try:
            Product_Image_URL = wbb.find_element(By.CSS_SELECTOR, "#imgTagWrapperId img").get_attribute('src')
        except:
            try:
                Product_Image_URL = wbb.find_element(By.CSS_SELECTOR, "#imgBlkFront").get_attribute('src')
            except:
                Product_Image_URL=""


        # ======product_price
        try:
            Price_of_the_Product = (wbb.find_element(By.CSS_SELECTOR,".a-section.a-spacing-none.aok-align-center .a-price-whole").text).replace("€","").replace("€","")
        except:
            try:
                Price_of_the_Product = (wbb.find_element(By.CSS_SELECTOR,".a-price.a-text-price.header-price.a-size-base.a-text-normal").text).replace("€","")
            except:
                try:
                    Price_of_the_Product=(wbb.find_element(By.CSS_SELECTOR,"#price").text).replace(" €","").replace("€","")
                except:
                    try:
                        Price_of_the_Product =(wbb.find_element(By.CSS_SELECTOR,".a-size-base.a-color-price.offer-price.a-text-normal").text).replace("€","")
                    except:
                        Price_of_the_Product =""


        try:
            Product_Details = wbb.find_element(By.CSS_SELECTOR, "#productDescription").text
            Product_Details = " ".join(Product_Details.split())
        except:
            Product_Details =Product_Title


        print(f"===================={count}===================================")
        print(f"Product_Title         : {Product_Title}")
        print(f"Price_of_the_Product  : {Price_of_the_Product}")
        print(f"Product_Details       : {Product_Details}")
        print(f"Product_Image_URL     : {Product_Image_URL}")
        print(f"Product_URL          : {scarp_url}")

        #======saving in csv======
        with open("amazon_op.csv", "a", newline='', encoding='UTF-8') as fp:
            writer = csv.writer(fp)
            writer.writerow([count, Product_Title, Price_of_the_Product, Product_Details, Product_Image_URL,scarp_url])

        #=======saving in json=======
        items={"Product_Title":Product_Title,
              "Price_of_the_Product":Price_of_the_Product,
              "Product_Details":Product_Details,
              "Product_Image_URL":Product_Image_URL,
              "Product_URL":scarp_url}

        json_data.append(items)

        with open("amazon_op_js.json", 'r+') as file:
            # First we load existing data into a dict.000000000000000000000000000000
            file_data = json.load(file)
            # Join new_data with file_data
            file_data.append(items)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)


    else:
        print("----------------------------------------------------------")
        print(f"unbale to scarap : {scarp_url}")



