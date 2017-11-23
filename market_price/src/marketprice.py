'''
Created on 2017-11-22

@author: chen
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import time
import urllib.request
#from urllib import request
#from urllib.parse import urlencode
def get_total_page_num():
    for i in range(1, 13690):
        url = "http://www.xinfadi.com.cn/marketanalysis/0/list/" + str(i) + ".shtml"
        yield url
def get_ip_content():
    url = "http://www.xicidaili.com/nn/"
    for i in range(1, 100):
        url_encode = url + str(i)
#        response = request.Request(url=url_encode, headers=headers)
#        创建ProxyHandler
        proxy_support = urllib.request.ProxyHandler({"8123":"171.37.157.235", "8123":"110.73.35.183", "21075":"180.122.144.253", "8123":"110.73.33.89", "8118":"106.85.203.139", "8123":"110.73.155.90"})
#        创建opener
        opener = urllib.request.build_opener(proxy_support)
#        添加user-agent
        handlers = [("User-Agent", "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/171.37.157.235 Mobile Safari/535.19")]
        opener.add_handlers = handlers
#        安装opener
        urllib.request.install_opener(opener)
        html = urlopen(url_encode).read().decode("utf-8")
        soup = BeautifulSoup(html, "lxml")
#        print(soup)
        ip_list = soup.find("table", {"id":"ip_list"})
        ip_items = ip_list.find_all("tr")
        for item in ip_items:
            item_td = item.find_all("td")
            if len(item_td) == 10:
                ip_address = item_td[1].get_text()
                port = item_td[2].get_text()
#                server_address = item_td[3].get_text().strip()
                speed = item_td[6].div["title"]
#                connect_time = item_td[7].div["title"]
                survival_time = item_td[8].get_text()
                if round(float(speed[0:-2])) < 1 and ((survival_time[-1:-2]) == "天" and round(float(survival_time[0:-2])) > 1):
                    print(port, ip_address)
#提取网页中的ip地址和端口号信息
def get_ip_port():
    ip_port = {}
    with open(r"C:\Users\chen\Desktop\新建文本文档.txt" , "r+") as f:
        lines = f.readlines()
        for line in lines:
#        print(line)
            if "IP地址" in line:
                ip_address = line[line.index(":") + 1:-1]
#            print(ip_address)
            elif "端口" in line:
                port = line[line.index(":") + 1:-1]
#            print(port)
                ip_port[str(port)] = str(ip_address)
    return ip_port
#验证代理ip的有效性
def verif_ip(ip, port):    # 验证ip有效性
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360EE'
    headers = {'User-Agent':user_agent}
    proxy = {'http':'http://%s:%s' % (ip, port)}
#    print(proxy)
    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
#    测试网址（百度）
    test_url = "https://www.baidu.com/"
    req = urllib.request.Request(url=test_url, headers=headers)
    try:
        res = urllib.request.urlopen(req)
#        time.sleep(3)
        content = res.read()
        if content:
#            print('that is ok')
#            with open(r"C:\Users\chen\Desktop\data2.txt", "a") as fd:       # 有效ip保存到data2文件夹
#                fd.write(ip + ":" + port)
#                fd.write("\n")
            return ip, port 
        else:
            return None
            
    except urllib.request.URLError as e:
        print(e.reason)
    
def get_page_content(url, ip, port):
        proxy_support = urllib.request.ProxyHandler({ip:port})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        html = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html, "lxml")
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
    url = get_total_page_num()
#    name, low_price, exp_price, high_price, standard, unit, data, null_index=get_page_content(url)
    with open(r"C:\Users\chen\Desktop\北京新发地农产品数据.csv", "w+", newline="") as file:
        tem = 1
        writer = csv.writer(file)
        writer.writerow(["name", "low_price", "exp_price", "high_price", "standard", "unit", "data", "null_index"])
        ip_port = get_ip_port()
        for each_url in url:
            for ip , port in ip_port.items():
                print(ip,port)
                if verif_ip(ip, port)==None:
                    ip, port = verif_ip(ip, port)
                else:
                    ip, port = verif_ip(ip, port)
                    print(ip+":"+port)
                    for name, low_price, exp_price, high_price, standard, unit, data, null_index in get_page_content(each_url,ip, port):
                        market_price = [name, low_price, exp_price, high_price, standard, unit, data, null_index]
                        writer.writerow(market_price)
                        print("第" + str(tem) + "次写入成功")
                        tem += 1
                    
                print("写入完毕") 
        
        
def main():
    write_to_csv()
#    get_ip_content()
if __name__ == '__main__':
    main()
    
