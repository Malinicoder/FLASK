import requests
import os
from flask import Flask, jsonify
from config import Config 
from flask_jwt_extended import JWTManager, jwt_required 
app = Flask(__name__)
port = int(os.environ.get('PORT', 5001))
app.config.from_object(Config) 
jwt = JWTManager(app)

BASE_URL = "https://dummyjson.com/products"
@app.route('/products', methods=['GET'])

@jwt_required()
def get_products():


    response = requests.get(f"{BASE_URL}")
    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code
    products = []
    for product in response.json()['products']:
        product_data = {
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'description': product['description']
        }
        products.append(product_data)
    return jsonify({'data': products}), 200 if products else 204
if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=port)
