# _*_ coding:utf-8 _*_

# 文档类
class Doc:
    def __init__(self, docid=None, doctype=None, docname=None, docctime=None, docutime=None, docstate=None):
        self.docid = docid
        self.docname = docname
        self.doctype = doctype
        self.docctime = docctime
        self.docutime = docutime
        self.docstate = docstate

    def to_dict(self):
        return self.__dict__

