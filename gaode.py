# coding:utf-8

from urllib import parse
import csv
from bs4 import BeautifulSoup
import requests

# 项目步骤：
    #1、找到一个目标URL
    #2、分析html页面，获取html页面
    #3、进行所需内容匹配
    #4、文件操作 写入CSV文件

URL = "http://hz.ganji.com/fang1/m1p3/o{page}"
ADDR = "http://hz.ganji.com"

start_page = 0
end_page = 20

with open("foo_1.csv","w",newline = '') as f:
    csv_writer = csv.writer(f,delimiter = ',')
    print("start……")

    while start_page < end_page:
        start_page += 1
        response = requests.get(URL.format(page = start_page))
        html = BeautifulSoup(response.text,"html.parser")
        house_list = html.select(".f-list > .f-list-item > .f-list-item-wrap")
        if not house_list:
            break
        for house in house_list:
            house_title = house.select(".title > .js-title")[0].string
            house_url = parse.urljoin(ADDR, house.select(".title > .js-title")[0].get("href"))
            house_addr = house.select(".address > .area > .address-eara")[-1].string
            house_price = house.select(".info > .price > .num")[0].string
            csv_writer.writerow([house_title,house_addr,house_price,house_url])
        print (start_page)
    print("end……")
