# -*- coding: utf-8 -*-
import pymysql

class Dao(object):
    cursor = None
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '',
        'charset':'utf8mb4',
        'db':'football',
        'autocommit': True,
        'cursorclass':pymysql.cursors.DictCursor
    }

    @staticmethod
    def init():
        conn = pymysql.connect(**Dao.config)
        Dao.cursor = conn.cursor()

    @staticmethod
    def create_sofifa_player():
        sql = """
        create table if not exists sofifa_player (
            id varchar(8) not null,
            full_name varchar(40),
            name varchar(25),
            birthday varchar(8),
            nationality int,
            position varchar(15),
            height int,
            weight int,
            foot varchar(1),
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def create_sofifa_rating():
        sql = """
        create table if not exists sofifa_rating (
            id varchar(8) not null,
            rating json,
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def create_sofifa_nationality():
        sql = """
        create table if not exists sofifa_nationality (
            id varchar(3) not null,
            name varchar(50),
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def upsert_sofifa_player(param):
        sql = """
        insert into sofifa_player values(%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        on duplicate key update full_name = %s, name = %s, birthday = %s, 
        nationality = %s, position = %s, height = %s, weight = %s, foot = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_sofifa_rating(param):
        sql = """
        insert into sofifa_rating values(%s, %s) 
        on duplicate key update rating = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_nationality(param):
        sql = """
        insert into sofifa_nationality values(%s, %s) 
        on duplicate key update name = %s
        """
        Dao.cursor.execute(sql, param)