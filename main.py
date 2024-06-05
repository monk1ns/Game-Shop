from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util, ObjectId
import datetime
import os
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(24)


client = MongoClient("mongodb+srv://robert:m8DQGRrye175THlg@cluster0.joirnmx.mongodb.net/")

CORS(app)

db = client.GameShop
products = db.products
users = db.Register
tokenlist = db.tokenlist
orders = db.orders

@app.route('/orders', methods=["POST"])
def get_order():
    if request.method == 'POST':
        data = request.get_json()
        orders.insert_one(data)
        return json_util.dumps(data)

@app.route('/products', methods=['GET'])
def get_orders():
    if request.method == 'GET':
    
        query = {}
        car_type = request.args.getlist('type')

        if car_type:
            query["type"] = {"$in":car_type}

        result = products.find(query)
        car_list = list(result)
        return json_util.dumps(car_list)

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    existing_user = users.find_one({'email': data['email']})

    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    if data['user_type'] == 'individual':
        user = {
            'email': data['email'],
            'password': hashed_password,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'user_type': 'individual'
        }
    elif data['user_type'] == 'organization':
        user = {
            'email': data['email'],
            'password': hashed_password,
            'org_name': data['org_name'],
            'reg_number': data['reg_number'],
            'address': data.get('address', ''),
            'user_type': 'organization'
        }
    else:
        return jsonify({'message': 'Invalid user type'}), 400

    users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201


# Аутентификация и создание токена JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = users.find_one({'email': data['email']})

    if user:
        if bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            session['email'] = data['email']
            
            # Создание токена и сохранение его в базе данных
            token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.secret_key, algorithm='HS256')
            tokenlist.insert_one({'token': token})

            
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

# Выход (удаление токена из базы данных)
@app.route('/logout', methods=['POST'])
def logout():
    # Извлечение токена из заголовка Authorization
    token = request.headers.get('Authorization')
    if token:
        # Удаляем токен из базы данных
        result = tokenlist.delete_one({'token': token})
        if result.deleted_count == 1:
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'Token not found'}), 404
    else:
        return jsonify({'message': 'Token missing'}), 400

if __name__ == '__main__':
    app.run(debug=True)