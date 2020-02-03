import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


words = [] #List to store rating of the product
driver = webdriver.Chrome()
driver.get("https://relatedwords.org/relatedto/accreditation")

content = driver.page_source
soup = BeautifulSoup(content)
a = soup.find('div', attrs={'class':'words'})

for i in a.findAll('a',attrs = {'class':'item'}):
    name = i.text
    words.append(name)

print (words)