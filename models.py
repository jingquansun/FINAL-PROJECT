import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    journal_id = IntegerField(primary_key=True)
    title = TextField(unique=True)
    created = DateField(default=datetime.datetime.now)
    time_spent = IntegerField(null=False)
    learned = TextField(null=False)
    to_remember = TextField(null=False)

    class Meta:
        database = DATABASE
        order_by = ('-created',)

    @classmethod
    def create_entry(cls, title, time_spent, learned, to_remember):
        with DATABASE.transaction():
            try:
                with DATABASE.transaction():
                    cls.create(title=title,
                               created=datetime.datetime.now,
                               time_spent=time_spent,
                               learned=learned,
                               to_remember=to_remember)
            except IntegrityError:
                raise ValueError("Entry already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()


if __name__ == "__main__":
    initialize()

