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

from pyltp import SentenceSplitter, Postagger, NamedEntityRecognizer, Parser
from assignments.project_1.const import LTP_TOP_DIR


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
    tokens = re.findall('[\d|\w|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|'
                      '\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|'
                      '\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]+', string)
    return ' '.join(tokens)


def split_sentences(string):
    sentences = SentenceSplitter.split(string)
    return [s for s in sentences if len(s) > 0]


def cut(string):
    return [w for w in jieba.cut(string)]


def get_postags(words):
    """
    get ltp 词性标注结果
    :param words: word list
    :return: postags
    """
    pos_model_path = os.path.join(LTP_TOP_DIR, 'pos.model')
    postgger = Postagger()
    postgger.load(pos_model_path)

    postags = postgger.postag(words)
    postgger.release()
    return [p for p in postags]


def get_ner(words, postags):
    """ ltp 命名实体识别 """
    ner_model_path = os.path.join(LTP_TOP_DIR, 'ner.model')
    recognizer = NamedEntityRecognizer()
    recognizer.load(ner_model_path)
    netags = recognizer.recognize(words, postags)
    recognizer.release()
    return list(netags)


def parse_arcs(words, postags):
    """ ltp 依存句法分析 """
    parser_model_path = os.path.join(LTP_TOP_DIR, 'parser.model')
    parser = Parser()
    parser.load(parser_model_path)

    arcs = parser.parse(words, postags)
    parser.release()
    # return arcs
    return [(arc.head, arc.relation) for arc in arcs]


if __name__ == '__main__':
    s_test = '本场梅西5次射门全部打正，并且收获3球，两次传球形成射门。苏亚雷斯说他都惊呆了'
    s = '军事委员会主席阿卜杜勒·法塔赫·布尔汉时表示，阿联酋将支持苏丹为维护国家安全和稳定所做出的努力，并呼吁各方通过对话实现民族和解。据阿联酋通讯社报道，穆罕默德表示，相信苏丹有能力克服目前的困难，实现和平的政治过渡和民族和解。'

    # s1 = token(s)
    # print(s1)
    sentencs = split_sentences(s)
    print(sentencs)
    words = [cut(s) for s in sentencs]
    print(words)
    postags = [get_postags(w) for w in words]
    print(postags)
    nes = [get_ner(w, p) for w, p in zip(words, postags)]
    print(nes)

    arcs = [parse_arcs(w, p) for w, p in zip(words, postags)]
    print(arcs)
    # import pdb
    # pdb.set_trace()



