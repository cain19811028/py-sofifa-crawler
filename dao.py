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
            name varchar(20),
            birthday varchar(8),
            nationality int,
            position json,
            height int,
            weight int,
            foot varchar(1),
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def create_rating():
        sql = """
        create table if not exists rating (
            id varchar(8) not null,
            rating json,
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)