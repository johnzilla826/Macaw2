from pathlib import Path
from peewee import SqliteDatabase, DatabaseProxy, Model, CharField

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
