from flask import Flask, jsonify
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

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "catalog"})

# Search books by topic endpoint
@app.route('/search/<topic>', methods=['GET'])
def search_by_topic(topic):
    matching_books = [
        {"id": book["id"], "title": book["title"]}
        for book in BOOKS
        if book["topic"].lower() == topic.lower()
    ]
    return jsonify(matching_books)

# Get book info by item number endpoint
@app.route('/info/<int:item_number>', methods=['GET'])
def get_book_info(item_number):
    book = next((book for book in BOOKS if book["id"] == item_number), None)
    if book:
        return jsonify({
            "title": book["title"],
            "quantity": book["quantity"],
            "price": book["price"]
        })
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)
