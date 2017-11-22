'''
Created on 2017-11-22

@author: chen
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import request
def get_content():
    url = "http://www.xicidaili.com/nn/"
    for i in range(1,100):
        url_encode = url + str(i)
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
        response=request.Request(url=url_encode, headers=headers)
        html = urlopen(response).read().decode("utf-8")
        soup = BeautifulSoup(html, "lxml")
#        print(soup)
        ip_list = soup.find("table", {"id":"ip_list"})
        ip_items = ip_list.find_all("tr")
        for item in ip_items:
            item_td=item.find_all("td")
            if len(item_td)==10:
                ip_address=item_td[1].get_text()
                port=item_td[2].get_text()
                server_address=item_td[3].get_text().strip()
                speed=item_td[6].div["title"]
                connect_time=item_td[7].div["title"]
                survival_time=item_td[8].get_text()
                if round(float(speed[0:-2]))<1:
                    print(port,ip_address)
                
        
def main():
    get_content()
if __name__ == '__main__':
    main()
