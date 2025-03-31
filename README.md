# Sentiment Analysis MLOps Project

A production-ready sentiment analysis API built with FastAPI that analyzes text sentiment with comprehensive monitoring capabilities.

## Features

- **Sentiment Analysis API**: Predicts sentiment (positive, neutral, negative) for text inputs
- **Optimized Model Loading**: Uses singleton pattern to load model only once during startup
- **Comprehensive Monitoring**:
  - Prometheus metrics for request counts, latency, and endpoint usage
  - Grafana dashboards for visualization
  - Performance threshold alerts
- **Detailed Logging**: Request tracking, response times, and warning alerts
- **Docker Deployment**: Complete containerization with Docker Compose
- **Testing**: Extensive unit tests with pytest and coverage reporting

## Quick Start

### Prerequisites
- Python 3.9+ 
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/bilalbrar/Task-MLOps.git
cd Task-MLOps

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model (if not already present)
python scripts/train_pipeline.py --data_path data/Books_10k.jsonl --model_path models/sentiment_model.pkl

# Run the API
uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build and start all services (API, Prometheus, Grafana)
docker-compose up -d

# View running services
docker-compose ps

# Stop services
docker-compose down
```

## Accessing the Services

After starting the services, you can access:

- **API**: [http://localhost:8000](http://localhost:8000)
  - Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Health check: [http://localhost:8000/health](http://localhost:8000/health)
  - Status: [http://localhost:8000/status](http://localhost:8000/status)
  - Metrics: [http://localhost:8000/metrics](http://localhost:8000/metrics)

- **Prometheus**: [http://localhost:9090](http://localhost:9090)
  - Query example: `http_requests_total{endpoint="/api/v1/*"}`

- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Default credentials: admin/admin

## API Usage

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
    "sentences": [
        "I really enjoyed this product!",
        "This was a terrible experience.",
        "It's okay, nothing special."
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

Example response:
```json
{
  "predictions": ["positive", "negative", "neutral"]
}
```

## Project Structure

```
Task-MLOps/
├── app/
│   ├── api/                # API routes and schemas
│   ├── core/               # Configuration and logging
│   ├── services/           # Model service with singleton pattern
│   └── main.py             # FastAPI application
├── data/                   # Training data
├── models/                 # Trained model files
├── scripts/                # Training scripts
├── tests/                  # Unit tests
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-container setup
├── prometheus.yml          # Prometheus configuration
└── requirements.txt        # Python dependencies
```

## Monitoring & Metrics

The project includes a comprehensive monitoring setup:

- **Request metrics**: Count, latency, status codes
- **Endpoint usage**: Which endpoints are most frequently accessed
- **Performance monitoring**: Response time percentiles
- **Alerts**: Configurable thresholds for latency and error rates

### Example Prometheus Queries

#### 99th Percentile Latency by Endpoint and Method
```
histogram_quantile(
  0.99,
  sum by (le, method, endpoint) (rate(http_request_latency_seconds_bucket[1m]))
)
```
This query calculates the 99th percentile (p99) of request latency for each endpoint and HTTP method over the last minute. It shows the latency threshold below which 99% of requests complete, helping you identify performance bottlenecks and set realistic SLOs.

## Docker Setup

When running `docker-compose up --build`, the services are available at the following ports:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| HOST | API host | 0.0.0.0 |
| PORT | API port | 8000 |
| MODEL_PATH | Path to trained model | models/sentiment_model.pkl |
| LOG_LEVEL | Logging level | INFO |
| LOG_FILE | Log file location | logs/app.log |
| LATENCY_THRESHOLD_MS | Warning threshold for latency | 300 |

## Testing

Run the test suite with:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app
```



