# _*_ coding:utf-8 _*_

from model import doc_model
from utils import mysql_utils
import uuid


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
