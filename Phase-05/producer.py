import asyncio
import json
import random
from aiokafka import AIOKafkaProducer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def produce_messages():
    # Initialize the Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',  # This matches the service name in docker-compose
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Start the producer
    await producer.start()
    logger.info("Kafka producer started successfully!")

    try:
        # Produce sample messages to different topics
        topics = ['task-added', 'user-events', 'system-logs']
        
        for i in range(20):  # Send 20 sample messages
            # Randomly select a topic
            topic = random.choice(topics)
            
            # Create a sample message based on the topic
            if topic == 'task-added':
                message = {
                    'event_type': 'task-added',
                    'task_id': i,
                    'task_name': f'Task {i}',
                    'description': f'Description for task {i}',
                    'priority': random.choice(['low', 'medium', 'high']),
                    'timestamp': asyncio.get_event_loop().time()
                }
            elif topic == 'user-events':
                message = {
                    'event_type': 'user-action',
                    'user_id': random.randint(1, 100),
                    'action': random.choice(['login', 'logout', 'update_profile', 'create_task']),
                    'timestamp': asyncio.get_event_loop().time()
                }
            else:  # system-logs
                message = {
                    'event_type': 'system-log',
                    'level': random.choice(['INFO', 'WARNING', 'ERROR']),
                    'message': f'System event #{i}',
                    'timestamp': asyncio.get_event_loop().time()
                }

            # Send message to Kafka
            await producer.send_and_wait(topic, message)
            logger.info(f"Sent message to topic '{topic}': {message}")
            
            # Wait a bit before sending the next message
            await asyncio.sleep(2)
            
    except Exception as e:
        logger.error(f"Error producing messages: {e}")
    finally:
        # Stop the producer
        await producer.stop()
        logger.info("Kafka producer stopped.")

if __name__ == "__main__":
    asyncio.run(produce_messages())