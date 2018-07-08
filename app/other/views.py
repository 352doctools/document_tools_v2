# _*_ coding:utf-8 _*_

from flask import render_template, request
import json
from . import other


@other.route('/doc_chapter', methods=['GET', 'POST'])
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


@other.route('/doc_cl_check', methods=['GET', 'POST'])
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


@other.route('/doc_cl_check2', methods=['GET', 'POST'])
def doc_cl_check2():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=dict(
                docid="123",
                cpcode="1300",
                bcontent="我们公司董事⻓是((president_name))……",
                rllist=[
                    dict(
                        rlname="董事⻓姓名",
                        rlsymbol="((president_name))"
                    ),
                    dict(
                        rlname="股东姓名",
                        rlsymbol="((stockholder_name))"
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


@other.route('/doc_check_t', methods=['GET', 'POST'])
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


@other.route('/doc_save_temp', methods=['GET', 'POST'])
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


@other.route('/doc_download', methods=['GET', 'POST'])
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

