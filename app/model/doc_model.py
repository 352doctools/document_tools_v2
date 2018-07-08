# _*_ coding:utf-8 _*_


class Doc:
    def __init__(self, docid=None, docname=None, doctype=None, docctime=None, docutime=None, docstate=None):
        self.docid = docid
        self.docname = docname
        self.doctype = doctype
        self.docctime = docctime
        self.docutime = docutime
        self.docstate = docstate

    def to_dict(self):
        return self.__dict__

