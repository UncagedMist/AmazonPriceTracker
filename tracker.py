import requests
from bs4 import BeautifulSoup
import smtplib

choice_price = 1   # edit this to make your choice price at which you want to purchase the product
  

URL = 'YOUR_PRODUCT_URL_GOES_HERE'

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def check_price():
    page = requests.get(URL,headers = headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id= "productTitle").get_text()
    price = soup2.find(id="priceblock_ourprice").get_text()
    
    # below 4 lines of codes has been used to remover extra currency symbol,commas etc. from the given price
    
    p1 = price.translate({ord(i): None for i in '₹'})
    p2 = p1.translate({ord(i): None for i in ' '})
    p3 = p2.translate({ord('\n'): None})
    p4 = p3.translate({ord(','): None})

    converted_price = float(p4[0:5])     # convert the given price into float number price

    print(converted_price)
    print(title.strip())

    # check the condition if it is true then send email
    if(converted_price < choice_price):
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()


    server.login('SENDER_EMAIL','SENDER_APP_PASSWORD_FOR_MAIL')

    # Email Contents

    subject = 'Price fell down'
    body = 'Check the amazon link\n'+URL
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'SENDER_EMAIL',
        'RECEIVER_EMAIL',
        msg
    )
    print('HEY EMAIL HAS BEEN SENT!')

    server.quit()


check_price()