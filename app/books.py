from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
ROLE = os.getenv('ROLE', 'primary')  # 'primary' or 'backup'
PEER_URL = os.getenv('PEER_URL')  # URL of the backup/primary node
CACHE_INVALIDATE_URL = os.getenv('CACHE_INVALIDATE_URL')  # URL to invalidate gateway cache

# Book data storage
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

def sync_with_peer(book_id, data):
    """Synchronize book data with peer node"""
    if not PEER_URL:
        logger.warning("No peer URL configured for sync")
        return
    
    try:
        url = f"{PEER_URL}/replica_sync/{book_id}"
        response = requests.put(url, json=data)
        if response.status_code == 200:
            logger.info(f"Successfully synced book {book_id} with peer")
        else:
            logger.error(f"Failed to sync with peer: {response.status_code}")
    except Exception as e:
        logger.error(f"Error syncing with peer: {str(e)}")

def notify_cache_invalidation(book_id):
    """Notify gateway to invalidate cache for a book"""
    if not CACHE_INVALIDATE_URL:
        return
    
    try:
        requests.post(CACHE_INVALIDATE_URL, json={"key": f"book:{book_id}"})
        logger.info(f"Cache invalidation notification sent for book {book_id}")
    except Exception as e:
        logger.error(f"Failed to notify cache invalidation: {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint with role information"""
    return jsonify({
        "status": "healthy",
        "service": "catalog",
        "role": ROLE,
        "timestamp": datetime.utcnow().isoformat(),
        "peer_configured": bool(PEER_URL)
    })

@app.route('/replica_sync/<int:item_number>', methods=['PUT'])
def replica_sync(item_number):
    """Handle sync requests from peer node"""
    if ROLE == 'primary':
        return jsonify({"error": "Primary node cannot accept sync requests"}), 403
        
    data = request.json
    book = find_book_by_id(item_number)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404
        
    if "price" in data:
        book["price"] = data["price"]
    if "quantity" in data:
        book["quantity"] = data["quantity"]
        
    logger.info(f"Synced book {item_number} from primary")
    return jsonify({"message": "Sync successful"})

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
    """Update book details with replication support"""
    # Only primary should handle write operations
    if ROLE != 'primary':
        return jsonify({"error": "Updates only allowed on primary node"}), 403
        
    data = request.json
    book = find_book_by_id(item_number)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if "price" in data:
        book["price"] = data["price"]
    if "quantity" in data:
        book["quantity"] = data["quantity"]

    # Sync with backup
    sync_with_peer(item_number, data)
    
    # Notify cache invalidation
    notify_cache_invalidation(item_number)
    
    logger.info(f"Updated book {item_number} on primary")
    return jsonify({"message": "Book updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
