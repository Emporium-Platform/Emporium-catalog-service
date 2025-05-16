# Emporium Catalog Service

A Flask-based microservice that provides book catalog functionality with replication support for the Emporium online bookstore.

## Features

- Primary-Backup replication architecture
- Automatic synchronization between replicas
- Cache invalidation notifications
- Role-based behavior (primary/backup)
- REST API endpoints for book management

## Environment Variables

- `ROLE`: 'primary' or 'backup'
- `PEER_URL`: URL of the other replica
- `CACHE_INVALIDATE_URL`: Gateway's cache invalidation endpoint

## API Endpoints

### Search Books by Topic
```
GET /search/<topic>
Response: Array of books matching the topic
```

### Get Book Info
```
GET /info/<item_number>
Response: Book details (title, quantity, price)
```

### Update Book (Primary Only)
```
PUT /update/<item_number>
Body: { "price": number, "quantity": number }
Response: Success/failure message
```

### Health Check
```
GET /health
Response: Service health and role information
```

### Replica Sync (Backup Only)
```
PUT /replica_sync/<item_number>
Body: Updated book details
Internal endpoint for primary-backup synchronization
```

## Running the Service

1. Start primary instance:
```bash
docker-compose up catalog-primary
```

2. Start backup instance:
```bash
docker-compose up catalog-backup
```

## Implementation Notes

- Only primary handles write operations
- Backup automatically stays in sync with primary
- Strong consistency model ensures data integrity
- Cache invalidation keeps gateway's cache consistent
