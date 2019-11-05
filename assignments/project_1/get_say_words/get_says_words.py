# -*- coding: utf-8 -*-
# @Time : 2019/10/24 8:07 AM
# @Author : qiujiafa
# @File : wiki_word_to_vector.py

"""
用 wiki 百科 及新闻语料 训练词向量 并得到所有与 '说' 相义的词
"""

import logging
import pandas as pd
import re
import os
import jieba
import datetime

from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim.models import word2vec

from assignments.project_1.utils import timeit, MySentences, token, cut

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

WIKI_DIR = '/Users/qiujiafa/lesson/wikiextractor-master'

# 预先分词后的维基百科文件
WIKI_DIR_CUTTED = '/Users/qiujiafa/lesson/wikiextractor-master/wikipedia_extracted_new'

# 新闻语料
NEWS_PATH = '/Users/qiujiafa/lesson/data/news_chinese_dumpload.csv'


say_words = ['答道', '质问', '声称', '还称', '责备', '提问', '说', '曼说', '责问', '写道', '既然', '询问', '真是', '难道',
             '怎会', '中称', '问道', '中说', '地称', '问起', '地问', '说道', '何况', '愚蠢', '说出', '谈到', '怎么', '却说',
             '喊道', '感叹', '上称', '听说', '发问', '问', '吗', '反问', '恐怕', '回答', '埋怨', '怎能', '在我看来', '觉得',
             '答', '呢', '他称', '中写', '地说', '怎', '文说', '确信', '时说', '文中说']


@timeit
def get_wiki_corpus():
    for file_path, _, file_list in os.walk(WIKI_DIR_CUTTED):
        #  拿部分文件做模型训练测试
        corpus = []
        for file in file_list[:100]:
            sentences = word2vec.LineSentence(datapath(os.path.join(WIKI_DIR_CUTTED, file)))
            for sentence in sentences:
                corpus.append(sentence)
    return corpus


@timeit
def train_wiki_word2vec():
    " 用 wiki 百科语料训练模型"
    sentences = MySentences(WIKI_DIR_CUTTED)
    wiki_model = Word2Vec(sentences=sentences,
                          size=100,
                          window=20,
                          min_count=10,
                          workers=4
                          )

    wiki_model.save('./word2vec_model/wiki_word2cev.model')


@timeit
def train_with_news():
    news_df = pd.read_csv(NEWS_PATH)
    content = news_df['content'].to_list()
    print(len(content))
    print(content[0])
    content = [token(str(i)) for i in content]
    corpus = []
    for news in content:
        for sentence in news:
            corpus.append(cut(sentence))

    model = Word2Vec.load('./word2vec_model/wiki_word2cev.model')
    model.train(sentences=corpus, total_examples=1, epochs=1)
    # model.save('./word2vec_model/wiki_word2cev.model')


def get_similar_word(word, model):
    model = Word2Vec.load(model)
    similar_words = model.wv.most_similar([word])
    return similar_words


if __name__ == '__main__':

    # corpus = get_wiki_corpus()
    # print(corpus)
    # train_wiki_word2vec()
    model = './word2vec_model/wiki_word2cev.model'
    say_words = get_similar_word('小米', model)
    print(say_words)
    # say_words = [i[0] for i in (get_similar_word('说', model))]
    # words = []
    # for w in say_words:
    #     word_similar = [i[0] for i in (get_similar_word(w, model))]
    #     words.extend(word_similar)
    # words = list(set(words))
    # print(words)
    # train_with_news()






