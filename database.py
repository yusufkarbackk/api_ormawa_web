import mysql.connector


def get_my_sql_connection():
    return mysql.connector.connect(user='root', host='localhost', port=8889, password='root', database='ormawa')
