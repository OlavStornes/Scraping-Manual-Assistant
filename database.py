import peewee as pw
import json


def set_up_systems_database(db):
    print("System database empty!")
    print("Creating system table...")

    data = {}

    with open('systems.json') as f:
        data = json.load(f)

    with db.atomic():
        for key, value in data.items():
            System.create(sys_id=key, name=value)

    print("Done! Created {} entries".format(System.select().count()))


db = pw.SqliteDatabase('database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class System(BaseModel):
    sys_id = pw.IntegerField(primary_key=True)
    name = pw.CharField()


class Game(BaseModel):
    game = pw.CharField()
    system = pw.ForeignKeyField(System, field='sys_id')
    publisher = pw.CharField()
    developer = pw.CharField()
    category = pw.CharField()
    year = pw.IntegerField()


# set_up_systems_database(db)

db.create_tables([Game, System])

if (System.select().count() == 0):
    set_up_systems_database(db)
