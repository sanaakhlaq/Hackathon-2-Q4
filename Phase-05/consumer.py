import asyncio
import json
from aiokafka import AIOKafkaConsumer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_messages():
    # Initialize the Kafka consumer
    consumer = AIOKafkaConsumer(
        'task-added',      # Topic for task-related events
        'user-events',     # Topic for user-related events
        'system-logs',     # Topic for system logs
        bootstrap_servers='kafka:9092',  # This matches the service name in docker-compose
        group_id='test-group',  # Consumer group ID
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Start the consumer
    await consumer.start()
    logger.info("Kafka consumer started successfully! Listening for messages...")

    try:
        # Continuously listen for messages
        async for message in consumer:
            # Extract topic, partition, offset, and value
            topic = message.topic
            partition = message.partition
            offset = message.offset
            value = message.value
            
            # Log the received message
            logger.info(f"Received message | Topic: {topic} | Partition: {partition} | "
                       f"Offset: {offset} | Value: {value}")
            
            # Process the message based on topic
            if topic == 'task-added':
                logger.info(f"Processing task: {value.get('task_name', 'Unknown')}")
                # Add your task processing logic here
            elif topic == 'user-events':
                logger.info(f"Processing user event: {value.get('action', 'Unknown')}")
                # Add your user event processing logic here
            elif topic == 'system-logs':
                level = value.get('level', 'INFO')
                logger.log(
                    getattr(logging, level, logging.INFO),
                    f"System log: {value.get('message', 'No message')}"
                )
                
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        # Stop the consumer
        await consumer.stop()
        logger.info("Kafka consumer stopped.")

if __name__ == "__main__":
    asyncio.run(consume_messages())