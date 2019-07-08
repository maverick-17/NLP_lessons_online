# NLP lesson_1 2019-06-30 运用语法树生成语言 并使用 2-gram 语言模型判断句子的出现概率

# -*- coding: utf-8 -*-

import random

movie_comment_file = './data/movie_comments.csv'

# grammers as follow

HOST = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = null
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？
"""

# my grammer about zoo story
ZOO_STORY = '''
zoo_story = 场景 动物 称谓 连词 动物 称谓 状语 动词
场景 = 在一个 怎样的 时间 | 在一个 怎样的 地点
怎样的 = 阳光明媚的 | 万物复苏的 | 令人陶醉的 | 伸手不见五指的 | 大雨滂沱的
时间 = 夜晚 | 清晨 | 春天 | 秋天 | 冬天 | 中午 | 傍晚
地点 = 湖边 | 森林 | 草地 | 草原 | 山丘 | 公路 | 田野
动物 = 熊 | 鸭 | 鸡 | 鹅 | 大象 | 老虎 | 企鹅 | 松鼠 | 蟑螂 | 屎壳郎 | 海豹
称谓 = 老哥 | 老弟 | 小哥 | 小弟 | 爸爸 | 上校 | 小偷 | 强盗 | 警察 | 护士 | 医生 | 将军 | 间谍
连词 = 和 | 带着 | 与 | 正与
状语 = 快乐地 | 痛苦地 | 和谐地 | 捉急地 | 幸福地 | 尴尬地 | 仿佛没人似的 
动词 = 拥抱着 | 生活着 | 打滚 | 做饭 | 晒衣服 | 斗地主 | 打游戏
'''


def create_grammer(grammer_str, split='=>', line_split='\n'):
    # 将定义的 grammer 结构化
    grammer = {}
    for line in grammer_str.split(line_split):
        if not line.strip(): continue
        exp, stmt = line.split(split)
        grammer[exp.strip()] = [i.split() for i in stmt.split('|')]
    return grammer


def generate_sentence_with_grammer(grammer, target):
    choice = random.choice
    if target not in grammer:
        return target

    expand = [generate_sentence_with_grammer(grammer, t) for t in choice(grammer[target])]
    return ''.join(expand)


def generate_many_sentence(grammer_str, split='=>', line_split='\n', target='zoo_story', number=3):
    grammer = create_grammer(grammer_str, split, line_split)

    result = []
    for i in range(number):
        result.append(generate_sentence_with_grammer(grammer, target))
    return result


if __name__ == '__main__':
    zoo_grammer = create_grammer(grammer_str=ZOO_STORY, split='=')
    print(zoo_grammer)
    sentence = generate_sentence_with_grammer(zoo_grammer, target='zoo_story')
    print(sentence)

    sentences = generate_many_sentence(grammer_str=ZOO_STORY, split='=', line_split='\n', target='zoo_story', number=5)
    print(sentences)
