# _*_ coding:utf-8 _*_
# Filename: data_import.py
# Author: pang song
# python 3.6
# Date: 2018/07/10
# 读取Excel 到 线上mysql

import pandas as pd
import numpy as np
import pymysql
from sshtunnel import SSHTunnelForwarder

# 通过ssh查询数据库
def init_ssh_mysql_connet():
    server = SSHTunnelForwarder(
        ssh_address_or_host=('39.105.61.38', 22),  # 指定ssh登录的跳转机的address
        ssh_username='root',  # 跳转机的用户
        ssh_password='352DocTools!',  # 跳转机的密码
        remote_bind_address=('127.0.0.1', 3306))
    server.start()
    myConfig = pymysql.connect(
        user="root",
        passwd="pangsongpangsong",
        host="127.0.0.1",
        db="352doc_tools_db",
        port=server.local_bind_port)
    return server, myConfig


# 读取数据从远程mysql 数据库
def read_mysql(server, myConfig, sql):

    cursor =myConfig.cursor()
    # 使用cursor()方法获取操作游标
    # sql = """show tables"""
    cursor.execute(sql)
    # 提交
    result = cursor.fetchall()
    myConfig.commit()
    # print(result)

    myConfig.close()
    server.close()
    return result

# 段落文本格式化为html格式
def deal_paragraph(data_frame, col_name, row_num):
    content = data_frame[col_name].values[row_num]
    # 如果是空值返回None
    if content is np.nan:
        return None

    paragraph_start = '<p style="text-indent:2em">'
    paragraph_row_end = '</p><p style="text-indent:2em">'
    paragraph_end = '</p>'


    # 如果首尾字符为换行，去掉换行
    if content[0] == '\n':
        content = content[1:]
    if content[-1] == '\n':
        content = content[:-1]

    # 替换段落中换行
    content = content.replace('\n', paragraph_row_end)
    content = paragraph_start + content + paragraph_end
    return content

# df数据格式化为html表格 参数，df数据，表格标题行号，表格行数，表格列数
def df_html_table(df, row_start, rows_num, cols_num):
    # row_start = 2
    # rows_num = 9
    # cols_num = 2
    html_table_start = '<table border = "1" cellpadding = "0" cellspacing = "0"><tbody>'
    html_table_end = '</tbody></table>'
    table_cell = ''
    table_content = ''
    for row in range(row_start + 1, row_start + rows_num + 1):
        for col in range(cols_num):
            # print(row, col, '------', df.loc[row].values[col])
            table_cell += '<td>' + df.loc[row].values[col] + '</td>'
            # print('------', table_cell)
        table_content += '<tr>' + table_cell + '</tr>'
        table_cell = ''
    table_content = html_table_start + table_content + html_table_end

    # print(table_content)
    return table_content

# df数据 批量 格式化为html表格，参数为df数据，返回表名和表内容(html格式)两个list
def df_html_tables(df):
    # 统计行列信息
    table_col_size = df.columns.size
    table_row_size = df.iloc[:, 0].size

    table_names = []
    table_contents = []
    for indexs in df.index:
        # print(indexs)
        row_values = df.loc[indexs].values[0]
        # print(row_values)
        # 获取所有表名
        if row_values is not np.nan and df.loc[indexs].values[1] is np.nan:
            # print(indexs, row_values)
            table_names.append(row_values)

            row_nums_temp = 0
            col_nums_temp = 0
            # 计算分表的列数
            for col_num in range(table_col_size):
                # print('ssss', df.loc[indexs + 1].values[col_num])
                if df.loc[indexs + 1].values[col_num] is np.nan:
                    col_nums_temp = col_num - 1
                    break
                col_nums_temp = table_col_size - 1
            # print('col_nums_temp', col_nums_temp)
            # 计算分表的行数
            for row_num in range(table_row_size):
                if indexs + row_num > table_row_size - 1:
                    row_nums_temp = row_num - 1
                    break
                if df.loc[indexs + row_num].values[0] is np.nan:
                    row_nums_temp = row_num - 1
                    break
            # print('row_nums_temp', row_nums_temp)

            # print(df_html_table(df, indexs, row_nums_temp, col_nums_temp + 1))
            table_contents.append(df_html_table(df, indexs, row_nums_temp, col_nums_temp + 1))
    return table_names, table_contents


if __name__ == "__main__":

    #读入
    file_path = "/Users/pinetree_mac/ps_use/start_up_business/doc_tools/文章模板/ipo/352内容梳理模板1-3章demo.xlsx"


    # df = pd.read_excel(file_path, sheet_name="表格", header = None)
    df = pd.read_excel(file_path, sheet_name="1-3章demo")

    # insertRow = pd.DataFrame([[np.nan, np.nan, np.nan]])
    # df = df.append(insertRow, ignore_index=True)
    col_names = ['章节代码', '1级标题', '2级标题', '3级标题', '4级标题', '5级标题', '内容类型', '内容']

    df_col_values = df['章节代码'].values
    print(type(df_col_values))
    print(df_col_values)

    for row in range(0, 10):
        print(df['章节代码'].values[row])

    exit()



    # content = df[0].values[1]
    content = df.loc[0].values[0]
    print(content)
    print(df.loc[16].values[0])
    print(df.loc[17].values[0])
    print(df.loc[18].values[0])
    exit()
    print("--------------------")

    t_names, t_content = df_html_tables(df)
    for i in range(len(t_names)):
        print(t_names[i])
        print(t_content[i])
    # print(content[80])
