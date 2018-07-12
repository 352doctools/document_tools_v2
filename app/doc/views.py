# _*_ coding:utf-8 _*_

from flask import render_template, request
import json
import doc_dal
from . import doc
from utils.is_json import is_json
from utils.post_json import post_json
from auth.user_dal import UserDal


@doc.route('/get_doc_by_id', methods=['GET', 'POST'])
def get_doc_by_id():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'doc_id' in data.keys():
                doc_dict = doc_dal.DocDal.get_doc_by_id(data)
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        if doc_dict is not None:
            return post_json(0, 'success', doc_dict)
        else:
            return post_json(data='获取文档出错')
    else:
        return render_template('404.html')


@doc.route('/doc_list', methods=['GET', 'POST'])
def get_doc_list():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys():
                if UserDal.check_uid(data) is not None:
                    doc_list = doc_dal.DocDal().get_doc_list(data)
                else:
                    return "用户校验出错"
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        return post_json(0, 'success', dict(docinfo=doc_list,))

    else:
        return render_template('404.html')


@doc.route('/doc_create', methods=['GET', 'POST'])
def doc_create():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys():
                if UserDal.check_uid(data) is not None:
                    doc_typeinfo = doc_dal.DocDal().get_doc_typeinfo()
                else:
                    return "用户校验出错"
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        return post_json(0, 'success', dict(doctypeinfo=doc_typeinfo))
    else:
        return render_template('404.html')


@doc.route('/doc_create1', methods=['GET', 'POST'])
def doc_create1():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docname' in data.keys() and 'doctype' in data.keys():
                if UserDal.check_uid(data) is not None:
                    new_doc = doc_dal.DocDal().insert_doc_and_get_doc(data)
                    if new_doc is not None:
                        doc_id = new_doc['doc_id']
                else:
                    return "用户校验出错"
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        if new_doc is not None:
            return post_json(0, 'success', dict(docid=doc_id))
        else:
            return post_json(data='新建文档出错')
    else:
        return render_template('404.html')


@doc.route('/doc_delete', methods=['GET', 'POST'])
def doc_delete():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys():
                if UserDal.check_uid(data) is not None:
                    rowcount = doc_dal.DocDal().delete_doc(data)
                else:
                    return "用户校验出错"
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        if rowcount > 0:
            return post_json(0, 'success', data='删除文档成功')
        else:
            return post_json(data='删除文档出错')
    else:
        return render_template('404.html')


@doc.route('/doc_chapter', methods=['GET', 'POST'])
def doc_chapter():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys():
                if UserDal.check_uid(data) is not None:
                    result = doc_dal.DocDal().doc_chapter(data)
                    if result is not None:
                        doc_dict = result[0]
                        doc_chapter_list = result[1]
                        data = dict(
                            docid=doc_dict['docid'],
                            docname=doc_dict['docname'],
                            doctype=doc_dict['doctype'],
                            chapters=doc_chapter_list,
                        )
                        return post_json(0, 'success', data=data)
                    else:
                        return post_json(data='提取目录出错')
                else:
                    return "用户校验出错"
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
    else:
        return render_template('404.html')