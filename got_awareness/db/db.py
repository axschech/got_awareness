from pony.orm import *
from got_awareness.config import config
import bcrypt
import random

sql_debug(True)

db = Database();

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    email = Required(str, unique=True)
    password = Required(str)
    organization = Set('Organization')
    messages = Set('Message')

class Organization(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    code = Required(str, 5)
    user = Set('User')
    messages = Set('Message')

class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    body = Required(str)
    user = Required(User)
    organization = Required(Organization)

def dropTables():
  db.drop_all_tables(with_all_data=True)

def createTables():
  db.create_tables()

def hash(str):
  try:
    return bcrypt.hashpw(str.encode('utf-8'),bcrypt.gensalt())
  except Exception, e:
    return str(e)
  
db.bind('mysql', host=config.host, user=config.user, passwd=config.password, db=config.db)
db.generate_mapping(create_tables=True)
