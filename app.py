from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/search")
def search():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "لا يوجد كلمة بحث"}), 400

    try:
        url = "https://serpapi.com/search.json"

        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY")
        }

        response = requests.get(url, params=params)
        data = response.json()

        products = []

        for item in data.get("shopping_results", []):
            title = item.get("title", "").lower()

            # فلترة حسب البحث
            if query.lower() not in title:
                continue

            price_str = item.get("price", "")
            price_num = item.get("extracted_price", 0)

            # تحويل للجنيه
            usd_to_egp = 50
            price_egp = price_num * usd_to_egp if price_num else 0

            products.append({
                "title": item.get("title"),
                "price": price_str,
                "price_num": price_num,
                "price_egp": round(price_egp, 2),
                "link": item.get("link"),
                "image": item.get("thumbnail")
            })

        # ترتيب الأرخص
        products = sorted(
            products,
            key=lambda x: x["price_num"] if x["price_num"] > 0 else 999999
        )

        cheapest = products[0] if products else None

        # نصيحة
        advice = "❌ مش متاح"
        if products:
            prices = [p["price_num"] for p in products if p["price_num"] > 0]
            if prices:
                avg = sum(prices) / len(prices)
                if min(prices) < avg:
                    advice = "🔥 اشتري دلوقتي"
                else:
                    advice = "⏳ استنى شوية"

        return jsonify({
            "products": products,
            "cheapest": cheapest,
            "advice": advice
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)