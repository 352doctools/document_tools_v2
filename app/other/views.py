# _*_ coding:utf-8 _*_

from flask import render_template, request
import json
from . import other
import time
from utils.post_json import post_json


@other.route('/doc_download', methods=['GET', 'POST'])
def doc_download():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                docurl="https://www.liuxue86.com/uploadfile/2016/0819/20160819100139702.doc",
            )

        ),
        dict(
            code=1,
            msg='error',
            data=u'下载出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        time.sleep(5)
        return post_json(0, 'success', data=message[0])
    else:
        return render_template('404.html')

