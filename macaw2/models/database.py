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
    reversal_transaction = BooleanField(default=False)
    reversed_of = ForeignKeyField(
        "self", null=True, backref="reversal", on_delete="SET NULL"
    )

    class Meta:
        constraints = [
            Check(
                "(reversal_transaction = 0 AND reversed_of_id IS NULL) "
                "OR (reversal_transaction = 1 AND reversed_of_id IS NOT NULL)"
            ),
            SQL("UNIQUE(reversed_of_id)")
        ]


class Entry(BaseModel):
    id = IntegerField(primary_key=True)
    transaction = ForeignKeyField(Transaction, backref="entries", on_delete="CASCADE")
    account = ForeignKeyField(Account, backref="entries")
    debit = DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = DecimalField(max_digits=10, decimal_places=2, default=0)
