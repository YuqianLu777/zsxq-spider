from peewee import *
from datetime import datetime,timedelta
from time import sleep
from db_init import Topic
import os
from playhouse.migrate import *

db = SqliteDatabase('zsxq.db')

class Topic_test(Model):
    topic_id = CharField(unique=True)
    create_time = DateTimeField()
    group_id = CharField()
    topic_content = TextField()

    class Meta:
        database = db # This model uses the "zsxq.db" database.

class File_test(Model):
    file_id = CharField(unique=True)
    file_create_time = DateTimeField()
    file_name = CharField()
    topic_id = CharField()
    file_content = TextField()

    class Meta:
        database = db # this model uses the "zsxq.db" database

db.connect()
Topic_test.truncate_table(restart_identity=True)
File_test.truncate_table(restart_identity=True)
db.close()