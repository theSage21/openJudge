import peewee as pw
import random
import string
from datetime import datetime


def random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


db = pw.SqliteDatabase("db.sqlite3", pragmas={"foreign_keys": 1})


class Table(pw.Model):
    class Meta:
        database = db


class User(Table):
    name = pw.CharField(unique=True)
    pwd = pw.CharField()


class Token(Table):
    id = pw.CharField(
        unique=True, primary_key=True, default=random_string, max_length=10
    )
    user = pw.ForeignKeyField(User)


class Language(Table):
    name = pw.CharField()
    shell_cmd = pw.CharField()
    memory_multiplier = pw.FloatField()
    time_multiplier = pw.FloatField()


class Program(Table):
    code = pw.TextField()
    language = pw.ForeignKeyField(Language)
    author = pw.ForeignKeyField(User)


class Question(Table):
    statement = pw.TextField()
    solution = pw.ForeignKeyField(Program)
    mem_limit = pw.IntegerField()
    time_limit = pw.IntegerField()


class Contest(Table):
    title = pw.CharField()
    description = pw.TextField()
    host = pw.ForeignKeyField(User)
    start = pw.DateTimeField()
    end = pw.DateTimeField()
    is_published = pw.BooleanField()


class ContestQuestion(Table):
    contest = pw.ForeignKeyField(Contest)
    question = pw.ForeignKeyField(Question)


class TestCase(Table):
    question = pw.ForeignKeyField(Question)
    inp = pw.TextField()
    out = pw.TextField()


class Attempt(Table):
    program = pw.ForeignKeyField(Program)
    testcase = pw.ForeignKeyField(TestCase)
    # ------------------------------
    is_being_checked = pw.BooleanField(default=False)
    is_checked = pw.BooleanField(default=False)
    stamp = pw.DateTimeField(default=datetime.utcnow)


class AttemptCheck(Table):
    id = pw.CharField(
        unique=True, primary_key=True, default=random_string, max_length=10
    )
    attempt = pw.ForeignKeyField(Attempt)
    stdout = pw.TextField(null=True)
    stderr = pw.TextField(null=True)
    exit_code = pw.IntegerField(null=True)
    is_timeout = pw.BooleanField(default=False)


with db:
    db.create_tables(
        [
            User,
            Token,
            Language,
            Program,
            Question,
            Contest,
            ContestQuestion,
            TestCase,
            Attempt,
            AttemptCheck,
        ]
    )
