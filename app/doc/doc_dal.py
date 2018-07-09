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
        sql = "select * from 352dt_doc_info where doc_id = %s"
        row = mysql_utils.Database().query_one(sql, (params['doc_id'],))
        if row is not None:
            doc = doc_model.Doc(docid=row[1], docname=row[2], doctype=row[3],
                                docctime=row[6].strftime("%Y-%m-%d %H:%M:%S"),
                                docutime=row[7].strftime("%Y-%m-%d %H:%M:%S"),
                                docstate=None)
            # 实例化一个对象，将查询结果添加给对象的属性
        else:
            return None

        return doc

    # 通过用户名及密码注册对象
    @classmethod
    def get_doc_list(cls, params):
        sql = "select * from 352dt_doc_info where doc_user_id = %s order by utime desc"
        rows = mysql_utils.Database().query_all(sql, (params['uid'],))
        if rows is not None:
            doc_list = []
            for row in rows:
                doc = doc_model.Doc(docid=row[1], docname=row[2], doctype=row[3],
                                    docctime=row[6].strftime("%Y-%m-%d %H:%M:%S"),
                                    docutime=row[7].strftime("%Y-%m-%d %H:%M:%S"),
                                    docstate=None)
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
        if rows is not None:
            doc_type_list = []
            for row in rows:
                doc_type = dict(doctype=row[3], doctypename=row[4])
                doc_type_list.append(doc_type)
            return doc_type_list
        else:
            return None

    @classmethod
    def insert_doc_and_get_doc(cls, params):
        download_url = "http://" + str(uuid.uuid1()) + ".docx"
        sql1 = "insert into 352dt_doc_info(doc_id, doc_type, doc_name, doc_path, doc_user_id, ctime, utime) " \
               "values (uuid(), %s, %s, %s, %s, now(), now())"
        sql2 = "select * from 352dt_doc_info " \
               "where id = (select last_insert_id() from 352dt_doc_info limit 1)"
        row = mysql_utils.Database().insert_del_update_query_one(sql1, sql2,
                                                                 params1=(params['doctype'], params['docname'],
                                                                          download_url, params['uid']))
        return row
