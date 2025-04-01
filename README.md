# Sentiment Analysis MLOps Project

A production-ready sentiment analysis API built with FastAPI that analyses text sentiment with comprehensive monitoring and observability features.

## Features

- **Sentiment Analysis API**: Predicts sentiment (positive, neutral, negative) for text inputs
- **Optimised Model Loading**: Uses singleton pattern to load model only once during startup
- **Comprehensive Monitoring**:
  - Prometheus metrics for request counts, latency, and endpoint usage
  - Configurable bucket sizes for accurate latency measurement
  - Grafana dashboards for visualisation
  - Performance threshold alerts
- **Detailed Logging**: Request tracking, response times, and warning alerts
- **Docker Deployment**: Complete containerisation with Docker Compose
- **Testing**: Extensive unit tests with pytest and coverage reporting

## Quick Start

### Prerequisites
- Python 3.12+ 
- Docker and Docker Compose (for containerised deployment)
- Git

### Local Development

 Clone the repository

```bash
cd

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
docker-compose up --build

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

- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Default credentials: admin/admin

## API Usage

### Python Client Example

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

### Example Response

```json
{
  "predictions": ["positive", "negative", "neutral"],
  "processing_time_ms": 3.42
}
```

## Project Structure

```
sentiment-analysis/
├── app/
│   ├── api/                # API routes and schemas
│   │   ├── __init__.py
│   │   ├── routes.py       # API endpoint definitions
│   │   └── schemas.py      # Pydantic models for request/response
│   ├── core/               # Configuration and logging
│   │   ├── __init__.py
│   │   ├── config.py       # Application settings
│   │   ├── logging.py      # Logging configuration
│   │   └── metrics.py      # Prometheus metrics
│   ├── services/           # Model service with singleton pattern
│   │   ├── __init__.py
│   │   ├── model_service.py # Model inference service
│   │   └── singleton.py    # Singleton pattern for model
│   ├── __init__.py
│   └── main.py             # FastAPI application
├── data/                   # Training data directory
│   └── Books_10k.jsonl     # Example dataset (not included in repo)
├── logs/                   # Application logs
├── models/                 # Trained model files
├── scripts/                # Training and utility scripts
│   └── train_pipeline.py   # Data preprocessing and model training
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_api.py         # API tests
│   ├── test_logging.py     # Logging tests
│   ├── test_main.py        # Main app tests
│   ├── test_model.py       # Model tests
│   ├── test_model_service.py # Model service tests
│   ├── test_schemas.py     # Schema validation tests
│   └── test_singleton.py   # Singleton pattern tests
├── .env                    # Environment variables (create from .env.sample)
├── .gitignore              # Git ignore file
├── alert_rules.yml         # Prometheus alerting rules
├── docker-compose.yml      # Multi-container setup
├── Dockerfile              # Docker image definition
├── prometheus.yml          # Prometheus configuration
├── pyproject.toml          # Python project configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── setup.py                # Package installation
```

## Monitoring & Metrics

The project includes a comprehensive monitoring setup:

### Available Metrics

- **Request metrics**: Count, latency, status codes by endpoint
- **Endpoint usage**: Tracking which endpoints are most frequently accessed
- **Performance monitoring**: Response time percentiles (50th, 95th, 99th)
- **Alerts**: Configurable thresholds for latency and error rates

### Prometheus Metrics

The application exposes the following metrics:
- `http_requests_total` - Counter of total HTTP requests by method, endpoint, and status
- `http_request_latency_seconds` - Histogram of request latency by method and endpoint

### Prometheus Queries

#### 99th Percentile Latency by Endpoint
```
histogram_quantile(
  0.99,
  sum(rate(http_request_latency_seconds_bucket[1m])) by (le, method, endpoint)
)
```

#### Raw Latency Bucket Data
```
sum(rate(http_request_latency_seconds_bucket[1m])) by (le, method, endpoint)
```

### Grafana Dashboards

The project includes ready-to-use Grafana dashboards for:
- Request volume and throughput
- Response time distributions
- Error rates and status codes
- Endpoint popularity

## Performance Considerations

### Latency Measurement

The application measures latency in two ways:
1. **Middleware Metrics**: Captures the full request lifecycle, including middleware processing
2. **Processing Time**: Records just the model inference time in the API response

For accurate latency distributions, the histogram buckets are configured with fine-grained values for low latencies:
```python
buckets=[0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0]
```

### Model Loading

The singleton pattern ensures the model is loaded only once at application startup. This avoids:
- Duplicate model instances in memory
- Repeated disk reads
- Inference latency spikes

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| HOST | API host | 0.0.0.0 |
| PORT | API port | 8000 |
| MODEL_PATH | Path to trained model | models/sentiment_model.pkl |
| LOG_LEVEL | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| LOG_FILE | Log file location | logs/app.log |
| LATENCY_THRESHOLD_MS | Warning threshold for latency | 300 |
| DATA_PATH | Path to training data | data/Books_10k.jsonl |

## Testing

Run the test suite with:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app
```

### Test Coverage

The application includes tests for:
- API endpoints and response validation
- Model service and prediction logic
- Singleton pattern implementation
- Schema validation
- Middleware behaviour
- Error handling

## Monitoring Setup

### Alert Rules

The project includes predefined alert rules for Prometheus, located in `alert_rules.yml`. These include:

- **HighRequestLatency**: Triggered when p99 latency exceeds 300ms for over 1 minute

You can customise these rules by editing the `alert_rules.yml` file.

### Logs

Check logs for detailed error messages:
```bash
# View API logs
docker logs task-mlops-sentiment-analysis-1

# View Prometheus logs
docker logs prometheus
```

## Licence

MIT Licence

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
