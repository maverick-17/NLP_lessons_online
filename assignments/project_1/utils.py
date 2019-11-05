# -*- coding: utf-8 -*-
# @Time : 2019/11/3 11:06 AM 
# @Author : qiujiafa
# @File : utils.py

import os
import re
import jieba
import logging
import datetime
import functools


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        rv = func(*args, **kwargs)
        duration = datetime.datetime.now() - start
        logging.info(f'==== calling {func.__name__} taken {duration} ====')
        return rv

    return wrapper


class MySentences(object):
    """
    定义一个有迭代器方法的 sentences 类 在语料较大时可以 memory-friendly
    输入文件夹，其下有多个已分词的语料文件
    """
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for file in os.listdir(self.dirname):
            if file == 'AL_wiki_80_new':
                continue
            with open(os.path.join(self.dirname, file), encoding='utf-8', errors='ignore') as f:
                for line in f:
                    yield line


def token(string):
    if not string:
        return None
    return re.findall('[\d|\w|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|'
                      '\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|'
                      '\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]+', string)

    # return re.findall(r'[\d|\w]+', string.replace('\\n', ''))


def cut(string):
    return [w for w in jieba.cut(string)]


if __name__ == '__main__':
    s = '我是一个中国人;&*)\n是的'
    s1 = token(s)
    print(s1)