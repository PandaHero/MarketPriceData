'''
Created on 2017-11-22

@author: chen
'''
import random
import re
import subprocess as sp
def get_proxys():
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
                ip_port[ip_address] = port
    return ip_port   
"""
函数说明:检查代理IP的连通性
Parameters:
    ip - 代理的ip地址
    lose_time - 匹配丢包数
    waste_time - 匹配平均时间
Returns:
    average_time - 代理ip平均耗时
Modify:
    2017-05-27
"""
def check_ip(ip, lose_time, waste_time):
    #命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = "ping -n 3 -w 3 %s"
    #执行命令
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    #获得返回结果并解码
    out = p.stdout.read().decode("gbk")
    #丢包数
    lose_time = lose_time.findall(out)
    #当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    #如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose > 2:
        #返回False
        return 1000
    #如果丢包数目小于等于2个,获取平均耗时的时间
    else:
        #平均时间
        average = waste_time.findall(out)
        #当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(average) == 0:
            return 1000
        else:
            #
            average_time = int(average[0])
            #返回平均耗时
            return average_time

"""
函数说明:初始化正则表达式
Parameters:
    无
Returns:
    lose_time - 匹配丢包数
    waste_time - 匹配平均时间
Modify:
    2017-05-27
"""
def initpattern():
    #匹配丢包数
    lose_time = re.compile("丢失 = (\d+)")
    #匹配平均时间
    waste_time = re.compile("平均 = (\d+)ms")
    return lose_time, waste_time

if __name__ == '__main__':
    #初始化正则表达式
    lose_time, waste_time = initpattern()
    #获取IP代理
    proxys_list = get_proxys()

    #如果平均时间超过200ms重新选取ip
    while True:
        #从100个IP中随机选取一个IP作为代理进行访问
        proxy = random.choice(proxys_list)
        ip = proxy.getValue()
        
        #检查ip
        average_time = check_ip(ip, lose_time, waste_time)
        if average_time > 200:
            #去掉不能使用的IP
            proxys_list.remove(proxy)
            print("ip连接超时, 重新获取中!")
        if average_time < 200:
            break

    #去掉已经使用的IP
    proxys_list.remove(proxy)
    
    print("使用代理:", proxys_list)
