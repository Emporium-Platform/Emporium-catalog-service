from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hardcoded books data
BOOKS = [
    {
        "id": 1,
        "title": "How to get a good grade in DOS in 40 minutes a day",
        "topic": "distributed systems",
        "quantity": 10,
        "price": 30
    },
    {
        "id": 2,
        "title": "RPCs for Noobs",
        "topic": "distributed systems",
        "quantity": 8,
        "price": 25
    },
    {
        "id": 3,
        "title": "Xen and the Art of Surviving Undergraduate School",
        "topic": "undergraduate school",
        "quantity": 15,
        "price": 20
    },
    {
        "id": 4,
        "title": "Cooking for the Impatient Undergrad",
        "topic": "undergraduate school",
        "quantity": 12,
        "price": 22
    }
]

def find_book_by_id(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "catalog"})

@app.route('/search/<topic>', methods=['GET'])
def search_by_topic(topic):
    matching_books = [
        {"id": book["id"], "title": book["title"]}
        for book in BOOKS
        if book["topic"].lower() == topic.lower()
    ]
    return jsonify(matching_books)

@app.route('/info/<int:item_number>', methods=['GET'])
def get_book_info(item_number):
    book = find_book_by_id(item_number)
    if book:
        return jsonify({
            "title": book["title"],
            "quantity": book["quantity"],
            "price": book["price"]
        })
    return jsonify({"error": "Book not found"}), 404

@app.route('/update/<int:item_number>', methods=['PUT'])
def update_book(item_number):
    data = request.json
    book = find_book_by_id(item_number)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if "price" in data:
        book["price"] = data["price"]
    if "quantity" in data:
        book["quantity"] = data["quantity"]

    return jsonify({"message": "Book updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
