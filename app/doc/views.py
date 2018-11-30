# _*_ coding:utf-8 _*_

from flask import render_template, request, send_from_directory, g
import json
import doc_dal
from . import doc
from utils.is_json import is_json
from utils.post_json import post_json
from auth.user_dal import UserDal
import utils.jwt_utils as jwt_utils
import os


# 通过id获取文档路由
@doc.route('/get_doc_by_id', methods=['GET', 'POST'])
def get_doc_by_id():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'doc_id' in data.keys():
                doc_dict = doc_dal.DocDal.get_doc_by_id(data)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
        if doc_dict is not None:
            return post_json('success', data=doc_dict)
        else:
            return post_json('error', '获取文档出错')
    else:
        return render_template('404.html')


# 获取用户文档列表路由
@doc.route('/doc_list', methods=['GET', 'POST'])
def get_doc_list():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        uid = jwt_utils.get_uid_token(request)[0]
        doc_list = doc_dal.DocDal().get_doc_list({'uid': uid})
        return post_json('success', data=doc_list)

    else:
        return render_template('404.html')


# 获取文档类型
@doc.route('/doc_temp', methods=['GET', 'POST'])
def doc_temp():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        doc_typeinfo = doc_dal.DocDal().get_doc_typeinfo()
        return post_json('success', data=dict(doctypeinfo=doc_typeinfo))
    else:
        return render_template('404.html')


# 新建路由
@doc.route('/doc_create', methods=['GET', 'POST'])
def doc_create():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            uid = jwt_utils.get_uid_token(request)[0]
            data.update({'uid': uid})
            if 'docname' in data.keys() and 'doctype' in data.keys():
                new_doc = doc_dal.DocDal().insert_doc_and_get_doc(data)
                if new_doc is not None:
                    # doc_id = new_doc['doc_id']
                    # return post_json('success', data=dict(docid=doc_id))
                    doc_dal.DocDal().copy_file(new_doc['doc_type'], new_doc['doc_id'])
                    return post_json('success', '新建文档成功')
                else:
                    return post_json('error', '新建文档出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 删除文档路由
@doc.route('/doc_delete', methods=['GET', 'POST'])
def doc_delete():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            uid = jwt_utils.get_uid_token(request)[0]
            data.update({'uid': uid})
            if 'docid' in data.keys():
                rowcount = doc_dal.DocDal().delete_doc(data)
                if rowcount > 0:
                    return post_json('success', '删除文档成功')
                else:
                    return post_json('success', '删除文档出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 获取文档章节目录路由
@doc.route('/doc_chapter', methods=['GET', 'POST'])
def doc_chapter():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
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
                        return post_json('success', data=data)
                    else:
                        return post_json('success', '提取目录出错')
                else:
                    return post_json('error', '用户校验出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 获取所有标签
@doc.route('/doc_keywords', methods=['GET', 'POST'])
def doc_keywords():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'doctype' in data.keys():
                keywords = doc_dal.DocDal().get_doc_keywords(data)
                return post_json('success', data=keywords)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 获取文档类型关键字返回内容
@doc.route('/doc_type_keyword', methods=['GET', 'POST'])
def doc_type_keyword():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'doctype' in data.keys() and 'keyword' in data.keys():
                if 'page' in data.keys():
                    if str(data['page']).isdigit() and int(data['page']) > 0:
                        contentlist = doc_dal.DocDal().get_doc_type_keyword(data)
                        return post_json('success', data=contentlist)
                    else:
                        return post_json('error', '输入参数不完整或者不正确')
                else:
                    result = doc_dal.DocDal().get_doc_type_keyword(data)
                    return post_json('success', data=result)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')



# 章节模块查询路由
@doc.route('/doc_cl_check', methods=['GET', 'POST'])
def get_doc_cl_check():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys() and 'cpcode' in data.keys():
                if UserDal.check_uid(data) is not None:
                    doc_cl_check = doc_dal.DocDal().get_doc_cl_check(data)
                    if doc_cl_check is not None:
                        return post_json('success', data=doc_cl_check)
                    else:
                        return post_json('error', '章节模块查询出错')
                else:
                    return post_json('error', '用户校验出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 计算数字标签数值
@doc.route('/calc_nl_value', methods=['GET', 'POST'])
def calc_nl_value():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys() and 'cpcode' in data.keys() \
                    and 'llist' in data.keys():
                if UserDal.check_uid(data) is not None:
                    calc_nl_value = doc_dal.DocDal().calc_nl_value(data)
                    if calc_nl_value is not None:
                        return post_json('success', data=calc_nl_value)
                    else:
                        return post_json('error', '标签提交出错')
                else:
                    return post_json('error', '用户校验出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 模块查询路由
@doc.route('/doc_check_t', methods=['GET', 'POST'])
def doc_check_t():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys() and 'cpcode' in data.keys() \
                    and 'tmcode' in data.keys() and 'tminputcode' in data.keys():
                if UserDal.check_uid(data) is not None:
                    tcontentlist = doc_dal.DocDal().doc_check_t(data)
                    if doc_check_t is not None:
                        return post_json('success', data=tcontentlist)
                    else:
                        return post_json('error', '模板查询出错')
                else:
                    return post_json('error', '用户校验出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 文档暂存路由
@doc.route('/doc_save', methods=['GET', 'POST'])
def doc_save():
    if is_json(request.get_data()):
        data = json.loads(request.get_data())
        with open("1.txt", "a") as code:
            code.write(request.path+"\n"+request.url+"\n"+request.get_data()+"\n")
        if 'status' in data.keys() and 'url' in data.keys() and 'key' in data.keys():
            if data['status'] == 2:
                doc_path = doc_dal.DocDal().get_doc_path_by_key(data['key'])
                url = data['url']
                doc_dal.DocDal().save_file(url, doc_path, data['key'])
                return post_json('success', '保存成功')
            else:
                return "{\"error\":0}"
        else:
            return "{\"error\":0}"
    else:
        return "{\"error\":0}"


# 文档保存路由
@doc.route('/doc_save_temp', methods=['GET', 'POST'])
def doc_save_temp():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys() and 'cpcode' in data.keys() \
                    and 'cpcontent' in data.keys():
                if UserDal.check_uid(data) is not None:
                    doc_save_return = doc_dal.DocDal().doc_save_temp(data)
                    if doc_save_return is not None:
                        return post_json('success', '暂存数据成功')
                    else:
                        return post_json('error', '数据暂存出错')
                else:
                    return post_json('error', '用户校验出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')


# 获取文档下载地址路由
@doc.route('/doc_download', methods=['GET', 'POST'])
def doc_download():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'docid' in data.keys():
                if UserDal.check_uid(data) is None:
                    return post_json('error', '用户校验出错')
                if doc_dal.DocDal.get_doc_by_id(data) is None:
                    return post_json('error', '该文档不存在或已删除')
                doc_url = doc_dal.DocDal().get_doc_url(data, request)
                if doc_url is not None:
                    return post_json('success', data=doc_url)
                else:
                    return post_json('error', '文档下载出错')
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
    else:
        return render_template('404.html')

# 下载路由
@doc.route('/download_file', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        return post_json('error', '请使用get方法')
    elif request.method == 'GET':
        downloadFile = request.args.get('downloadFile')
        user_doc_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/user-doc')
        return send_from_directory(user_doc_dir, downloadFile, as_attachment=True)
    else:
        return render_template('404.html')
