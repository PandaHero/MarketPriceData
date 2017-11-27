'''
Created on 2017-11-27

@author: chen
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
#获取浏览器驱动
from pyquery import PyQuery as pq
driver=webdriver.Chrome()
driver_wait=WebDriverWait(driver,10)
def search():
    driver.get("http://www.vegnet.com.cn/Market/List?page=1")
    html = driver.page_source
    print(html)
    doc=pq(html)
    items=doc("#price_right .gre_k .frame_list1").items()
    for item in items:
        print(item)
    
def main():
    search()
if __name__ == '__main__':
    main()