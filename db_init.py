from peewee import *
from datetime import date

db = SqliteDatabase('zsxq.db')

class Topic(Model):
    topic_id = CharField(unique=True)
    create_time = DateTimeField()
    group_id = CharField()
    topic_content = TextField()

    class Meta:
        database = db # This model uses the "zsxq.db" database.

class File(Model):
    topic_id = CharField(unique=True)
    file_name = CharField()
    file_content = TextField()

    class Meta:
        database = db # this model uses the "people.db" database
