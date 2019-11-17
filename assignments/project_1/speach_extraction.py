# -*- coding: utf-8 -*-
# @Time : 2019/11/5 11:55 PM 
# @Author : qiujiafa
# @File : speach_extraction.py

import os
import jieba

from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser
from assignments.project_1.const import LTP_TOP_DIR
from assignments.project_1.utils import token, cut, split_sentences


def load_saywords():
    with open('./say_words.txt', 'r', encoding='utf8') as f:
        for line in f:
            say_words = line.split('|')
    return say_words


def extraction_option(text):
    """
    抽取新闻文本中人物，观点
    :param text: 新闻文本
    :return:
    """
    # text = token(text)

    cws_model_path = os.path.join(LTP_TOP_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    # segmentor = Segmentor()  # 初始化实例
    # segmentor.load(cws_model_path)  # 加载模型

    pos_model_path = os.path.join(LTP_TOP_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    ner_model_path = os.path.join(LTP_TOP_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型

    par_model_path = os.path.join(LTP_TOP_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型

    # cut sentences

    sentences = SentenceSplitter.split(text)
    print(f'sentences:{list(sentences)}')
    opnion_results = []
    say_words = load_saywords()

    for sentence in sentences:
        # cut words
        words = cut(sentence)
        # 词性标注
        postags = postagger.postag(words)
        # 命名实体识别
        netags = recognizer.recognize(words, postags)
        # netags = list(netags)
        # 依存句法分析
        arcs = parser.parse(words, postags)

        arcs = [(arc.head, arc.relation) for arc in arcs]

        print(f'words: {list(words)} \npost_tags: {list(postags)}\nnettags: {list(netags)}\narcs:{arcs}')

        # print([(arc.head, arc.relation) for arc in arcs])

        if not [i for i in netags if i in ['S-Nh', 'S-Ni', 'S-Ns']]:
            continue

        hed_index = 0
        for arc in arcs:
            if arc[1] == 'HED':
                break
            hed_index += 1

        print(f"HED: {words[hed_index]}")

        say_word = words[hed_index]
        # if say_word in say_words:

        arcs_new = [(i, arc) for i, arc in enumerate(arcs) if arc[1] == 'SBV']  #SBV 主谓关系 找出主谓关系的句子
        print(arcs_new)

        for arc in arcs_new:
            verb_index = arc[1][0]
            subject = arc[0]
            if words[verb_index - 1] not in say_words:
                continue
            opnion_results.append((words[subject], words[verb_index - 1], ''.join(words[verb_index:])))

        return opnion_results

    postagger.release()
    recognizer.release()
    parser.release()






if __name__ == '__main__':
    docs = '穆罕默德表示，相信苏丹有能力克服目前的困难，实现和平的政治过渡和民族和解。'
    r = extraction_option(docs)
    print(r)
