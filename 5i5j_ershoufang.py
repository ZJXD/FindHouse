# Findhouse
# -*- coding:utf-8 -*-
# author::ZHT 19-07-09
# 通过 lxml 爬取我爱我家 二手房数据

import requests
import csv
from lxml import etree
import pymysql
import time
import random

# 创建我爱我家类


class Woaiwojia:
    # 创建页面获取函数
    def get_page(self, url):
        self.url = url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
            'Cookie': 'yfx_c_g_u_id_10000001=_ck19022116084813839206365574151; _ga=GA1.2.172982220.1550736528; ershoufang_BROWSES=41857749%2C42331571; _gid=GA1.2.1753629442.1551407389; _Jo0OQK=3C360A430707C39DC66841396A856BB9F1CDAFCCCBE5DD3EF55A648ADA5CBA77AEE43F896CA59E44D089FA0454846BD97D221FB8F73A12B808A197E69B45975E9E5C57212F12283777C840763663251ADEB840763663251ADEB8B9BB377FBE15866A593CD374DB85252GJ1Z1dg==; PHPSESSID=plv3sri11n4ivdfekjgjrl0qme; domain=bj; yfx_f_l_v_t_10000001=f_t_1550736528365__r_t_1551407385571__v_t_1551423063129__r_c_2; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1550824470,1551407393,1551407583,1551423064; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1551423064'
        }
        response = requests.get(self.url, headers=headers)
        return response.text

    # 创建解析函数
    def parse_page(self, url):
        self.url = url
        selector = etree.HTML(self.get_page(self.url))
        items = selector.xpath('/html/body/div[4]/div[1]/div[2]/ul/li')
        for item in items:
            url = item.xpath('./div[2]/h3/a/@href')[0]
            house_id = url[12:-5]
            house_url = url
            house_title = item.xpath('./div[2]/h3/a/text()')[0]
            style = item.xpath('./div[2]/div[1]/p[1]/text()')[0].split('·')
            house_type = style[0].strip()
            house_buildarea = style[1].strip()[:-3]
            house_heading = style[2].strip()
            house_floor = style[3].strip()
            house_decoratelevel = style[4].strip()
            house_place = item.xpath('./div[2]/div[1]/p[2]/a/text()')[0]
            house_firstuptime = item.xpath(
                './div[2]/div[1]/p[3]/text()')[0].split('·')[2][:-2]
            house_price = item.xpath(
                './div[2]/div[1]/div/p[2]/text()')[0][2:-4]
            house_total_price = item.xpath(
                './div[2]/div[1]/div/p[1]/strong/text()')[0]
            # info = [name, style, place, price, total_price]
            # self.csv_info(info)
            self.insertmysql(house_id, house_url, house_title, house_type, house_buildarea, house_heading,
                             house_floor, house_decoratelevel, house_place, house_firstuptime, house_price,
                             house_total_price)
            time.sleep(random.randint(0, 5))

    # 创建保存函数

    def csv_info(self, content):
        with open('info-1.csv', 'a', encoding='utf-8', newline='')as file:
            write = csv.writer(file)
            write.writerow(content)

    @staticmethod
    def insertmysql(house_id, house_url, house_title, house_type, house_buildarea, house_heading,
                    house_floor, house_decoratelevel, house_place, house_firstuptime, house_price,
                    house_total_price):
        conn = pymysql.connect(host='localhost', port=3306,
                               user='root', passwd='erb356wer', db='hose_db')
        cursor = conn.cursor()

        insert_sql = "insert into `wiwj_hz` (`house_id`, `house_url`, `house_title`, `house_type`, `house_buildarea`, `house_heading`, `house_floor`, `house_decoratelevel`,`house_place`, `house_firstuptime`, `house_price`, `house_total_price`, `type`)values('%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s',2)" % (house_id, house_url, house_title, house_type, house_buildarea, house_heading,
                                                                                                                                                                                                                                                                                                                                      house_floor, house_decoratelevel, house_place, house_firstuptime, house_price,
                                                                                                                                                                                                                                                                                                                                      house_total_price)
        select_sql = "select `house_id` from `wiwj_hz` where `house_id`='%s'" % house_id

        try:
            response = cursor.execute(select_sql)
            conn.commit()
            if response == 1:
                print(u'该房源存在...')
            else:
                try:
                    cursor.execute(insert_sql)
                    conn.commit()
                    print(u'房源插入成功...')
                except Exception as e:
                    print(u'房源插入错误...', e)
                    conn.rollback()
        except Exception as e:
            print(u'查询错误...', e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


# 调用运行
if __name__ == '__main__':
    k = Woaiwojia()
    # title = ['名称', '户型', '地区', '售价', '总价/万']
    # k.csv_info(title)
    for x in range(1, 100):
        print("-----------------------" + str(x) + "------------------")
        url = 'https://hz.5i5j.com/ershoufang/n%s/' % x
        k.parse_page(url)
