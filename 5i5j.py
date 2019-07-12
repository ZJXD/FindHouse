# coding:utf-8
# 爬取 我爱我家 租房信息，该方式已经不可用

from urllib import parse
from urllib import request
import csv
from bs4 import BeautifulSoup
import requests
import sys

# 设置编码
# reload(sys)
# sys.setdefaultencoding('utf-8')

sys_type = sys.getdefaultencoding()


# 项目步骤：
# 1、找到一个目标URL
# 2、分析html页面，获取html页面
# 3、进行所需内容匹配
# 4、文件操作 写入CSV文件

URL = "https://hz.5i5j.com/zufang/r2n{page}/"
ADDR = "http://hz.5i5j.com"

start_page = 1
end_page = 10

with open("5i5j_xihu.txt", "w") as f:
    print("start……")

    while start_page < end_page:
        start_page += 1
        #response = requests.get(URL.format(page = start_page))
        # response = request.urlopen(URL.format(page=start_page))
        response = requests.get("https: // hz.5i5j.com/zufang/r2n1/")
        a = response.read().decode('utf-8').encode(sys_type)
        html = BeautifulSoup(a, "html.parser")
        house_list = html.select(".list-body > .list-body > li > .list-info")
        if not house_list:
            break
        for house in house_list:
            house_title = house.select("h2 > a")[0].string
            house_url = parse.urljoin(
                ADDR, house.select("h2 > a")[0].get("href"))
            house_addr = house.select(".list-info-l > li > a > h3")[0].string
            house_price = house.select(".list-info-r > h3")[0].string
            # print(house_price)
            f.write(str(house_title).replace(u'\xa0', '')+','+str(house_addr).replace(
                u'\xa0', '')+','+str(house_price)+','+str(house_url)+'\n')
        print(start_page)
    print("end……")
