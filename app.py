from flask import Flask, request, jsonify

app = Flask(__name__)

products = [
    {"name": "iphone 13", "price": 30000},
    {"name": "laptop dell", "price": 25000},
    {"name": "rice", "price": 30},
    {"name": "samsung tv", "price": 15000}
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('product').lower()

    results = []
    for p in products:
        if query in p['name']:
            results.append(p)

    return jsonify(results)

app.run()
