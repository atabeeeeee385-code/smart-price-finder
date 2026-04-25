from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 💾 بيانات المنتجات (قبل وبعد)
products = {
    "iphone 13": {"price": 30000, "old_price": 32000},
    "laptop dell": {"price": 25000, "old_price": 27000},
    "rice": {"price": 30, "old_price": 35},
    "samsung tv": {"price": 15000, "old_price": 18000}
}

# الصفحة الرئيسية
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# البحث
@app.route('/search')
def search():
    query = request.args.get('product', '').lower()
    results = []

    for name, data in products.items():
        if query in name:
            current = data["price"]
            old = data["old_price"]

            # 🤖 نصيحة
            if current < old:
                advice = "🔥 اشتري دلوقتي"
            elif current > old:
                advice = "⏳ استنى السعر ينزل"
            else:
                advice = "😐 السعر ثابت"

            results.append({
                "name": name,
                "price": current,
                "old_price": old,
                "advice": advice
            })

    return jsonify(results)