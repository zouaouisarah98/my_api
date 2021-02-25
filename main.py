from datetime import date, datetime
from flask import Flask, jsonify, request,render_template,redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo



app = Flask(__name__)
app.secret_key = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/planning.Users"
mongo = PyMongo(app)

@app.route('/',methods=['GET'])
def index():
    return 'hello world'

@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        _hash_pass = generate_password_hash(_password)
        id = mongo.db.Users.insert({'name':_name,'email':_email,'password':_hash_pass})
        resp = jsonify("user added ")
        resp.status_code = 200
        return resp
    else:
        return not_found()
@app.route('/add_tasks',methods=['POST'])
def add_tasks():
    _json = request.json
    _task = _json['task']
    _id_user = _json['id_user']
    _descrption = _json['descrption']


    if _task and _id_user and request.method == 'POST':
        startDate = datetime.now()
        id_task = mongo.db.tasks.insert({'task':_task,'id_user':_id_user,'descrption':_descrption,'data_time':startDate})
        resp = jsonify("task added ")
        resp.status_code = 200
        return resp
    else:
        return not_found()
@app.route('/tasks')
def tasks():
    tasks = mongo.db.tasks.find()
    resp = dumps(tasks)
    return resp


@app.route('/task/<id>')
def task(id):
    tsk = mongo.db.tasks.find({'id_user':id})
    resp = dumps(tsk)
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message': 'not found ' + request.url

    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
@app.route('/users')
def users():
    users = mongo.db.Users.find()
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.db.Users.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.Users.delete_one({'_id':ObjectId(id)})
    resp = jsonify("user deleted")
    resp.status_code = 200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and _id and request.method =='PUT':
        _hash_pass = generate_password_hash(_password)
        mongo.db.Users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name': _name, 'email': _email, 'password': _hash_pass}})
        resp = jsonify("user updated ")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/update_task/<id>',methods=['PUT'])
def update_task(id):
    _id = id
    _json = request.json
    _task = _json['task']
    _id_user = _json['id_user']
    _descrption = _json['descrption']

    if _task and _id_user and _descrption and _id and request.method =='PUT':
        startDate = datetime.now()
        mongo.db.tasks.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'task':_task,'id_user':_id_user,'data_time':startDate,'descrption':_descrption}})
        resp = jsonify("task updated ")
        resp.status_code = 200
        return resp
    else:
        return not_found()

if __name__ == "__main__":
    app.run(debug=True)
