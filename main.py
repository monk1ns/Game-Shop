from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import jwt
from bson import json_util, ObjectId
import datetime
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
            query["type"] = {"$in": car_type}

        result = products.find(query)
        car_list = list(result)
        return json_util.dumps(car_list)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = users.find_one({'email': data['email']})

    if user:
        if bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            session['email'] = data['email']
            
            token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.secret_key, algorithm='HS256')
            tokenlist.insert_one({'token': token})
            
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if token:
        result = tokenlist.delete_one({'token': token})
        if result.deleted_count == 1:
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'Token not found'}), 404
    else:
        return jsonify({'message': 'Token missing'}), 400

@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = products.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Failed to delete product. Error: {str(e)}'}), 500

@app.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        result = products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': data}
        )
        if result.matched_count == 1:
            return jsonify({'message': 'Product updated successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Failed to update product. Error: {str(e)}'}), 500



@app.route('/products', methods=['POST'])
def add_product():
    if request.method == 'POST':
        data = request.get_json()
        # Insert logic to add the product to MongoDB
        products.insert_one(data)
        return jsonify({'message': 'Product added successfully'}), 201
    else:
        return jsonify({'message': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
