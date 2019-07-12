#!/usr/bin/python
# -*- coding:utf-8 -*-
# author::ZHT 19-07-09
# 通过分析得到的，m 网址里面的json数据，也会监测到不能爬

import random
import re
import time
import pymysql
import requests

# CREATE TABLE `wiwj_sh_zufang` (
#   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `house_id` char(16) NOT NULL,
#   `house_url` varchar(127) NOT NULL,
#   `house_jpg` varchar(512) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '封面图',
#   `house_title` varchar(512) CHARACTER SET utf8mb4 NOT NULL,
#   `house_type` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
#   `house_buildarea` varchar(64) CHARACTER SET utf8mb4 NOT NULL,
#   `house_heading` varchar(16) CHARACTER SET utf8mb4 NOT NULL,
#   `house_floor` varchar(128) CHARACTER SET utf8mb4 NOT NULL,
#   `house_decoratelevel` varchar(128) CHARACTER SET utf8mb4 NOT NULL,
#   `house_place` varchar(512) CHARACTER SET utf8mb4 NOT NULL,
#   `house_firstuptime` varchar(128) CHARACTER SET utf8mb4 NOT NULL,
#   `house_price` int(16) NOT NULL,
#   `house_renttype` varchar(16) CHARACTER SET utf8mb4 NOT NULL,
#   `house_paytype` varchar(16) CHARACTER SET utf8mb4 NOT NULL,
#   `house_area` varchar(32) CHARACTER SET utf8mb4 NOT NULL,
#   `house_tags` varchar(512) CHARACTER SET utf8mb4 NOT NULL,
#   `house_subwaylines` varchar(512) CHARACTER SET utf8mb4 NOT NULL,
#   `house_traffic` varchar(512) CHARACTER SET utf8mb4 NOT NULL,
#   `house_quality` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `houseid` (`house_id`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=2671 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


class Wiwj(object):
    def __init__(self):
        """
        13014 按每页30个 共有434页
        """
        self.start_url = 'https://m.5i5j.com/hz/zufang/index-n{}'
        # self.start_url = 'https://m.5i5j.com/hz/ershoufang/index-n{}'
        # 只添加'x-requested-with' 可能获取不到json数据，可以直接把整个请求头加上
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': '',
            'pragma': 'no-cache',
            # 'referer': 'https://m.5i5j.com/hz/zufang/index',
            # 'referer': 'https://m.5i5j.com/hz/ershoufang/index',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    def gethouselist(self):
        """ 5i5j 杭州租房 """
        for page in range(46, 435):
            print("-----------------------" + str(page) + "------------------")
            r = requests.get(self.start_url.format(page), headers=self.headers)
            result = r.json()
            houses = result['houses']
            # print(r.json())
            for i in range(0, len(houses)):
                # print(houses[i]['_source']['housesid'])
                house_id = houses[i]['_source']['housesid']
                house_url = 'https://m.5i5j.com/hz/zufang/{}.html'.format(
                    houses[i]['_source']['housesid'])
                house_jpg = houses[i]['_source']['imgurl']
                house_title = houses[i]['_source']['housetitle']
                house_type = houses[i]['_source']['bedroom_cn'] + \
                    houses[i]['_source']['livingroom_cn'] + \
                    houses[i]['_source']['toilet_cn']
                house_buildarea = houses[i]['_source']['area']
                house_heading = houses[i]['_source']['heading']
                house_floor = houses[i]['_source']['floorPositionStr'] + \
                    '/' + str(houses[i]['_source']['houseallfloor'])
                house_decoratelevel = houses[i]['_source']['decoratelevel']
                house_place = str(houses[i]['_source']['sqname']) + \
                    ' ' + str(houses[i]['_source']['communityname'])
                house_firstuptime = houses[i]['_source']['firstuptimestr']
                house_price = houses[i]['_source']['price']
                house_renttype = houses[i]['_source']['rentmodename']
                house_paytype = houses[i]['_source']['pay']
                house_area = houses[i]['_source']['qyname']
                house_tag = houses[i]['_source']['tagwall']
                house_tags = ','.join(house_tag)
                house_subwayline = houses[i]['_source']['subwaylines']
                house_subwaylines = ','.join(house_subwayline)
                house_traffic = houses[i]['_source']['traffic']
                house_quality = houses[i]['_source']['house_quality']
                # print(house_id, house_url, house_jpg, house_title, house_type, house_buildarea, house_heading,
                #       house_floor, house_decoratelevel, house_place, house_firstuptime, house_price, house_renttype,
                #       house_paytype, house_area, house_tags, house_subwaylines, house_traffic, house_quality)
                self.insertmysql(house_id, house_url, house_jpg, house_title, house_type, house_buildarea, house_heading,
                                 house_floor, house_decoratelevel, house_place, house_firstuptime, house_price, house_renttype,
                                 house_paytype, house_area, house_tags, house_subwaylines, house_traffic, house_quality)
            time.sleep(random.randint(0, 5))

    @staticmethod
    def insertmysql(house_id, house_url, house_jpg, house_title, house_type, house_buildarea, house_heading,
                    house_floor, house_decoratelevel, house_place, house_firstuptime, house_price, house_renttype,
                    house_paytype, house_area, house_tags, house_subwaylines, house_traffic, house_quality):
        conn = pymysql.connect(host='localhost', port=3306,
                               user='root', passwd='erb356wer', db='hose_db')
        cursor = conn.cursor()

        insert_sql = "insert into `wiwj_hz` (`house_id`, `house_url`, `house_jpg`, `house_title`, `house_type`, `house_buildarea`, `house_heading`, `house_floor`, `house_decoratelevel`,`house_place`, `house_firstuptime`, `house_price`, `house_renttype`, `house_paytype`, `house_area`, `house_tags`, `house_subwaylines`,`house_traffic`, `house_quality`, `type`)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s',1)" % (house_id, house_url, house_jpg, house_title, house_type, house_buildarea, house_heading,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      house_floor, house_decoratelevel, house_place, house_firstuptime, house_price, house_renttype, house_paytype,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      house_area, house_tags, house_subwaylines, house_traffic, house_quality)
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


if __name__ == '__main__':
    """ 杭州 """
    wiwj = Wiwj()
    wiwj.gethouselist()
