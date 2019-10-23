# -*- coding: utf-8 -*-
# @Time : 2019/10/22 6:55 PM 
# @Author : qiujiafa
# @File : flask_test.py

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hell_world():
    return 'Hello world!'


if __name__ == '__main__':
    app.run()