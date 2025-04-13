# filename: app.py
from flask import Flask, jsonify, request, send_from_directory
import random
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')

adjectives = ['Smart', 'Eco', 'Quick', 'Easy', 'Super', 'Ultra', 'Magic', 'Pro', 'Lite', 'Max']
nouns = ['Cleaner', 'Bottle', 'Speaker', 'Gadget', 'Helmet', 'Lamp', 'Device', 'Tool', 'Box', 'Kit']

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['GET'])
def generate_product_name():
    try:
        # Verify API key
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != f'Bearer {API_KEY}':
            return jsonify({
                'status': 'error',
                'message': 'Invalid or missing API key'
            }), 401

        # Get optional parameters
        count = request.args.get('count', default=1, type=int)
        if count < 1 or count > 5:
            count = 1
            
        # Generate multiple names if requested
        names = []
        for _ in range(count):
            name = random.choice(adjectives) + " " + random.choice(nouns)
            names.append(name)
            
        return jsonify({
            'status': 'success',
            'product_names': names if count > 1 else names[0]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
