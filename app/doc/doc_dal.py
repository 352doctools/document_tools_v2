# _*_ coding:utf-8 _*_
from __future__ import division
from model import doc_model
from utils import mysql_utils
import uuid
import re
import decimal


class DocDal:
    def __init__(self):
        pass
    persist = None

    # 通过用户名及密码查询用户对象
    @classmethod
    def get_doc_by_id(cls, params):
        sql = "select * from 352dt_doc_info where doc_id = %s and doc_state = 1"
        row = mysql_utils.Database().query_one(sql, (params['docid'],))
        if row is not None:
            doc = doc_model.Doc(docid=row['doc_id'], doctype=row['doc_type'], docname=row['doc_name'],
                                docctime=row['ctime'].strftime("%Y-%m-%d %H:%M:%S"),
                                docutime=row['utime'].strftime("%Y-%m-%d %H:%M:%S"),
                                docstate="3/13")
            # 实例化一个对象，将查询结果添加给对象的属性
        else:
            return None
        return doc.to_dict()

    # 通过用户名及密码注册对象
    @classmethod
    def get_doc_list(cls, params):
        sql = "select * from 352dt_doc_info where doc_user_id = %s and doc_state = 1 order by utime desc"
        rows = mysql_utils.Database().query_all(sql, (params['uid'],))
        if len(rows) > 0:
            doc_list = []
            for row in rows:
                doc = doc_model.Doc(docid=row['doc_id'], doctype=row['doc_type'], docname=row['doc_name'],
                                    docctime=row['ctime'].strftime("%Y-%m-%d %H:%M:%S"),
                                    docutime=row['utime'].strftime("%Y-%m-%d %H:%M:%S"),
                                    docstate="3/13")
                doc_list.append(doc.to_dict())
            return doc_list
        else:
            return None

    @classmethod
    def get_doc_dict(cls, dict_class):
        sql = "select * from 352dt_base_dict where dict_class = %s order by dict_class"
        rows = mysql_utils.Database().query_all(sql, (dict_class,))
        return rows

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

    @classmethod
    def insert_doc_and_get_doc(cls, params):
        download_url = "http://" + str(uuid.uuid1()) + ".docx"
        sql1 = "insert into 352dt_doc_info(doc_id, doc_type, doc_name, doc_path, doc_user_id, ctime, utime, doc_state) " \
               "values (uuid(), %s, %s, %s, %s, now(), now(), 1)"
        sql2 = "select * from 352dt_doc_info " \
               "where id = (select last_insert_id() from 352dt_doc_info limit 1)"
        row = mysql_utils.Database().insert_del_update_query_one(sql1, sql2,
                                                                 params1=(params['doctype'], params['docname'],
                                                                          download_url, params['uid']))
        return row

    @classmethod
    def delete_doc(cls, params):
        sql = "update 352dt_doc_info set doc_state='0' " \
              "where doc_user_id=%s and doc_id = %s and doc_state = 1"
        rowcount = mysql_utils.Database().insert_del_update(sql, (params['uid'], params['docid'],))
        return rowcount

    @classmethod
    def doc_chapter(cls, params):
        doc_dict = cls.get_doc_by_id(params)
        if doc_dict is None:
            return None
        sql = "select * from 352dt_doc_base_content " \
              "where doc_type = %s"
        rows = mysql_utils.Database().query_all(sql, (doc_dict['doctype'],))
        if len(rows) > 0:
            doc_chapter_list = []
            for row in rows:
                doc_chapter = dict(cptitle=row['cptitle'], cpcode=row['cpcode'], level=row['cplevel'],
                                   next=row['cpnext'])
                doc_chapter_list.append(doc_chapter)
            return [doc_dict, doc_chapter_list]

        return [doc_dict, None]

    @classmethod
    def get_doc_base_content(cls, params):
        sql = "select * from 352dt_doc_base_content where cpcode = %s"
        row = mysql_utils.Database().query_one(sql, (params['cpcode'],))
        if row is not None:
            doc_base_content = dict(cpcode=row['cpcode'], bcontent=row['bcontent'], change="0")
            return doc_base_content
        return row

    @classmethod
    def get_doc_content(cls, params):
        sql = "select * from 352dt_doc_content where docid = %s and cpcode = %s"
        row = mysql_utils.Database().query_one(sql, (params['docid'], params['cpcode'],))
        if row is not None:
            doc_content = dict(cpcode=row['cpcode'], bcontent=row['bcontent'], change="1")
            return doc_content
        return row

    @classmethod
    def get_replace_label_dict(cls, params):
        sql = "select * from 352dt_replace_label_dict where cpcode = %s " \
              "and rlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['rlsymbol']))
        if row is not None:
            replace_label_dict = dict(rlcode=row['rlcode'], rlname=row['rlname'], rlcontent=row['rlcontent'],
                                      rlsymbol=row['rlsymbol'], rlnote=row['rlnote'], change="0")
            return replace_label_dict
        return row

    @classmethod
    def get_replace_label_content(cls, params):
        sql = "select * from 352dt_replace_label_content where cpcode = %s " \
              "and docid = %s and rlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['docid'], params['rlsymbol']))
        if row is not None:
            replace_label_content = dict(rlcode=row['rlcode'], rlname=row['rlname'], rlcontent=row['rlcontent'],
                                         rlsymbol=row['rlsymbol'], rlnote=row['rlnote'], change="1")
            return replace_label_content
        return row

    @classmethod
    def get_template_dict(cls, params):
        sql = "select * from 352dt_template_dict where cpcode = %s and tmsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['tmsymbol'], ))
        if row is not None:
            template_dict = dict(tmcode=row['tmcode'], tmtype=row['tmtype'], tmname=row['tmname'],
                                 tmsymbol=row['tmsymbol'], tmnote=row['tmnote'], tmcontent=row['tmcontent'], change="0")
            return template_dict
        return row

    @classmethod
    def get_template_recommend_content_type(cls, params):
        sql = "select distinct tminputcode, tminputtext from 352dt_template_recommend_content " \
              "where cpcode = %s and tmcode = %s "
        rows = mysql_utils.Database().query_all(sql, (params['cpcode'], params['tmcode'], ))
        if len(rows) > 0:
            return rows
        return None

    @classmethod
    def get_template_content(cls, params):
        sql = "select * from 352dt_template_content where cpcode = %s and docid = %s and tmsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['docid'], params['tmsymbol'],))
        if row is not None:
            template_content = dict(tmcode=row['tmcode'], tmtype=row['tmtype'], tmname=row['tmname'],
                                    tmsymbol=row['tmsymbol'], tmnote=row['tmnote'],
                                    tmcontent=row['tmcontent'], change="1")
            return template_content
        return row

    @classmethod
    def get_num_label_dict(cls, params):
        sql = "select * from 352dt_num_label_dict where cpcode = %s and nlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['nlsymbol'], ))
        if row is not None:
            num_label_dict = dict(nlcode=row['nlcode'], nltype=row['nltype'], nlname=row['nlname'],
                                  nlsymbol=row['nlsymbol'], nlcontent=row['nlcontent'],
                                  nlnote=row['nlnote'], changer="0")
            return num_label_dict
        return row

    @classmethod
    def get_num_label_content(cls, params):
        sql = "select * from 352dt_num_label_content where cpcode = %s and docid = %s and nlsymbol = %s "
        row = mysql_utils.Database().query_one(sql, (params['cpcode'], params['docid'], params['nlsymbol'], ))
        if row is not None:
            num_label_content = dict(nlcode=row['nlcode'], nltype=row['nltype'], nlname=row['nlname'],
                                     nlsymbol=row['nlsymbol'], nlcontent=row['nlcontent'],
                                     nlnote=row['nlnote'], changer="1")
            return num_label_content
        return row

    @classmethod
    def get_doc_cl_check(cls, params):
        doc_cl_check = cls.get_doc_content(params)
        if doc_cl_check is None:
            doc_cl_check = cls.get_doc_base_content(params)
            if doc_cl_check is None:
                return None
        doc_cl_check['cpcode'] = params['cpcode']
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
                rl_result = cls.get_replace_label_content(dict(cpcode=params['cpcode'],
                                                        docid=params['docid'], rlsymbol=rl,))
                if rl_result is None:
                    rl_result = cls.get_replace_label_dict(dict(cpcode=params['cpcode'], rlsymbol=rl,))
                if rl_result is None:
                    rl_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + rl +" 标签")
                rllisttemp.append(rl_result)
            rllist = rllisttemp
        else:
            rllist = None

        if len(tmlist) > 0:
            tmlisttemp = []
            for tm in tmlist:
                tm_result = cls.get_template_content(dict(cpcode=params['cpcode'],
                                                           docid=params['docid'], tmsymbol=tm, ))
                if tm_result is None:
                    tm_result = cls.get_template_dict(
                        dict(cpcode=params['cpcode'], tmsymbol=tm, ))
                if tm_result is None:
                    tm_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + tm + " 标签")
                else:
                    tminputlist = cls.get_template_recommend_content_type(
                        dict(cpcode=params['cpcode'], tmcode=tm_result['tmcode'],))
                    if tminputlist is not None:
                        tm_result['tminputlist'] = tminputlist
                    else:
                        tm_result['tminputlist'] = dict(err="当前类型文档当前章节该模板标签无可选模板")
                tmlisttemp.append(tm_result)
            tmlist = tmlisttemp
        else:
            tmlist = None

        if len(nllist) > 0:
            nllisttemp = []
            for nl in nllist:
                nl_result = cls.get_num_label_content(dict(cpcode=params['cpcode'],
                                                           docid=params['docid'], nlsymbol=nl, ))
                if nl_result is None:
                    nl_result = cls.get_num_label_dict(
                        dict(cpcode=params['cpcode'], nlsymbol=nl, ))
                if nl_result is None:
                    nl_result = dict(err="数字标签字典当前类型文档当前章节中没有 " + nl +" 标签")
                nllisttemp.append(nl_result)
            nllist = nllisttemp
        else:
            nllist = None

        doc_cl_check['rllist'] = rllist
        doc_cl_check['tmlist'] = tmlist
        doc_cl_check['nllist'] = nllist
        return doc_cl_check


    @classmethod
    def get_formula(cls, params):
        # 通过params里面的'cpcode'得到所有公式formulas
        sql = "select * from 352dt_num_label_dict " \
              "where cpcode = %s and nltype = 'output' "
        rows = mysql_utils.Database().query_all(sql, (params['cpcode'],))
        if len(rows) > 0:
            formulas = {}
            for row in rows:
                formulas[row['nlsymbol']] = row['nlcontent']
            return formulas
        else:
            return None

    @classmethod
    def calc_nl_value(cls, params):
        formulas = cls.get_formula(params)
        if formulas is None:
            return None
        for key in formulas.keys():
            for item in params['llist']:
                if 'lsymbol' in item.keys() and 'lcontent' in item.keys():
                    formulas[key] = formulas[key].replace(item['lsymbol'], item['lcontent'])
                else:
                    return None
            calc = eval(formulas[key])
            formulas[key] = decimal.Decimal(calc).quantize(decimal.Decimal('0.00'))
        return formulas

