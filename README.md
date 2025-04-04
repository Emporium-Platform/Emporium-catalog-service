# Emporium Catalog Service

The Catalog Service is a crucial component of the Emporium platform, responsible for managing and providing access to the book inventory. It maintains information about books, including titles, prices, quantities, and topics.

## Features

- Book search by topic
- Detailed book information retrieval
- Inventory management
- Health check endpoint
- CORS support
- RESTful API design

## Tech Stack

- Python 3.9
- Flask web framework
- Flask-CORS for cross-origin resource sharing
- Docker support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Emporium-Platform/Emporium-catalog-service.git
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the service:
```bash
python run.py
```

## Environment Variables

The service can be configured using the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Flask environment mode (development/production) | development |
| PORT | Port number for the catalog service | 5000 |
| HOST | Host address to bind to | 0.0.0.0 |

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the service.

**Response**:
```json
{
    "status": "healthy",
    "service": "catalog"
}
```

### Search Books by Topic
```
GET /search/<topic>
```
Returns a list of books matching the specified topic.

**Parameters**:
- `topic` (path parameter): The topic to search for (e.g., "distributed systems")

**Response**:
```json
[
    {
        "id": 1,
        "title": "How to get a good grade in DOS in 40 minutes a day"
    },
    {
        "id": 2,
        "title": "RPCs for Noobs"
    }
]
```

### Get Book Information
```
GET /info/<item_number>
```
Retrieves detailed information about a specific book.

**Parameters**:
- `item_number` (path parameter): The unique identifier of the book

**Response**:
```json
{
    "title": "How to get a good grade in DOS in 40 minutes a day",
    "quantity": 10,
    "price": 30
}
```

### Update Book Details
```
PUT /update/<item_number>
```
Updates the price and/or quantity of a specific book.

**Parameters**:
- `item_number` (path parameter): The unique identifier of the book

**Request Body**:
```json
{
    "price": 35,
    "quantity": 15
}
```

**Response**:
```json
{
    "message": "Book updated successfully"
}
```

## Sample Book Data

The service comes pre-loaded with sample book data:

```json
[
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
```

## Running with Docker Compose

The catalog service is part of a multi-service Docker Compose setup that includes the gateway-service and order-service.

### Step 1: Start the Services
To build and run all services together, navigate to the project directory containing the docker-compose.yml file and run:

```bash
docker-compose up --build
```

This command will:
- Build fresh images for emporium-catalog-service and other related services
- Start each service in its own container and connect them over a shared network
- Expose the catalog service on port 5000

## Error Handling

The service includes comprehensive error handling:
- 404 errors for non-existent books
- Input validation
- Appropriate HTTP status codes and error messages

## Development

To run the service in development mode:

1. Set the environment to development:
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
```

2. Start the service:
```bash
python run.py
```

The service will automatically reload when changes are detected in the source code.
