from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Товары (штрих-код: (название, цена, категория))
PRODUCTS = {
    "123456": ("Хлеб", 50, "Товары без группы"),
    "654321": ("Молоко", 80, "Товары без группы"),
    "111222": ("Шоколад", 120, "Товары без группы"),
    "333444": ("Кофе", 250, "Разливные напитки"),
    "555666": ("Чай", 150, "Разливные напитки")
}

cart = []
discount = 0  # Скидка в %
payment_method = ""

@app.route('/')
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    barcode = data.get("barcode")
    if barcode in PRODUCTS:
        name, price, category = PRODUCTS[barcode]
        cart.append((name, price))
        return jsonify({"message": f"Добавлен: {name} - {price} руб.", "cart": cart})
    return jsonify({"error": "Товар не найден"}), 404

@app.route('/set_discount', methods=['POST'])
def set_discount():
    global discount
    data = request.json
    discount = data.get("discount", 0)
    return jsonify({"message": f"Скидка установлена: {discount}%"})

@app.route('/set_payment', methods=['POST'])
def set_payment():
    global payment_method
    data = request.json
    payment_method = data.get("method")
    return jsonify({"message": f"Выбран способ оплаты: {payment_method}"})

@app.route('/checkout', methods=['POST'])
def checkout():
    global cart, discount, payment_method
    total = sum(price for _, price in cart) * (1 - discount / 100)
    receipt = {"items": cart, "total": round(total, 2), "payment": payment_method}
    cart.clear()  # Очистка корзины
    return jsonify(receipt)

if __name__ == "__main__":
    app.run(debug=True)
