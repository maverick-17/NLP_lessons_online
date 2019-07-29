# -*- coding: utf-8 -*-
# @Time : 2019/7/13 3:47 PM 
# @Author : qiujiafa
# @File : guangzhou_metro_crawler.py

import json
import requests
import matplotlib.pyplot as plt
from collections import defaultdict


# 偷懒了 使用高德地图 api 拿到广州地铁线路图的站点及坐标
url = 'http://map.amap.com/subway/index.html?&1100'

guangzhou_metro_url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=4401_drw_guangzhou.json'

response = requests.get(guangzhou_metro_url)
gz_json = json.loads(response.text)
info = gz_json.get('l')


def get_gz_metro_station_info():
    """ 拿到广州地铁每条线的站点和坐标 """
    result = []
    for line in info:
        line_dict = defaultdict(list)
        line_name = line['ln']
        for st in line['st']:
            item = {}
            station = st['n']
            postions = tuple(float(k) for k in st['sl'].split(','))
            #         print(station, postions)
            item[station] = postions

            line_dict[line_name].append(item)
        # print(line_dict)
        result.append(line_dict)

    return result


def get_gz_metro_all_postitions():
    gz_metro_info = get_gz_metro_station_info()
    gz_all_st_pos = {}
    for item in gz_metro_info:
        for line in item:
            #         print(item[line])
            for st in item[line]:
                for st_name, pos in st.items():
                    if st_name in gz_all_st_pos: continue
                    gz_all_st_pos[st_name] = pos
    print(gz_all_st_pos)
    return gz_all_st_pos






# gz_metro_info = get_gz_metro_station_info(guangzhou_metro_url)


if __name__ == '__main__':
    # response = requests.get(url)
    # text = response.text
    # print(text)

    rv = get_gz_metro_all_postitions()
    print(rv)