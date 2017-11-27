'''
Created on 2017-11-27

@author: chen
'''
from bs4 import BeautifulSoup

import csv
import requests
def get_total_url():
    for i in range(1, 30):
        url = "http://www.vegnet.com.cn/Market/List?page=" + str(i)
        yield url
def get_page_content(url):
    header = {
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
         "Accept-Encoding":"gzip, deflate, sdch",
         "Accept-Language":"zh-CN,zh;q=0.8",
         "Cache-Control":"max-age=0",
         "Connection":"keep-alive",
         "Cookie":"__cfduid=df4d3663c0be2325cdc0f8c26cce606bf1511749701; cf_clearance=1f9ffffece6c15b19a77257c3efdd48af5fd564c-1511749706-31536000; ASP.NET_SessionId=xqrxlc25nb4cdmuuvrr0gj0x; bdshare_firstime=1511749706770; Hm_lvt_8f396c620ee16c3d331cf84fd54feafe=1511749840; Hm_lpvt_8f396c620ee16c3d331cf84fd54feafe=1511749842; safedog-flow-item=; __utmt=1; __utma=247588352.1169809198.1511749707.1511761560.1511764231.4; __utmb=247588352.2.10.1511764231; __utmc=247588352; __utmz=247588352.1511749707.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_eda63048a2a5f2f971045c7b18e63a72=1511749707; Hm_lpvt_eda63048a2a5f2f971045c7b18e63a72=1511765158",
         "Host":"www.vegnet.com.cn",
         "Upgrade-Insecure-Requests":"1",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
            }
    response = requests.get(url, headers=header)
#print(response.content)
    soup = BeautifulSoup(response.content, "lxml")
    frame_list = soup.find_all("div", {"class":"frame_list1"})
#    frame_list2 = soup.find_all("div", {"class":"frame_list1"},{"id":"bj_gra"})
#    print(frame_list)
    page_url = "/Market/30.html"
    for i in range(1, 60):
        bj_url = "http://www.vegnet.com.cn" + page_url + "?page=" + str(i)
#        print(bj_url)
        request = requests.get(bj_url, headers=header)
    #   print(request.content)
        bsobj = BeautifulSoup(request.content, "lxml")
        price_day_items = bsobj.find_all("li", {"tag":"show_1"})
        for item in price_day_items:
            price_item_url= item.a["href"]
            price_url="http://www.vegnet.com.cn"+price_item_url
            response=requests.get(price_url,headers=header)
#            print(response)
            soup_price=BeautifulSoup(response.content,"lxml")
            pri_items=soup_price.find("div",{"class":"pri_k"})
#            print(type(pri_items))
            p_items=pri_items.find_all("p")
            for item in p_items:
                    span=item.find_all("span")
#                    print(span)
                    data=span[0].get_text()
                    name=span[1].get_text()
                    market=span[2].get_text()
                    low_price=span[3].get_text()
                    high_price=span[4].get_text()
                    exp_price=span[5].get_text()
                    unit=span[6].get_text()
                    yield data,name,market,low_price,high_price,exp_price,unit
def write_to_csv():
    urls = get_total_url()
    for url in urls:
#    name, low_price, exp_price, high_price, standard, unit, data, null_index=get_page_content(url)
        with open(r"C:\Users\chen\Desktop\北京新发地农产品数据.csv", "w+", newline="",encoding='utf-8') as file:
            tem = 1
            writer = csv.writer(file)
            writer.writerow(["data","name","market","low_price","high_price","exp_price","unit"])
            for url in urls:
                for data,name,market,low_price,high_price,exp_price,unit in get_page_content(url):
                    market_price = [data,name,market,low_price,high_price,exp_price,unit]
                    writer.writerow(market_price)
                    print("第" + str(tem) + "次写入成功")
                    tem += 1          
            print("写入完毕")     
def main():
    write_to_csv()
if __name__ == '__main__':
    main()

