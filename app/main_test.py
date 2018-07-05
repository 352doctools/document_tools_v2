# _*_ coding:utf-8 _*_
# Filename: main_test.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试

import os
from flask import Flask, request, make_response, flash, render_template
from flask_bootstrap import Bootstrap
import json
import datetime
from flask import Flask, request, url_for, send_from_directory
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

bootstrap = Bootstrap(app)


# app.config.from_pyfile('config')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return '<h1>Hello 3下5除2 在线小工具!</h1>'


@app.route('/base')
def base():
    return render_template('base.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/sendjson', methods=['POST'])
def sendjson():
    # 接收前端发来的数据,转化为Json格式,我个人理解就是Python里面的字典格式
    data = json.loads(request.get_data())
    # 然后在本地对数据进行处理,再返回给前端
    name = data["name"]
    age = data["age"]
    location = data["location"]
    data["time"] = "2016"

    # Output: {u'age': 23, u'name': u'Peng Shuang', u'location': u'China'}
    # print data
    return jsonify(data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'用户名密码正确',
        ),
        dict(
            code=1,
            msg='error',
            data=u'用户名或密码错误',
        ),
    )
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uname"] == 'pangsong':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'用户登出成功',
        ),
        dict(
            code=1,
            msg='error',
            data=u'用户登出失败',
        ),
    )
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uname"] == 'pangsong':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'注册成功',
        ),
        dict(
            code=1,
            msg='error',
            data=u'注册失败',
        ),
    )
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uname"] == 'pangsong':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/register_name_check', methods=['GET', 'POST'])
def register_name_check():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'注册用户名不存在，可以注册',
        ),
        dict(
            code=1,
            msg='error',
            data=u'注册用户名已经存在，换一个用户名试试',
        ),
    )
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uname"] == 'pangsong':
            return json.dumps(message[1], ensure_ascii=False)
        else:
            return json.dumps(message[0], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_list', methods=['GET', 'POST'])
def doc_list():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docinfo=[
                    dict(
                        docid=12301,
                        docname="说明书1",
                        doctype="ipo",
                        docctime="2018-06-18 17:00:05",
                        docutime="2018-06-18 17:00:05",
                        docstate="3/13",
                    ),
                    dict(
                        docid=12302,
                        docname="说明书2",
                        doctype="ipo",
                        docctime="2018-06-18 17:00:05",
                        docutime="2018-06-18 17:00:05",
                        docstate="12/13",
                    ),
                ],
            ),
        ),
        dict(
            code=1,
            msg='error',
            data=u'获取数据出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_chapter', methods=['GET', 'POST'])
def doc_chapter():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=[
                dict(
                    docid=123,
                    docname="XXX说明书",
                    doctype="ipo",
                    chapters=[
                        dict(
                            cptitle="第⼀章",
                            cpcode="1000",
                            level="1",
                            next="0"
                        ),
                        dict(
                            cptitle="第⼆章",
                            cpcode="2000",
                            level="1",
                            next="1"
                        ),
                        dict(
                            cptitle="2.1",
                            cpcode="2100",
                            level="2",
                            next="0"
                        ),
                        dict(
                            cptitle="2.2",
                            cpcode="2200",
                            level="2",
                            next="0"
                        ),
                        dict(
                            cptitle="第三章",
                            cpcode="3000",
                            level="1",
                            next="1"
                        ),
                        dict(
                            cptitle="3.1",
                            cpcode="3100",
                            level="2",
                            next="0"
                        ),
                        dict(
                            cptitle="3.2",
                            cpcode="3200",
                            level="2",
                            next="1"
                        ),
                        dict(
                            cptitle="3.2.1",
                            cpcode="3210",
                            level="3",
                            next="0"
                        ),
                        dict(
                            cptitle="3.2.2",
                            cpcode="3220",
                            level="3",
                            next="0"
                        ),
                        dict(
                            cptitle="3.2.3",
                            cpcode="3230",
                            level="3",
                            next="1"
                        ),
                        dict(
                            cptitle="3.2.3.1",
                            cpcode="3231",
                            level="4",
                            next="0"
                        ),
                        dict(
                            cptitle="3.2.3.2",
                            cpcode="3232",
                            level="4",
                            next="0"
                        ),
                        dict(
                            cptitle="3.2.4",
                            cpcode="3240",
                            level="3",
                            next="0"
                        ),
                        dict(
                            cptitle="第四章",
                            cpcode="4000",
                            level="1",
                            next="0"
                        ),
                    ],
                ),
            ],
        ),
        dict(
            code=1,
            msg='error',
            data=u'获取数据出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_cl_check', methods=['GET', 'POST'])
def doc_cl_check():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                cpcode="1300",
                bcontent="<p>我们公司董事⻓是((president_name))……</p>",
                modulelist=[
                    dict(
                        modulecode="5111",
                        moduledisplay="董事⻓姓名为",
                        moduletype="rl",
                        modulesymbol="((president_name))",
                        modulenote="⽂档中所有董事⻓姓名讲被替换为输⼊内容",
                        tmlist=""
                    ),
                    dict(
                        modulecode="6121",
                        moduledisplay="请选择所属⾏业",
                        moduletype="tm",
                        modulesymbol="((hangye_risk))",
                        modulenote="根据您选择的⾏业，将给出推荐供您参考",
                        tmlist=[
                            dict(
                                tmtype="risk",
                                tmname="⾏业⻛险",
                                tminputlist=[
                                    dict(
                                        tminputcode="612101",
                                        tminputtext="⾦融⾏业",
                                    ),
                                    dict(
                                        tminputcode="612103",
                                        tminputtext="信息⾏业",
                                    ),
                                    dict(
                                        tminputcode="612103",
                                        tminputtext="其他⾏业",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dict(
            code=1,
            msg='error',
            data=u'获取数据出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_cl_check2', methods=['GET', 'POST'])
def doc_cl_check2():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                cpcode="1300",
                bcontent="""
                <p>公司控股股东((stockholder_name))以及实际控制人((controller_name))承诺：</p><p style="text-indent:2em">1、自公司股票上市之日起 36 个月内，不转让或者委托他人管理本次发行前其持有的公司股份，也不由公司回购该部分股份。</p><p style="text-indent:2em">2、在上述锁定期满后 2 年内减持的，其减持价格不低于发行价（指公司首次公开发行股票的发行价格，如果因公司上市后派发现金红利、送股、转增股本、增发新股等原因进行除权、除息的，则按照深圳证券交易所的有关规定作除权除息处理，下同）。</p><p style="text-indent:2em">3、公司上市后 6 个月内如公司股票连续 20 个交易日的收盘价均低于发行价，或者上市后 6 个月期末收盘价低于发行价，其所持公司股票的锁定期限自动延长 6 个月。</p><p style="text-indent:2em">4、在担任公司董事、监事或高级管理人员期间，每年转让持有的公司股份不超过其持有公司股份总数的 25%；离职后半年内，不转让其持有的公司股份。如在公司首次公开发行股票上市之日起 6 个月内申报离职的，自申报离职之日起 18 个月内不转让其直接持有的公司股份；在公司首次公开发行股票上市之日起第 7 个月至第 12 个月之间申报离职的，自申报离职之日起 12 个月内不转让其直接持有的公司股份。</p>
                """,
                rllist=[
                    dict(
                        rlname="公司控股股东姓名：",
                        rlsymbol="((stockholder_name))",
                        note="⽂档中所有公司控股股东姓名讲被替换为输⼊内容",
                    ),
                    dict(
                        rlname="实际控制人姓名：",
                        rlsymbol="((controller_name))",
                    ),
                ],
                tmlist=[
                    dict(
                        tmtype="risk",
                        tmname="⾏业⻛险",
                        tminputlist=[
                            dict(
                                tminputcode="612101",
                                tminputtext="⾦融⾏业",
                            ),
                            dict(
                                tminputcode="612102",
                                tminputtext="信息⾏业",
                            ),
                            dict(
                                tminputcode="612103",
                                tminputtext="其他⾏业",
                            ),
                        ],
                    ),
                    dict(
                        tmtype="promise",
                        tmname="承诺",
                        tminputlist=[
                            dict(
                                tminputcode="612101",
                                tminputtext="⾦融⾏业",
                            ),
                            dict(
                                tminputcode="612102",
                                tminputtext="信息⾏业",
                            ),
                            dict(
                                tminputcode="612103",
                                tminputtext="其他⾏业",
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dict(
            code=1,
            msg='error',
            data=u'获取数据出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_check_t', methods=['GET', 'POST'])
def doc_check_t():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                doccpcode="1300",
                tcontentlist=[
                    dict(
                        modulecode="6121",
                        tminputcode="612101",
                        tmcontent="⾏业⻛险是啥？是这个……",
                        tmctime="2018-02-11 20:19:12",
                        tmsource="著名公司xxx⾥"
                    ),
                    dict(
                        modulecode="6121",
                        tminputcode="612202",
                        tmcontent="⾏业⻛险我也不知道是啥……",
                        tmctime="2018-02-01 20:19:12",
                        tmsource="⼩破公司xxx鑫"
                    ),
                ],
            ),
        ),
        dict(
            code=1,
            msg='error',
            data=u'获取数据出错',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_save_temp', methods=['GET', 'POST'])
def doc_save_temp():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'暂存成功',
        ),
        dict(
            code=1,
            msg='error',
            data=u'暂存失败',
        ),
    )

    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


@app.route('/doc_download', methods=['GET', 'POST'])
def doc_download():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                docurl="http://www.abc.com/abc.docx",
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
        data = json.loads(request.get_data())
        if data["uid"] == '000':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')


if __name__ == '__main__':
    # 局域网访问调试
    app.run(host='127.0.0.1', port=8090, debug=True)
    # 本机调试
    # app.run(debug=True)
