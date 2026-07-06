# Async Item Processing System

## Technologies
- Python
- Flask
- RabbitMQ (Docker)
- Celery
- SQLite
- Pika

## Run RabbitMQ

docker run -d --hostname rabbitmq --name rabbitmq ^
-p 5672:5672 ^
-p 15672:15672 ^
rabbitmq:3-management

RabbitMQ Dashboard:
http://localhost:15672

Username: guest
Password: guest

## Install

pip install -r requirements.txt

## Run

Terminal 1
python app.py

Terminal 2
python celery_worker.py

Terminal 3
celery -A tasks:celery_app worker --pool=solo --loglevel=info