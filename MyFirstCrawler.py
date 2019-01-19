#爬奇摩股市抓取商品代號與名稱
#1.抓取所有分類並存檔
#2.從分類理抓取個股並輸出

import requests
from decimal import Decimal
from bs4 import BeautifulSoup


path_cat = "cat.txt"
path_stock = "stock.txt"
path_detail = "stock_detail.txt"

url1 = 'https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=%A5b%BE%C9%C5%E9&form=menu&form_id=stock_id&form_name=stock_name&domain=0' #上市網址
url2 = 'https://tw.stock.yahoo.com/h/kimosel.php?tse=2&cat=%C2d%A5b%BE%C9&form=menu&form_id=stock_id&form_name=stock_name&domain=0' #上櫃網址
url3 = 'https://tw.stock.yahoo.com/q/q?s=' #個股報價網址
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

def get_cat(url):
    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text)

    # 抓取所有分類並存檔
    file = open(path_cat, 'a', encoding='utf8')
    cat_box = soup.select('.c3')
    for cat in cat_box:
        if len(cat.select('a')) and cat.text!='上市' and cat.text!='上櫃':
            href = cat.select('a')[0]['href']
            text = cat.text
            file.write(text+','+href+'\n')

    file.close()

def get_detail(stock_text):
    stock_num = stock_text.split(" ")[0]
    re = requests.get(url3+stock_num, headers=headers)
    soup = BeautifulSoup(re.text)

    # 抓取報價並存檔
    file = open(path_detail, 'a', encoding='utf8')
    file.write(stock_text + '|')
    detail_tr = soup.select('tr')[10]
    detail_td = detail_tr.select('td')
    #print(detail_tr)
    for i in range(1,11):
        if i==5:
            if detail_td[2].text!="－" and detail_td[7].text!="－":
                diff = Decimal(detail_td[2].text) - Decimal(detail_td[7].text)
                file.write(str(diff) + '|')
            else:
                file.write('－|')
        elif i==11:
            file.write(detail_td[i].text)
        else:
            file.write(detail_td[i].text + '|')
    file.close()

def get_stock(url, cat):
    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text)
    # 抓取所有個股並存檔
    file = open(path_stock, 'a', encoding='utf8')
    file.write("-----"+cat+"-----\n")
    stock_box = soup.select('.none')
    for stock in stock_box:
        file.write(stock.text+'\n')
        get_detail(stock.text)
        #break
    file.close()

import os
if os.path.exists(path_cat):
    os.remove(path_cat)

get_cat(url1)
#get_cat(url2)

if os.path.exists(path_stock):
    os.remove(path_stock)

if os.path.exists(path_cat):
    os.remove(path_detail)

file = open(path_cat, 'r', encoding='utf8')
# 透過迴圈方式一次讀一行出來
for line in file:
    text = line.split(",")
    cat = text[0]
    url = text[1]
    get_stock("https://tw.stock.yahoo.com"+url, cat)
    #break
file.close()