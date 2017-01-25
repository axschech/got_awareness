from flask import Flask, request, abort, jsonify
from db import db

import bcrypt
import random
import string
import json

app = Flask(__name__)

@app.route("/")
def hello():
    with db.db_session:
        return db.User[7].password + " " + bcrypt.hashpw("somewords", db.User[7].password.encode('utf-8'))
    # return "Hello World!"

@app.route("/api/register", methods=["POST"])
def register():
  try:
    with db.db_session:
      try:
          try:
            org = db.Organization[request.json['org']]
          except db.ObjectNotFound:
            return jsonify(error="Outlaws"), 401

          if str(request.json['code']) != str(org.code):
            return jsonify(error="Nightmare Hospital"), 401

          user = db.User(name=request.json['name'], email=request.json['email'], password=bcrypt.hashpw(request.json['password'].encode('utf-8'),bcrypt.gensalt()))
      except KeyError, e:
        return jsonify(error="Don't tell me what I can't " + str(e) + "!"), 401
  except Exception, e:
    # this is lit
    if "IntegrityError" in str(e):
      return jsonify(error="Hall Monitor"), 401
        
@app.route("/user")
def user():
    with db.db_session:
       return db.User.get(name=request.args.get('name')).email
    return ""
  
@app.route("/message")
def message():
    with db.db_session:
        user = db.User[1]
        org = db.Organization[1]
    
        msg = db.Message(body="Hey messaging", user=user, organization=org)
        msg.organization = org;
    return
  
if __name__ == "__main__":
    app.run()
