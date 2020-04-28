from bs4 import BeautifulSoup
from selenium import webdriver
from re import sub
from decimal import Decimal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Firefox("/usr/local/Cellar/geckodriver/0.26.0/bin/", options=options)

driver.get("https://www.flatirondistrictataustinranch.com/floorplans/bedrooms--1/rent--under-1400")
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')


container = soup.find(class_="content-section").find(class_="container-bs3").find(class_="row-bs3").find(id="ctmcontentcontainer").find(id="RentCafeContent").find(id="FloorPlanContainer").find(id="mainformcontainer").find(id="innerformdiv").find(class_="tab-content").find(id="FPhideMap").find(class_="fp-wrapper").find(id="floorplanCards").find("h2", string="6A8").parent.find(class_="fp-price").find(class_="amount")

price = 0
for string in container.stripped_strings:
    price = Decimal(sub(r'[^\d.]', '', string))

print(price)

if price <= 1200.00:
    # enter your email credentials here before running
    MY_ADDRESS = ''
    PASSWORD = ''

    smtp = smtplib.SMTP(host='smtp.live.com', port=587)
    smtp.starttls()
    smtp.login(MY_ADDRESS, PASSWORD)

    priceMsg = MIMEMultipart()

    priceMsgSubject = 'The price for 6A8 is ' + str(price)
    priceMsgBody = 'Jump on that shite!'

    priceMsg['From'] = MY_ADDRESS
    priceMsg['To'] = MY_ADDRESS
    priceMsg['Subject'] = priceMsgSubject

    priceMsg.attach(MIMEText(priceMsgBody))

    smtp.send_message(priceMsg)
    del priceMsg

    smtp.quit()

