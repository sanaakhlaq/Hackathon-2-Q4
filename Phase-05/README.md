# Phase-05: Kafka Integration

This phase adds Apache Kafka for real-time data streaming to your FastAPI application.

## Services

- **zookeeper**: Coordination service for Kafka
- **kafka**: Kafka broker for message queuing
- **ai-app**: Your main FastAPI application with Kafka integration
- **dapr-sidecar**: Dapr sidecar for distributed application runtime
- **kafka-test-producer**: Test producer to send sample messages
- **kafka-test-consumer**: Test consumer to receive and process messages

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Start all services:
   ```bash
   docker-compose up --build
   ```

2. The application will be available at `http://localhost:8000`
3. The Streamlit frontend will be available at `http://localhost:8501`
4. Dapr sidecar will be available at `http://localhost:3500`

### Testing Kafka Streaming

The setup includes a producer and consumer for testing:

1. The `kafka-test-producer` service sends sample messages to Kafka topics
2. The `kafka-test-consumer` service receives and logs messages from Kafka topics

You can monitor the logs to see the real-time data streaming:
```bash
docker-compose logs -f kafka-test-consumer
```

## Kafka Topics

The system uses three Kafka topics:

- `task-added`: For task creation events
- `user-events`: For user activity events
- `system-logs`: For system log events

## Architecture

All services run on the same Docker network (`app-network`) to ensure proper communication between components. The Kafka cluster (with Zookeeper) handles message queuing between different parts of the application.

## Files

- `docker-compose.yml`: Defines all services and their configuration
- `producer.py`: Sample Kafka producer implementation
- `consumer.py`: Sample Kafka consumer implementation
- `main.py`: Main FastAPI application with Kafka integration