"""
Вся работа с дб и таблицами
"""
from peewee import *


db = SqliteDatabase('db.sqlite3')  # создание бд


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    telegram_id = IntegerField()


class SearchRequest(BaseModel):
    user = ForeignKeyField(User)
    first = CharField()
    second = CharField()
    third = CharField()


# создание таблиц, если их нет
User.create_table()
SearchRequest.create_table()
