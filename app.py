from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# =========================
# تحسين البحث (ذكي)
# =========================
def improve_query(q):
    q = q.lower().strip()

    stop_words = [
        "عايز","اريد","محتاج","هات","جيب",
        "افضل","احسن","كويس","حلو",
        "في","من","على","لي","لل"
    ]

    for w in stop_words:
        q = q.replace(w, "")

    try:
        from deep_translator import GoogleTranslator
        q = GoogleTranslator(source='auto', target='en').translate(q)
    except:
        pass

    q = f"{q} buy online best price"
    return q


# =========================
# الصفحة الرئيسية
# =========================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================
# API البحث
# =========================
@app.route("/search")
def search():
    query = request.args.get("q")
    min_price = request.args.get("min")
    max_price = request.args.get("max")
    sort = request.args.get("sort")

    if not query:
        return jsonify({"error": "لا يوجد بحث"}), 400

    query = improve_query(query)

    try:
        url = "https://serpapi.com/search.json"

        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY"),  # 🔥 مهم جدا
            "gl": "us",
            "hl": "ar"
        }

        res = requests.get(url, params=params)
        data = res.json()

        # لو المفتاح غلط
        if "error" in data:
            return jsonify({"error": data["error"]})

        products = []

        for item in data.get("shopping_results", []):
            price = item.get("price", "")
            price_num = item.get("extracted_price", 0)

            products.append({
                "title": item.get("title"),
                "price": price if price else "غير معروف",
                "price_num": price_num if price_num else 0,
                "link": item.get("link"),
                "image": item.get("thumbnail")
            })

        # فلترة السعر
        if min_price:
            products = [p for p in products if p["price_num"] >= float(min_price)]

        if max_price:
            products = [p for p in products if p["price_num"] <= float(max_price)]

        # ترتيب
        if sort == "cheap":
            products.sort(key=lambda x: x["price_num"])
        elif sort == "expensive":
            products.sort(key=lambda x: x["price_num"], reverse=True)

        # نصيحة
        prices = [p["price_num"] for p in products if p["price_num"] > 0]
        advice = "❌ مش متاح"

        if prices:
            avg = sum(prices) / len(prices)
            advice = "🔥 اشتري دلوقتي" if min(prices) < avg else "⏳ استنى شوية"

        return jsonify({
            "products": products,
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# تشغيل
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)