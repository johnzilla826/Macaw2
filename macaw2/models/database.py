from pathlib import Path
from peewee import *

db_proxy = DatabaseProxy()

def init_db():
    docs = Path.home() / "Documents"
    docs.mkdir(exist_ok=True)

    db_path = docs / "macaw2.db"
    db = SqliteDatabase(db_path)
    db_proxy.initialize(db)
    return db


class BaseModel(Model):
    class Meta:
        database = db_proxy

class Account(BaseModel):
    id = CharField(unique=True, primary_key=True)
    name = CharField()
    type = CharField()

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    date = DateField()
    memo = CharField()

class Entry(BaseModel):
    id = IntegerField(primary_key=True)
    transaction = ForeignKeyField(Transaction, backref='entries', on_delete='CASCADE')
    account = ForeignKeyField(Account, backref='entries')
    debit = DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = DecimalField(max_digits=10, decimal_places=2, default=0)
