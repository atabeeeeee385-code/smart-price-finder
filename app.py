from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

products = [
    {"name": "iphone 13", "price": 30000},
    {"name": "laptop dell", "price": 25000},
    {"name": "rice", "price": 30},
    {"name": "samsung tv", "price": 15000}
]

# 👇 ده اللي ناقصك
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('product').lower()

    results = []
    for p in products:
        if query in p['name']:
            results.append(p)

    return jsonify(results)

app.run(host='0.0.0.0', port=10000)