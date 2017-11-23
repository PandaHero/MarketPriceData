#网站反爬虫：一个IP频繁访问就先将该IP加入黑名单
#反爬虫策略：限制IP访问频率，超过频率就自动断开：降低爬虫的速度，在每个请求前加time.sleep,或更换IP
#策略二：后台对访问进行统计，如果单个userAgent访问超过阈值，予以封锁：误伤较大，一般网站不使用
#策略三：针对cookies：一般网站不使用

from bs4 import BeautifulSoup
import csv
import random
import re
import requests
import time

#首先，我们找一个发布代理IP的网站，从该网站爬取代理IP来访问网页，当本地IP失效，启用代理IP

class Download(object):
    def __init__(self):
        self.ip_list = []
        with open(r"C:\Users\chen\Desktop\新建文本文档.txt" , "r+") as f:
            lines = f.readlines()
        for line in lines:
#        print(line)
            if "IP地址" in line:
                ip_address = line[line.index(":") + 1:-1]
                self.ip_list.append(ip_address)
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def get(self, url, timeout, proxy=None, num_retries=6):
        ua = random.choice(self.user_agent_list)   #从user_agent_list中随机抽取出一个字符串
        # print(ua)
        header = {"User-Agent":ua}  #构造一个完整的User_Agent

        if proxy == None:    #当代理为空时，不使用代理获取response
            try:
                response = requests.get(url, headers=header, timeout=timeout)
                return response
            except:
                if num_retries > 0:
                    time.sleep(10)
                    print("获取网页错误，10s后将获取倒数第：", num_retries, "次")
                    return self.get(url, timeout, num_retries - 1)  #调用自身并将次数减1
                else:
                    print("开始使用代理")
                    time.sleep(10)
                    IP = "".join(str(random.choice(self.ip_list)).strip())
                    proxy = {"http":IP}
                    return self.get(url, timeout, proxy)

        else:
            try:
                IP = "".join(str(random.choice(self.ip_list)).strip())   #随机取IP并去除空格
                proxy = {"http":IP}   #构造一个代理
                response = requests.get(url, headers=header, proxies=proxy, timeout=timeout)  #使用代理来获取response
                return response
            except:
                if num_retries > 0:
                    time.sleep(10)
                    IP = "".join(str(random.choice(self.ip_list)).strip())
                    print("正在更换代理，10s后将重新获取第", num_retries, "次")
                    print("当前代理是：", proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print("代理发生错误，取消代理")
                    return self.get(url, 3)

request = Download();
def get_total_page_num():
    for i in range(9982, 13691):
        url = "http://www.xinfadi.com.cn/marketanalysis/0/list/" + str(i) + ".shtml"
        yield url
def get_page_content(url):
        html=request.get(url,3)
        print(url)
        soup = BeautifulSoup(html.content, "lxml")
        market_contents = soup.find("table", {"class":"hq_table"})
        items_2 = market_contents.find_all("tr")
        items_2.remove(items_2[0])
        for item in items_2:
            item_td = item.find_all("td")
            name = item_td[0].get_text()
            low_price = item_td[1].get_text()
            exp_price = item_td[2].get_text()
            high_price = item_td[3].get_text()
            standard = item_td[4].get_text()
            unit = item_td[5].get_text()
            data = item_td[6].get_text()
            null_index = item_td[7].get_text()
            yield name, low_price, exp_price, high_price, standard, unit, data, null_index       
def write_to_csv():
    urls = get_total_page_num()
#    name, low_price, exp_price, high_price, standard, unit, data, null_index=get_page_content(url)
    with open(r"C:\Users\chen\Desktop\北京新发地农产品数据.csv", "w+", newline="") as file:
        tem = 1
        writer = csv.writer(file)
        writer.writerow(["name", "low_price", "exp_price", "high_price", "standard", "unit", "data", "null_index"])
        for url in urls:
            for name, low_price, exp_price, high_price, standard, unit, data, null_index in get_page_content(url):
                market_price = [name, low_price, exp_price, high_price, standard, unit, data, null_index]
                writer.writerow(market_price)
                print("第" + str(tem) + "次写入成功")
                tem += 1          
        print("写入完毕") 
def main():
    write_to_csv()
if __name__ == '__main__':
    main()
