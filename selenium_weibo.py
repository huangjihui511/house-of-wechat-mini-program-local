from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from fake_useragent import UserAgent
import time
from lxml import etree
from bs4 import BeautifulSoup
import re
import bs4

import json

cpath = "./chromedriver"
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(cpath, options = options)
driver.maximize_window()

# https://s.weibo.com/article?q=%E8%A1%A8%E6%83%85%E5%8C%85&Refer=weibo_article&page=6

def get_url(word, page):
    return "https://s.weibo.com/hot?q=%23{}%23&xsort=hot&suball=1&tw=hotweibo&Refer=weibo_hot&page={}".format(word, page)

def login():
    url = "https://weibo.com/"
    driver.get(url)
    input("登陆完成后输入回车")
    return

def get_weibo(word, max_page = 1):
    
    result = []
    for i in range(max_page):
        print("loading the page{}".format(i))
        url = get_url(word, i)
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        answer_page = BeautifulSoup(html, "html.parser")
        a = answer_page.find_all("div",{"class":"card"})
        for item in a:
            result += get_url_des(item)

    return result

def get_url_des(card):
    temp_txts = card.find_all("p",{"class":"txt"})
    txts = []
    for item in temp_txts:
        contents = item.contents
        str_list = []
        for item2 in contents:
            s = ""
            if type(item2) == bs4.element.NavigableString:
                s = str(item2)
            if type(item2) == bs4.element.Tag:
                s = item2.text
            str_list.append(s.replace("\n", ""))


        des = "".join(str_list).replace(" ","")
        txts.append(des)
    
    temp_imgs = card.find_all("img")
    imgs = []
    for item in temp_imgs:
        src = item.attrs["src"]
        if src[0] == "/" and src[1] == "/":
            src = src[2:]
        if src[:4] != "http":
            src = "http://" + src
        imgs.append(src)
    result = [(img,txts) for img in imgs]
    print("found {} result".format(len(result)))
    return result

def main():
    # login()
    word = "表情包"
    result = get_weibo(word, 40)
    f = open("result.json", "w")
    for r in result:
        str = json.dumps(r,ensure_ascii=False)
        f.write(str + "\n")

main()

# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome -remote-debugging-port=9222  
