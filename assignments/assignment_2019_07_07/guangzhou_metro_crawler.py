# -*- coding: utf-8 -*-
# @Time : 2019/7/13 3:47 PM 
# @Author : qiujiafa
# @File : guangzhou_metro_crawler.py

import json
import requests
from collections import defaultdict


url = 'http://map.amap.com/subway/index.html?&1100'

guangzhou_metro_url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=4401_drw_guangzhou.json'

response = requests.get(guangzhou_metro_url)
gz_json = json.loads(response.text)
info = gz_json.get('l')


def get_gz_metro_station_info():
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
        print(line_dict)
        result.append(line_dict)

    return result


if __name__ == '__main__':
    # response = requests.get(url)
    # text = response.text
    # print(text)

    rv = get_gz_metro_station_info()
    print(rv)