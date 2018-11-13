# _*_ coding:utf-8 _*_
from __future__ import division
from model import doc_model
from utils import mysql_utils
from auth import hash
import uuid
import re
import decimal
import os
import urllib2
import shutil
import time
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

# docx处理函数
def unzip_repalce_file(zipfilename, unziptodir, symbol_list):
    if not os.path.exists(unziptodir): os.makedirs(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            os.makedirs(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir)
            xml_content = zfobj.read(name)
            for symbol in symbol_list:
                if symbol['symbol'] in xml_content:
                    xml_content = xml_content.replace(symbol['symbol'], symbol['content'])

            with open(ext_filename, "wb") as f:
                f.write(xml_content)

# 删除文档解压缩临时文件
def zip_del_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()
    shutil.rmtree(dirname)

# 文档处理对象
class DocDal:
    def __init__(self):
        pass
    persist = None

    # 通过docid 查询文档信息
    @classmethod
    def get_doc_by_id(cls, params):
        sql = "select * from 352dt_doc_info where doc_id = %s and doc_state = 1"
        row = mysql_utils.Database().query_one(sql, (params['docid'],))
        if row is not None:
            docstate_sql = "select (select count(*) from 352dt_doc_content where docid = %s)" \
                           "/(select count(*) from 352dt_doc_base_content where doctype = %s " \
                           "and bcontent like %s) as result"
            result = mysql_utils.Database().query_one(docstate_sql, (row['doc_id'], row['doc_type'], '%((%'))
            doc = doc_model.Doc(docid=row['doc_id'], doctype=row['doc_type'], docname=row['doc_name'],
                                docctime=row['ctime'].strftime("%Y-%m-%d %H:%M:%S"),
                                docutime=row['utime'].strftime("%Y-%m-%d %H:%M:%S"),
                                docstate='%.1f%%' % (100 * result['result']))
            # 实例化一个对象，将查询结果添加给对象的属性
        else:
            return None
        return doc.to_dict()


    # 通过docid得到文档
    @classmethod
    def get_docpath_by_id(cls, docid):
        sql = "select * from 352dt_doc_info where doc_id = %s and doc_state = 1"
        row = mysql_utils.Database().query_one(sql, (docid,))
        return row


    # 通过key得到path
    @classmethod
    def get_doc_path_by_key(cls, key):
        sql = "select * from 352dt_doc_info where doc_key = %s"
        row = mysql_utils.Database().query_one(sql, (key,))
        return row['doc_path']


    # 通过uid得到用户已编辑的文档列表
    @classmethod
    def get_doc_list(cls, params):
        sql = "select * from 352dt_doc_info where doc_user_id = %s and doc_state = 1 order by utime desc"
        rows = mysql_utils.Database().query_all(sql, (params['uid'],))
        if len(rows) > 0:
            doc_list = []
            for row in rows:
                docstate_sql = "select (select count(*) from 352dt_doc_content where docid = %s)" \
                               "/(select count(*) from 352dt_doc_base_content where doctype = %s " \
                               "and bcontent like %s) as result"
                result = mysql_utils.Database().query_one(docstate_sql, (row['doc_id'], row['doc_type'], '%((%'))
                doc_user_id_sql = "select uname from 352dt_user_info where uid = %s "
                result_uname = mysql_utils.Database().query_one(doc_user_id_sql, (row['doc_user_id'],))
                doc = dict(docid=row['doc_id'],
                           doctype=row['doc_type'],
                           docname=row['doc_name'],
                           docpath=row['doc_path'],
                           doc_user_id=row['doc_user_id'],
                           doc_user_name=result_uname['uname'],
                           u_ids=row['u_ids'],
                           permission=row['permission'],
                           doc_key=row['doc_key'],
                           docctime=row['ctime'].strftime("%Y-%m-%d %H:%M:%S"),
                           docutime=row['utime'].strftime("%Y-%m-%d %H:%M:%S"),
                           docstate='%.1f%%' % (100*result['result'])
                           )
                doc_list.append(doc)
            return doc_list
        else:
            return None
    # 字典查询函数
    @classmethod
    def get_doc_dict(cls, dict_class):
        sql = "select * from 352dt_base_dict where dict_class = %s order by dict_class"
        rows = mysql_utils.Database().query_all(sql, (dict_class,))
        return rows
    # 查询字典对应文本
    @classmethod
    def get_doc_template_name(cls, doc_type):
        sql = "select dict_text from 352dt_base_dict where dict_name = %s"
        row = mysql_utils.Database().query_one(sql, (doc_type,))
        return row

    # 得到文档类型
    @classmethod
    def get_doc_typeinfo(cls):
        rows = cls.get_doc_dict('doc_type')
        if len(rows) > 0:
            doc_type_list = []
            for row in rows:
                doc_type = dict(doctype=row['dict_name'], doctypename=row['dict_text'])
                doc_type_list.append(doc_type)
            return doc_type_list
        else:
            return None

    # 插入新的文档并且获得该文档的docid
    @classmethod
    def insert_doc_and_get_doc(cls, params):
        download_url = str(uuid.uuid1()) + ".docx"
        doc_key = hash.docid_to_key(download_url)
        sql1 = "insert into 352dt_doc_info(doc_id, doc_type, doc_name, doc_path, doc_user_id, u_ids, ctime, utime, doc_state, permission, doc_key) " \
               "values (uuid(), %s, %s, %s, %s, %s, now(), now(), 1, 0, %s)"
        sql2 = "select * from 352dt_doc_info " \
               "where id = (select last_insert_id() from 352dt_doc_info limit 1)"
        row = mysql_utils.Database().insert_del_update_query_one(sql1, sql2,
                                                                 params1=(params['doctype'], params['docname'],
                                                                          download_url, params['uid'], params['uid'], doc_key))
        return row

    # 删除文档
    @classmethod
    def delete_doc(cls, params):
        sql = "update 352dt_doc_info set doc_state='0' " \
              "where doc_user_id=%s and doc_id = %s and doc_state = 1"
        rowcount = mysql_utils.Database().insert_del_update(sql, (params['uid'], params['docid'],))
        return rowcount

    # 得到文档的目录结构
    @classmethod
    def doc_chapter(cls, params):
        doc_dict = cls.get_doc_by_id(params)
        if doc_dict is None:
            return None
        sql = "select * from 352dt_doc_base_content " \
              "where doctype = %s"
        rows = mysql_utils.Database().query_all(sql, (doc_dict['doctype'],))
        if len(rows) > 0:
            doc_chapter_list = []
            for row in rows:
                doc_chapter = dict(cptitle=row['cptitle'], cpcode=row['cpcode'], level=row['cplevel'],
                                   next=row['cpnext'])
                doc_chapter_list.append(doc_chapter)
            return [doc_dict, doc_chapter_list]

        return [doc_dict, None]

    # 得到文档模板内容
    @classmethod
    def get_doc_base_content(cls, params):
        sql = "select * from 352dt_doc_base_content where cpcode = %s"
        row = mysql_utils.Database().query_one(sql, (params['cpcode'],))
        if row is not None:
            doc_base_content = dict(cpcode=row['cpcode'], bcontent=row['bcontent'], cpchange="0")
            return doc_base_content
        return row

    # 得到用户文档的内容
    @classmethod
    def get_doc_content(cls, params):
        sql = "select * from 352dt_doc_content where docid = %s and cpcode = %s"
        row = mysql_utils.Database().query_one(sql, (params['docid'], params['cpcode'],))
        if row is not None:
            doc_content = dict(cpcode=row['cpcode'], bcontent=row['bcontent'], cpchange="1")
            return doc_content
        return row

    # 得到替换标签的字典内容
    @classmethod
    def get_replace_label_dict(cls, params):
        sql = "select * from 352dt_replace_label_dict where doctype = %s and rlsymbol = %s "
        params['doctype'] = params['cpcode'].split('-')[0]
        row = mysql_utils.Database().query_one(sql, (params['doctype'], params['rlsymbol']))
        if row is not None:
            replace_label_dict = dict(rlcode=row['rlcode'], rlname=row['rlname'], rlcontent=row['rlname'],
                                      rlsymbol=row['rlsymbol'], rlnote=row['rlnote'], rlchange="0")
            return replace_label_dict
        return row

    # 得到替换标签用户编辑内容
    @classmethod
    def get_replace_label_content(cls, params):
        sql = "select * from 352dt_replace_label_content where docid = %s and rlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['docid'], params['rlsymbol']))
        if row is not None:
            replace_label_content = dict(rlcode=row['rlcode'], rlname=row['rlname'], rlcontent=row['rlcontent'],
                                         rlsymbol=row['rlsymbol'], rlnote=row['rlnote'], rlchange="1")
            return replace_label_content
        return row

    # 得到模板字典
    @classmethod
    def get_template_dict(cls, params):
        sql = "select * from 352dt_template_dict where doctype = %s and tmsymbol = %s "
        params['doctype'] = params['cpcode'].split('-')[0]
        row = mysql_utils.Database().query_one(sql, (params['doctype'], params['tmsymbol'], ))
        if row is not None:
            template_dict = dict(tmcode=row['tmcode'], tmtype=row['tmtype'], tmname=row['tmname'],
                                 tmsymbol=row['tmsymbol'], tmnote=row['tmnote'], tmcontent=row['tmname'], tmchange="0")
            return template_dict
        return row

    # 得到模板文档里模板标签的内容
    @classmethod
    def get_template_recommend_content_type(cls, params):
        sql = "select distinct tminputcode, tminputtext from 352dt_template_recommend_content " \
              "where cpcode = %s and tmcode = %s "
        rows = mysql_utils.Database().query_all(sql, (params['cpcode'], params['tmcode'], ))
        if len(rows) > 0:
            return rows
        return None

    # 得到模板标签用户内容
    @classmethod
    def get_template_content(cls, params):
        sql = "select * from 352dt_template_content where docid = %s and tmsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['docid'], params['tmsymbol'],))
        if row is not None:
            template_content = dict(tmcode=row['tmcode'], tmtype=row['tmtype'], tmname=row['tmname'],
                                    tmsymbol=row['tmsymbol'], tmnote=row['tmnote'],
                                    tmcontent=row['tmcontent'], tmchange="1")
            return template_content
        return row

    # 得到数字标签字典内容
    @classmethod
    def get_num_label_dict(cls, params):
        sql = "select * from 352dt_num_label_dict where doctype = %s and nlsymbol = %s "
        params['doctype'] = params['cpcode'].split('-')[0]
        row = mysql_utils.Database().query_one(sql, (params['doctype'], params['nlsymbol'], ))
        if row is not None:
            num_label_dict = dict(nlcode=row['nlcode'], nltype=row['nltype'], nlname=row['nlname'],
                                  nlsymbol=row['nlsymbol'], nlcontent=row['nlname'],
                                  nlnote=row['nlnote'], nlchange="0")
            return num_label_dict
        return row

    # 得到数字标签用户编辑内容
    @classmethod
    def get_num_label_content(cls, params):
        sql = "select * from 352dt_num_label_content where docid = %s and nlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['docid'], params['nlsymbol'], ))
        if row is not None:
            num_label_content = dict(nlcode=row['nlcode'], nltype=row['nltype'], nlname=row['nlname'],
                                     nlsymbol=row['nlsymbol'], nlcontent=row['nlcontent'],
                                     nlnote=row['nlnote'], nlchange="1")
            return num_label_content
        return row

    # 得到文档内容，查询标签并替换标签
    @classmethod
    def get_doc_cl_check(cls, params):
        doc_cl_check = cls.get_doc_content(params)
        if doc_cl_check is None:
            doc_cl_check = cls.get_doc_base_content(params)
            if doc_cl_check is None:
                return None
        doc_cl_check['docid'] = params['docid']
        regxString = doc_cl_check['bcontent']
        rlregx = re.compile("(\(\(str.*?\)\))")
        rllist = re.findall(rlregx, regxString)
        rllist = sorted(set(rllist), key=rllist.index)
        tmregx = re.compile("(\[\[tm.*?\]\])")
        tmlist = re.findall(tmregx, regxString)
        tmlist = sorted(set(tmlist), key=tmlist.index)
        nlregx = re.compile("(\(\(num.*?\)\))")
        nllist = re.findall(nlregx, regxString)
        nllist = sorted(set(nllist), key=nllist.index)
        if len(rllist) > 0:
            rllisttemp = []
            for rl in rllist:
                rl_result = cls.get_replace_label_content(dict(docid=params['docid'], rlsymbol=rl,))
                if rl_result is None:
                    rl_result = cls.get_replace_label_dict(dict(cpcode=params['cpcode'], rlsymbol=rl,))
                if rl_result is None:
                    pass
                    # rl_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + rl +" 标签")
                else:
                    rllisttemp.append(rl_result)
            rllist = rllisttemp
        else:
            rllist = None

        if len(tmlist) > 0:
            tmlisttemp = []
            for tm in tmlist:
                tm_result = cls.get_template_content(dict(docid=params['docid'], tmsymbol=tm, ))
                if tm_result is None:
                    tm_result = cls.get_template_dict(
                        dict(cpcode=params['cpcode'], tmsymbol=tm, ))
                if tm_result is None:
                    pass
                    # tm_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + tm + " 标签")
                else:
                    tminputlist = cls.get_template_recommend_content_type(
                        dict(cpcode=params['cpcode'], tmcode=tm_result['tmcode'],))
                    if tminputlist is not None:
                        tm_result['tminputlist'] = tminputlist
                    else:
                        pass
                        # tm_result['tminputlist'] = dict(err="当前类型文档当前章节该模板标签无可选模板")
                    tmlisttemp.append(tm_result)
            tmlist = tmlisttemp
        else:
            tmlist = None

        if len(nllist) > 0:
            nllisttemp = []
            for nl in nllist:
                nl_result = cls.get_num_label_content(dict(docid=params['docid'], nlsymbol=nl, ))
                if nl_result is None:
                    nl_result = cls.get_num_label_dict(
                        dict(cpcode=params['cpcode'], nlsymbol=nl, ))
                if nl_result is None:
                    pass
                    # nl_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + nl +" 标签")
                else:
                    nllisttemp.append(nl_result)
            nllist = nllisttemp
        else:
            nllist = None

        doc_cl_check['rllist'] = rllist
        doc_cl_check['tmlist'] = tmlist
        doc_cl_check['nllist'] = nllist
        return doc_cl_check


    # 得到所有标签
    @classmethod
    def get_doc_keywords(cls, params):
        keywords = dict()

        sql = "select rlcode, rltype, rlname, rlsymbol, rlnote from 352dt_replace_label_dict where doctype = %s order by rlsymbol;"
        rllist = mysql_utils.Database().query_all(sql, (params['doctype'],))

        sql2 = "select tmcode, tmtype, tmname, tmsymbol, tmnote from 352dt_template_dict where doctype = %s order by tmsymbol;"
        tmlist = mysql_utils.Database().query_all(sql2, (params['doctype'],))
        for row in tmlist:
            sql4 = "select tminputcode, tminputtext from 352dt_template_recommend_content where tmcode = %s group by tminputcode order by tminputcode"
            tminputtypelist = mysql_utils.Database().query_all(sql4, (row['tmcode'],))
            for row2 in tminputtypelist:
                sql5 = "select tmcontentcode, tmcontent, tmsource from 352dt_template_recommend_content where tmcode = %s and tminputcode=%s order by tmcontentcode"
                tminputlist = mysql_utils.Database().query_all(sql5, (row['tmcode'], row2['tminputcode']))
                row2['tminputlist'] = tminputlist
            row['tminputtypelist'] = tminputtypelist

        sql3 = "select nlcode, nltype, nlname, nlcontent, nlsymbol, nlnote from 352dt_num_label_dict where doctype = %s order by nlsymbol;"
        nllist = mysql_utils.Database().query_all(sql3, (params['doctype'],))

        keywords['rllist'] = rllist
        keywords['nllist'] = nllist
        keywords['tmlist'] = tmlist
        return keywords


    # 得到数字标签计算公式
    @classmethod
    def get_formula(cls, params):
        # 通过params里面的'cpcode'得到所有公式formulas
        sql = "select * from 352dt_num_label_dict " \
              "where doctype = %s and nltype = 'output' "
        params['doctype'] = params['cpcode'].split('-')[0]
        rows = mysql_utils.Database().query_all(sql, (params['doctype'],))
        if len(rows) > 0:
            formulas = []
            for row in rows:
                formula = dict(lcode=row["nlcode"], lsymbol=row['nlsymbol'], lcontent=row['nlcontent'])
                formulas.append(formula)
            return formulas
        else:
            return None

    # 根据公式计算数字标签
    @classmethod
    def calc_nl_value(cls, params):
        formulas = cls.get_formula(params)
        if formulas is None:
            return None
        for formula in formulas:
            for item in params['llist']:
                if 'lsymbol' in item.keys() and 'lcontent' in item.keys():
                    formula['lcontent'] = formula['lcontent'].replace(item['lsymbol'], item['lcontent'])
                else:
                    return None
            calc = eval(formula['lcontent'])
            formula['lcontent'] = str(decimal.Decimal(calc).quantize(decimal.Decimal('0.00')))
        return formulas

    # 得到模板选择内容
    @classmethod
    def doc_check_t(cls, params):
        sql = "select tminputcode, tmcontentcode, tmcontent, ctime, tmsource " \
              "from 352dt_template_recommend_content where cpcode = %s and tmcode = %s and tminputcode = %s"
        rows = mysql_utils.Database().query_all(sql, (params['cpcode'], params['tmcode'], params['tminputcode'],))
        if len(rows) > 0:
            for row in rows:
                row['tmctime'] = row.pop('ctime').strftime('%Y-%m-%d %H:%M:%S')
            return rows
        else:
            return None

    # 暂存文档，将前台传回数据标准化并保存
    @classmethod
    def doc_save_temp(cls, params):
        uid = params['uid']
        docid = params['docid']
        cpcode = params['cpcode']
        cpcontent = params['cpcontent']
        doctype = params['cpcode'].split('-')[0]
        database = mysql_utils.Database()

        rlregx = re.compile("(<span[^<]*?rlcode=\"(.*?)\" rlsymbol=\"(.*?)\">(.*?)</span>)")
        tmregx = re.compile("(<span[^<]*?tmcode=\"(.*?)\" tmsymbol=\"(.*?)\">(.*?)</span>)")
        nlregx = re.compile("(<span[^<]*?nlcode=\"(.*?)\" nlsymbol=\"(.*?)\">(.*?)</span>)")
        rllist = re.findall(rlregx, cpcontent)
        tmlist = re.findall(tmregx, cpcontent)
        nllist = re.findall(nlregx, cpcontent)
        rllist = sorted(set(rllist), key=rllist.index)
        tmlist = sorted(set(tmlist), key=tmlist.index)
        nllist = sorted(set(nllist), key=nllist.index)

        rl_insert_result = 0
        tm_insert_result = 0
        nl_insert_result = 0

        if len(rllist) > 0:
            for rl in rllist:
                cpcontent = cpcontent.replace(rl[0], rl[2])
                rl_dict_sql = "select rlname, rltype, rlnote from 352dt_replace_label_dict " \
                              "where doctype = %s and rlcode = %s"
                rl_dict_result = database.query_one(rl_dict_sql, (doctype, rl[1],))
                if rl_dict_result is None:
                    return None
                else:
                    rl_content_sql = "select * from 352dt_replace_label_content " \
                                     "where docid = %s and rlcode = %s"
                    rl_content_result = database.query_one(rl_content_sql, (docid, rl[1],))
                    if rl_content_result is None:
                        sql = "insert into " \
                              "352dt_replace_label_content(uid, docid, cpcode, rlcode, rlname, rltype, rlcontent, " \
                              "rlsymbol, rlnote, ctime, utime) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())"
                        rl_result = database.insert_del_update(sql, (
                            uid, docid, cpcode, rl[1], rl_dict_result['rlname'], rl_dict_result['rltype'],
                            rl[3], rl[2], rl_dict_result['rlnote'],
                        ))
                    else:
                        sql = "update 352dt_replace_label_content set cpcode = %s, rlcontent = %s, utime = now()" \
                              "where docid = %s and rlcode = %s"
                        rl_result = database.insert_del_update(sql, (cpcode, rl[3], docid, rl[1],))
                rl_insert_result += rl_result

        if len(tmlist) > 0:
            for tm in tmlist:
                cpcontent = cpcontent.replace(tm[0], tm[2])
                tm_dict_sql = "select tmname, tmtype, tmnote from 352dt_template_dict " \
                              "where doctype = %s and tmcode = %s"
                tm_dict_result = database.query_one(tm_dict_sql, (doctype, tm[1],))
                if tm_dict_result is None:
                    return None
                else:
                    tm_content_sql = "select * from 352dt_template_content " \
                                     "where docid = %s and tmcode = %s"
                    tm_content_result = database.query_one(tm_content_sql, (docid, tm[1],))
                    if tm_content_result is None:
                        sql = "insert into " \
                              "352dt_template_content(uid, docid, cpcode, tmcode, tmname, tmtype, tmcontent, " \
                              "tmsymbol, tmnote, ctime, utime) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())"
                        tm_result = database.insert_del_update(sql, (uid, docid, cpcode, tm[1], tm_dict_result['tmname'],
                            tm_dict_result['tmtype'], tm[3], tm[2], tm_dict_result['tmnote'],
                        ))
                    else:
                        sql = "update 352dt_template_content set cpcode = %s, tmcontent = %s, utime = now()" \
                              "where docid = %s and tmcode = %s"
                        tm_result = database.insert_del_update(sql, (cpcode, tm[3], docid, tm[1],))
                tm_insert_result += tm_result

        if len(nllist) > 0:
            for nl in nllist:
                cpcontent = cpcontent.replace(nl[0], nl[2])
                nl_dict_sql = "select nlname, nltype, nlnote from 352dt_num_label_dict " \
                              "where doctype = %s and nlcode = %s"
                nl_dict_result = database.query_one(nl_dict_sql, (doctype, nl[1],))
                if nl_dict_result is None:
                    return None
                else:
                    nl_content_sql = "select * from 352dt_num_label_content " \
                                     "where docid = %s and nlcode = %s"
                    nl_content_result = database.query_one(nl_content_sql, (docid, nl[1],))
                    if nl_content_result is None:
                        sql = "insert into " \
                              "352dt_num_label_content(uid, docid, cpcode, nlcode, nlname, nltype, nlcontent, " \
                              "nlsymbol, nlnote, ctime, utime) " \
                              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())"
                        nl_result = database.insert_del_update(sql, (uid, docid, cpcode, nl[1], nl_dict_result['nlname'],
                            nl_dict_result['nltype'], nl[3], nl[2], nl_dict_result['nlnote'],
                        ))
                    else:
                        sql = "update 352dt_num_label_content set cpcode = %s, nlcontent = %s, utime = now()" \
                              "where docid = %s and nlcode = %s"
                        nl_result = database.insert_del_update(sql, (cpcode, nl[3], docid, nl[1],))
                nl_insert_result += nl_result

        doc_dict_sql = "select cptitle from 352dt_doc_base_content where cpcode = %s"
        doc_dict_result = database.query_one(doc_dict_sql, (cpcode,))
        if doc_dict_result is None:
            return None
        else:
            doc_content_sql = "select * from 352dt_doc_content where uid = %s and docid = %s and cpcode = %s"
            doc_content_result = database.query_one(doc_content_sql, (uid, docid, cpcode))
            if doc_content_result is None:
                cpcontent_sql = "insert into 352dt_doc_content(uid, docid, cpcode, cptitle, bcontent, ctime, utime)" \
                                "values (%s, %s, %s, %s, %s, now(), now())"
                cpcontent_result = database.insert_del_update(cpcontent_sql, (uid, docid, cpcode,
                                                                              doc_dict_result['cptitle'], cpcontent,))
            else:
                cpcontent_sql = "update 352dt_doc_content set bcontent = %s, utime = now() " \
                                "where docid = %s and cpcode = %s"
                cpcontent_result = database.insert_del_update(cpcontent_sql, (cpcontent, docid, cpcode))

        if rl_insert_result != len(rllist) or tm_insert_result != len(tmlist) \
                or nl_insert_result != len(nllist) or cpcontent_result != 1:
            return None
        else:
            return True

    # 得到标签列表
    @classmethod
    def get_symbol_list(cls, params):
        symbol_list = []
        sql = "select rlsymbol, rlcontent from 352dt_replace_label_content " \
              "where uid = %s and docid = %s"
        rows = mysql_utils.Database().query_all(sql, (params['uid'], params['docid'],))
        rlsymbol_list = []
        if len(rows) > 0:
            for row in rows:
                rlsymbol = dict(
                    symbol=row['rlsymbol'],
                    content=row['rlcontent'],
                )
                rlsymbol_list.append(rlsymbol)
        symbol_list.extend(rlsymbol_list)

        sql = "select nlsymbol, nlcontent from 352dt_num_label_content " \
              "where uid = %s and docid = %s"
        rows = mysql_utils.Database().query_all(sql, (params['uid'], params['docid'],))
        nlsymbol_list = []
        if len(rows) > 0:
            for row in rows:
                nlsymbol = dict(
                    symbol=row['nlsymbol'],
                    content=row['nlcontent'],
                )
                nlsymbol_list.append(nlsymbol)
        symbol_list.extend(nlsymbol_list)

        sql = "select tmsymbol, tmcontent from 352dt_template_content " \
              "where uid = %s and docid = %s"
        rows = mysql_utils.Database().query_all(sql, (params['uid'], params['docid'],))
        tmsymbol_list = []
        if len(rows) > 0:
            for row in rows:
                tmsymbol = dict(
                    symbol=row['tmsymbol'],
                    content=row['tmcontent'],
                )
                tmsymbol_list.append(tmsymbol)
        symbol_list.extend(tmsymbol_list)
        # symbol_list.extend([{"symbol": "((str_company_issuer))", "content": "((str_company_issuer111))"}, ])
        return symbol_list

    # 获取文档下载连接
    @classmethod
    def get_doc_url(cls, params, request):
        doc_type = cls.get_doc_by_id(params)['doctype']
        template_name = cls.get_doc_template_name(doc_type)
        if template_name is None:
            return None
        template_name = template_name['dict_text']
        docpath = cls.get_docpath_by_id(params['docid'])['doc_path']
        template_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/template')
        user_doc_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/user-doc')

        try:
            unzip_repalce_file(template_dir + '/' + template_name + ".docx",
                               template_dir + '/' + template_name + '_' + params['docid'],
                               cls.get_symbol_list(params))
            zip_del_dir(template_dir + '/' + template_name + '_' + params['docid'],
                    user_doc_dir + '/' + template_name + '_' + docpath)
        except:
            return None
        return dict(
            docid=params['docid'],
            docurl=request.url_root + 'download_file' + '?' + 'downloadFile=' + template_name + '_' + docpath,
        )

    # 获取文档下载连接
    @classmethod
    def copy_file(cls, doc_type, doc_id):
        template_name = cls.get_doc_template_name(doc_type)
        template_name = template_name['dict_text']
        docpath = cls.get_docpath_by_id(doc_id)['doc_path']
        template_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/template')
        user_doc_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/user-doc')
        shutil.copy(template_dir + '/' + template_name + ".docx", user_doc_dir + '/' + docpath)


# 获取文档下载连接
    @classmethod
    def save_file(cls, url, doc_path):
        user_doc_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '..' + '/' + '..' + '/user-doc')
        doc_path = user_doc_dir + '/' + doc_path
        f = urllib2.urlopen(url)
        stream = f.read()
        with open(doc_path, "wb") as code:
            code.write(stream)

