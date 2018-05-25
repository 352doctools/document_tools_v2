# _*_ coding:utf-8 _*_
# Filename: public_sentiment_part1.py
# Author: pang song
# python 3.6
# Date: 2017/10/30
# 学习flask框架

import os
from flask import Flask,request,make_response,render_template
from flask_bootstrap import Bootstrap
import datetime
from flask import Flask, request, url_for, send_from_directory
import deal_word
# from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['docx', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
bootstrap = Bootstrap(app)
# 设置上传目录为当前脚本目录
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16M

# 全局变量，用于储存文件名
STATIC_FILE_NAME = ""

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             file_url = url_for('uploaded_file', filename=filename)
#             return html + '<br><img src=' + file_url + '>'
#     return html



# 文件上传界面
@app.route('/index', methods=['GET', 'POST'])
def index():
    global STATIC_FILE_NAME
    if request.method == 'POST':
        # file = request.files['document']
        file = request.files['input-b2']
        if file and allowed_file(file.filename):
            STATIC_FILE_NAME = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # 处理文档
            deal_word.typesetting(file_path)
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file_url = url_for('uploaded_file', filename=filename)
            # return html + '<br><img src=' + file_url + '>'
    return render_template('index.html')

# 文件下载
@app.route("/downloader")
def downloader():
    global STATIC_FILE_NAME
    download_file_path = os.path.join(UPLOAD_FOLDER, '')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    filename = STATIC_FILE_NAME
    STATIC_FILE_NAME = ""
    return send_from_directory(download_file_path, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


if __name__ == '__main__':
    # 局域网访问调试
    app.run(host='0.0.0.0', port=8099, debug=True)
    # 本机调试
    # app.run(debug=True)