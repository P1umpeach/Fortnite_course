import sqlite3
from flask import flash


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM user'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_user(self, course, name, telephone, news_permission):
        try:
            self.__cur.execute("INSERT INTO students VALUES(NULL, ?, ?, ?, ?)", (course, name, telephone, news_permission))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД"+str(e))
            return False

        return True

    def get_user(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE user_id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return []


