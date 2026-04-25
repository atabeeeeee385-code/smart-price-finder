from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/search')
def search():
    query = request.args.get('q')

    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    params = {
        "query": query,
        "country": "US",
        "page": "1"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    products = []

    try:
        for item in data['data']['products'][:5]:
            price = item.get('product_price', '0')
            price_num = int(''.join(filter(str.isdigit, price)) or 0)

            products.append({
                "name": item.get('product_title'),
                "price": price,
                "price_num": price_num,
                "image": item.get('product_photo'),
                "link": item.get('product_url')
            })
    except:
        return jsonify({"error": "في مشكلة في البيانات"})

    # مقارنة
    prices = [p["price_num"] for p in products if p["price_num"] > 0]

    advice = "❌ مش مستاهل"
    if prices:
        avg = sum(prices) / len(prices)
        min_price = min(prices)

        if min_price < avg:
            advice = "🔥 اشتري دلوقتي"
        else:
            advice = "⏳ استنى شوية"

    return jsonify({
        "products": products,
        "advice": advice
    })

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)