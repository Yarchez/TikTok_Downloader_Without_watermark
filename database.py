import sqlite3
from datetime import datetime


def create_table_convertations():
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS convertations (id integer PRIMARY KEY, telegram_id BIGINT, register_date TEXT, '
        'status TEXT)')
    connection.commit()
    connection.close()


def add_convertation(telegram_id, status):
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    cursor.execute('INSERT INTO convertations(telegram_id, register_date, status) VALUES(?,?,?)',
                   (telegram_id, dt_string, status))
    connection.commit()
    connection.close()


def get_convertations():
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM convertations')
    data = cursor.fetchall()
    connection.close()
    info = ''
    for i in data:
        info += f'data: {i}\n'
    return info


def create_table_users():
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, telegram_id BIGINT, username TEXT, register_date '
        'TEXT)')
    connection.commit()
    connection.close()


def add_user(telegram_id, username):
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE telegram_id = ? ', (telegram_id,))
    data = cursor.fetchone()
    print(data)
    if data is not None:
        connection.close()
        return
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    cursor.execute('INSERT INTO users(telegram_id, username, register_date) VALUES(?,?,?)',
                   (telegram_id, username, dt_string))
    connection.commit()
    connection.close()


def get_users():
    connection = sqlite3.connect('tiktok.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    connection.close()
    info = ''
    for i in data:
        info += f'data: {i}\n'
    return info