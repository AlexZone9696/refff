from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

items = []
discount = 0  # Скидка в %

@app.route('/')
def home():
    return render_template("index.html")  # Отображение главной страницы

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    if name and price:
        items.append((name, price))
        return jsonify({"message": f"Добавлен: {name} - {price:.2f} руб."})
    return jsonify({"error": "Неверные данные"}), 400

@app.route('/remove_item', methods=['POST'])
def remove_item():
    data = request.json
    name = data.get("name")
    for item in items:
        if item[0] == name:
            items.remove(item)
            return jsonify({"message": f"Удалено: {name}"})
    return jsonify({"error": "Товар не найден"}), 404

@app.route('/set_discount', methods=['POST'])
def set_discount():
    global discount
    data = request.json
    discount = data.get("discount", 0)
    return jsonify({"message": f"Скидка установлена: {discount}%"})

@app.route('/checkout', methods=['POST'])
def checkout():
    global items, discount
    total = sum(price for _, price in items) * (1 - discount / 100)
    items.clear()  # Очистка чека
    return jsonify({"total": round(total, 2), "message": "Оплата прошла"})

if __name__ == "__main__":
    app.run(debug=True)
