# _*_ coding:utf-8 _*_

from flask import render_template, request

from . import main


@main.route('/test', methods=['GET', 'POST'])
def test():
    return '<h1>Hello 3下5除2 在线小工具!</h1>'


@main.route('/base')
def base():
    return render_template('base.html')


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404