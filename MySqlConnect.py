# !/usr/bin/python3

import pymysql

dbInfo = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'ai',
    'charset': 'utf8'
}


def select(dbInfo, sql):
    # 打开数据库连接
    db = pymysql.connect(**dbInfo)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    finally:
        # 关闭数据库连接
        db.close()
    return results


def select(sql):
    # 打开数据库连接
    db = pymysql.connect(**dbInfo)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    finally:
        # 关闭数据库连接
        db.close()
    return results


def edit(sql):
    # 打开数据库连接
    db = pymysql.connect(**dbInfo)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交操作
        db.commit()
    except Exception as e:
        print(e)
        print("Error: unable to fetch data")
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()
# results=select("select * from dt_hiddendanger_record")
# for row in results:
#     print(row)
