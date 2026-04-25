from flask import Flask, request, jsonify
import os

app = Flask(__name__)

products = [
    {"name": "iphone 13", "price": 30000},
    {"name": "laptop dell", "price": 25000},
    {"name": "rice", "price": 30},
    {"name": "samsung tv", "price": 15000}
]

@app.route('/')
def home():
    return "Smart Price Finder is running 🚀"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('product')

    if not query:
        return jsonify({"error": "please provide product"}), 400

    query = query.lower()

    results = []
    for p in products:
        if query in p['name']:
            results.append(p)

    return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))