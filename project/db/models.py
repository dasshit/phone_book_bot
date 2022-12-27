import peewee


database = peewee.SqliteDatabase('data.db')


class BaseModel(peewee.Model):

    class Meta:
        database = database


class User(BaseModel):

    user_name = peewee.TextField(null=True)
    first_name = peewee.TextField(null=True)
    last_name = peewee.TextField(null=True)


class Contact(BaseModel):

    user = peewee.ForeignKeyField(User, backref='contacts')
    first_name = peewee.TextField()
    last_name = peewee.TextField()
    phone = peewee.TextField()
    contact_type = peewee.TextField()


database.create_tables([
    User,
    Contact
])
