'''
Created on 2017-11-27

@author: chen
'''
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup 
def get_total_page_url():
    for i in range(1, 30):
        url = "http://www.vegnet.com.cn/Market/List?page=" + str(i)
        yield url
def page_content(url):
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    response=request.Request("http://www.vegnet.com.cn/Market/List?page=1",headers=head)
    contents = urlopen(response).read()
    soup = BeautifulSoup(contents,"lxml")
    frame_list1=soup.find("div", {"class":"gre_k"})
    print(frame_list1)
def main():
    for url in  get_total_page_url():
        print(url)
        page_content(url)
if __name__ == '__main__':
    main()
    
