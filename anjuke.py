# coding:utf-8

from urllib import parse
from urllib import request
import csv
from bs4 import BeautifulSoup
import requests
import sys

# 设置编码
#reload(sys)
#sys.setdefaultencoding('utf-8')

sys_type = sys.getdefaultencoding()


# 项目步骤：
    #1、找到一个目标URL
    #2、分析html页面，获取html页面
    #3、进行所需内容匹配
    #4、文件操作 写入CSV文件

URL = "https://hz.zu.anjuke.com/fangyuan/yuhang/fx1-p{page}/"
ADDR = "https://hz.zu.anjuke.com"

start_page = 0
end_page = 10

with open("anjuke.txt","w") as f:
    print("start……")

    while start_page < end_page:
        start_page += 1
        response = requests.get(URL.format(page = start_page))
        html = BeautifulSoup(response,"html.parser")
        house_list = html.select(".maincontent > .list-content > .zu-itemmod")
        if not house_list:
            break
        for house in house_list:
            house_title = house.select(".zu-info > .h3 > a")[0].string
            house_url = house.select(".zu-info > .h3 > a")[0].get("href")
            house_addr = house.select(".zu-info > .details-item > a")[0].string
            house_price = house.select(".zu-info > .zu-side > p > strong")[0].string
            #print(house_price)
            f.write(str(house_title).replace(u'\xa0','')+','+str(house_addr).replace(u'\xa0','')+','+str(house_price)+','+str(house_url)+'\n')
        print (start_page)
    print("end……")
