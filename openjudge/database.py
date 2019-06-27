import peewee as pw
import random
import string


def random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(20))


db = pw.SqliteDatabase("db.sqlite3", pragmas={"foreign_keys": 1})


class Table(pw.Model):
    class Meta:
        database = db


class User(Table):
    name = pw.CharField(unique=True)
    pwd = pw.CharField()


class Token(Table):
    id = pw.CharField(
        unique=True, primary_key=True, default=random_string, max_length=20
    )
    user = pw.ForeignKeyField(User)


with db:
    db.create_tables([User])
