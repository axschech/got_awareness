from got_awareness.db import db
import random
import os

class Seeder:
  script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
  rel_path = 'names.txt'
  abs_file_path = os.path.join(script_dir, rel_path)
  names = []
  orgs = []
  raw = []
  code = '12345'
  
  def __init__(self):
    self.dropTables()
    self.getNames()
    
  def getNames(self):
    content = ''
    with open(self.abs_file_path) as f:
      content = f.readlines()
      content = [x.strip() for x in content]
    self.names = content
  
  def dropTables(self):
    db.dropTables()
    db.createTables()
    
  def createOrg(self):
    name = random.choice(self.names).replace(" ", '')
    code = self.code
    try:
      with db.db_session:
        try:
          db.Organization(name=name, code=code)
        except Exception, e:
          print str(e)
    except:
      pass
        
  def createUser(self):

    name = random.choice(self.names)
    password = name.lower().replace(" ", '')
    email = password + "@coolguy.com"
    try:
      with db.db_session:
        try:
          org = db.Organization.select_random(1)
          db.User(name=name, password=db.hash(password), email=email, organization=org)
          self.raw.append({'name': name, 'email': email, 'password': password})
        except Exception, e:
          print str(e)
    except:
      pass
  
#   def createMessage:
    
seeder = Seeder()
orgs = []

print "\n Creating Orgs \n"
for x in range(0, 10):
  seeder.createOrg()
  
print "\n Creating Users \n"
for x in range(0, 20):
  seeder.createUser()

for x in seeder.raw:
  print "\n"
  print x['name']
  print x['email']
  print x['password']
  print "\n"


