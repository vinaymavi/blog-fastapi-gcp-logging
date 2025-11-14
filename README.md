# FastAPI GCP Logging with Structlog

A FastAPI application demonstrating structured logging with `structlog` for Google Cloud Platform (GCP) Cloud Logging. Each log level has a dedicated endpoint that accepts all HTTP methods.

## Features

- 🚀 FastAPI server with structured logging
- 📊 Integration with GCP Cloud Logging
- 🎯 Endpoints for each log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- 🔄 All endpoints accept all HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD)
- 📝 Structured JSON logs with request metadata
- ☁️ Automatic GCP log level mapping

## Endpoints

| Endpoint | Log Level | Methods |
|----------|-----------|---------|
| `/debug` | DEBUG | ALL |
| `/info` | INFO | ALL |
| `/warning` | WARNING | ALL |
| `/error` | ERROR | ALL |
| `/critical` | CRITICAL | ALL |
| `/` | INFO | GET |

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running Locally

```bash
# Run the server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --port 8080
```

The server will start on `http://localhost:8080`

## Testing Endpoints

```bash
# Test INFO endpoint with GET
curl http://localhost:8080/info

# Test ERROR endpoint with POST
curl -X POST http://localhost:8080/error -H "Content-Type: application/json" -d '{"test": "data"}'

# Test WARNING endpoint with PUT
curl -X PUT http://localhost:8080/warning

# Test DEBUG endpoint with DELETE
curl -X DELETE http://localhost:8080/debug

# Test CRITICAL endpoint with PATCH
curl -X PATCH http://localhost:8080/critical
```

## Deployment to GCP Cloud Run

```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy fastapi-logging-demo \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --platform managed
```

## GCP Cloud Logging Integration

When deployed to GCP, the application automatically:
- Sends logs to Google Cloud Logging
- Preserves log severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Includes structured metadata (method, path, client IP, request body)
- Formats logs as JSON for easy querying

### Viewing Logs in GCP

1. Go to [GCP Console > Logging](https://console.cloud.google.com/logs)
2. Filter by severity level
3. View structured fields in the JSON payload

## Log Format

Each log entry includes:
```json
{
  "event": "Log level message",
  "method": "GET",
  "path": "/info",
  "client_ip": "127.0.0.1",
  "body": null,
  "timestamp": "2024-01-01T12:00:00.000000Z",
  "level": "info"
}
```

## Environment Variables

- `PORT`: Server port (default: 8080)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP service account key (for local development)

## Use Cases

This repository serves as a reference for:
- Setting up structured logging in FastAPI
- Integrating Python applications with GCP Cloud Logging
- Understanding log level handling in production environments
- Building observable microservices
- Blog posts and tutorials on logging best practices

## License

MIT
