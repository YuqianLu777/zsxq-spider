from orator import DatabaseManager
from orator import Model
import sqlite3

'''
mysql_config = {
    'default': 'local',
    'local': {
        'driver': 'sqlite',
        'host': 'localhost',
        'database': 'content',
        'user': 'root',
        'password': '',
        'prefix': '',
        'log_queries': True
    }
}

db = DatabaseManager(mysql_config)

def connect_db():
    db.set_default_connection('local')
    Model.set_connection_resolver(db)

def post_topics(group_id: int, text: str = '', creat_time: str = ''):
    query = db.table('topics').insert(group_id = group_id, text = text, creat_time = creat_time)

if __name__ == '__main__':
#    connect_db()

#    post_topics(121214, 'dfsdfdsfdsf', '1010101')'''

if __name__ == '__main__':
    db = sqlite3.connect('content.db')
    cursor = db.cursor()
    cursor.execute('insert into topics (group_id, text, creat_time) values (\'1212\', \'Michael\', \'20211213\')')
    cursor.close()
    db.commit()
    db.close()
