import json
import pika
from models import db, Item
from config import Config
from tasks import celery_app, process_item_task

# Initialize database
from flask import Flask
from config import Config as AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)


def callback(ch, method, properties, body):
    """Callback function to process messages from RabbitMQ"""
    try:
        # Parse message
        data = json.loads(body)
        item_id = data.get('item_id')
        item_name = data.get('item')
        
        print(f"Received: {data}")
        
        process_item_task.delay(
        data["item_id"],
        data["item"]
        )
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing message: {e}")
        # Reject and requeue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    """Start RabbitMQ consumer"""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=Config.RABBITMQ_HOST)
        )
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
        
        # Set prefetch count to 1
        channel.basic_qos(prefetch_count=1)
        
        # Consume messages
        channel.basic_consume(
            queue=Config.RABBITMQ_QUEUE,
            on_message_callback=callback
        )
        
        print(f" Waiting for messages in queue: {Config.RABBITMQ_QUEUE}")
        print("Press CTRL+C to stop")
        
        channel.start_consuming()
        
    except Exception as e:
        print(f"Error starting consumer: {e}")
        raise


if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Start consumer
    start_consumer()