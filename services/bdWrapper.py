import sqlite3
from config import *
from services.log import *

def check_user_presence(chat_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM users WHERE telegram_chat_id = '{chat_id}';")
    res = cur.fetchall()
    return len(res) > 0


def create_user(chat_id, username):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO users(telegram_chat_id, telegram_username) 
       VALUES('{chat_id}', '{username}');""")
    conn.commit()
    return True

def create_request(chat_id, name, area, wifi, internal_model, external_model, wall_material, comments, plan, email):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO requests(user_id, name, area, internal_model, external_model, wall_material, comments, plan, email,wifi) 
       VALUES('{chat_id}', '{name}', '{area}', '{internal_model}', '{external_model}', '{wall_material}', '{comments}', '{plan}', '{email}','{wifi}');""")
    conn.commit()
    cur.execute(f"SELECT id FROM requests WHERE user_id = '{chat_id}' ORDER BY id DESC LIMIT 1;")
    res = cur.fetchone()
    return res[0]





def change_user_parametr(user_id, parametr_name, parametr_value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE users SET {parametr_name} = '{parametr_value}' WHERE telegram_chat_id = '{user_id}'""")
    conn.commit()
    return True

def change_request_parametr(user_id, parametr_name, parametr_value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE requests SET {parametr_name} = '{parametr_value}' WHERE id = '{user_id}'""")
    conn.commit()
    return True




def get_all_users():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users;")
    res = cur.fetchall()
    return res

def get_user_by_id(user_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE telegram_chat_id = '{user_id}';")
    res = cur.fetchone()
    return res

def get_request_by_id(user_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM requests WHERE id = '{user_id}';")
    res = cur.fetchone()
    return res

def get_user_by_username(chat_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE telegram_username = '{chat_id}';")
    res = cur.fetchone()
    return res

def add_news(news_id, user_id, msg_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO news(news_id, user_id, msg_id) 
       VALUES('{news_id}', '{user_id}', '{msg_id}');""")
    conn.commit()
    return True

def get_news_messages(news_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM news WHERE news_id = {news_id};")
    res = cur.fetchall()
    return res


def get_parameters():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM settings;")
    res = cur.fetchall()
    return res

def get_texts():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM texts;")
    res = cur.fetchall()
    return res

def get_parameter(parameter_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM settings WHERE id = {parameter_id};")
    res = cur.fetchone()
    return res



def get_setting(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM settings WHERE id = '{setting_id}';")
    res = cur.fetchall()
    return res[0][0]


def set_setting(setting_id, setting_value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE settings SET value = '{setting_value}' WHERE id = '{setting_id}'""")
    conn.commit()
    return True


def get_text(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM texts WHERE id = '{setting_id}';")
    res = cur.fetchall()
    return res[0][0]

def get_text_obj(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM texts WHERE id = '{setting_id}';")
    res = cur.fetchone()
    return res

def get_parameter_obj(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM settings WHERE id = '{setting_id}';")
    res = cur.fetchone()
    return res


def set_text(setting_id, value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE texts SET value = '{value}' WHERE id = '{setting_id}'""")
    conn.commit()
    return True


def get_request_by_user_id(user_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM requests WHERE user_id = '{user_id}';")
    res = cur.fetchone()
    return res


def delete_dannie(user_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    curs = conn.cursor()
    curs.execute(f'UPDATE requests SET ceiling_ar = null WHERE user_id={user_id}').fetchone()
    curs.execute(f'UPDATE requests SET wall_ar = null WHERE user_id={user_id}').fetchone()
    curs.execute(f'UPDATE requests SET omni = null WHERE user_id={user_id}').fetchone()
    curs.execute(f'UPDATE requests SET sector_ar = null WHERE user_id={user_id}').fetchone()
    curs.execute(f'UPDATE requests SET result = null WHERE user_id={user_id}').fetchone()
    conn.commit()
