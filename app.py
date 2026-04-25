from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# الصفحة الرئيسية (index.html)
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# API للبحث عن الأسعار
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
            "api_key": os.getenv("RAPIDAPI_KEY")  # لازم تحط المفتاح في Railway
        }

        response = requests.get(url, params=params)
        data = response.json()

        products = []

        for item in data.get("shopping_results", []):
            price = item.get("price", "")
            price_num = 0

            if price:
                # نحاول نحول السعر لرقم
                try:
                    price_num = float(
                        price.replace("EGP", "")
                             .replace("جنيه", "")
                             .replace(",", "")
                             .strip()
                    )
                except:
                    price_num = 0

            products.append({
                "title": item.get("title"),
                "price": price,
                "link": item.get("link"),
                "image": item.get("thumbnail"),
                "price_num": price_num
            })

        # تحليل الأسعار
        prices = [p["price_num"] for p in products if p["price_num"] > 0]

        advice = "❌ مش متاح"

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

    except Exception as e:
        return jsonify({
            "error": "حصلت مشكلة",
            "details": str(e)
        })


# التشغيل على Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)