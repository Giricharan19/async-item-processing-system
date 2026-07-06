# 🚀 Async Item Processing System

An asynchronous item processing system built using **Flask, RabbitMQ, Celery, SQLite, Python Threading, and Docker**.

## 📌 Features

- REST API using Flask
- Asynchronous background processing with Celery
- RabbitMQ as the message broker
- SQLite database for storing items
- Concurrent requests using Python Threading
- Dockerized RabbitMQ setup

---

## 🛠 Tech Stack

- Python
- Flask
- RabbitMQ
- Celery
- SQLite
- SQLAlchemy
- Pika
- Requests
- Docker Desktop

---

## 📂 Project Structure

```
processing_items/
│── app.py
│── tasks.py
│── celery_worker.py
│── models.py
│── config.py
│── requirements.txt
│── README.md
```

---

## 🔄 Workflow

```
Client
   │
   ▼
Flask API
   │
   ▼
SQLite (Pending)
   │
   ▼
RabbitMQ Queue
   │
   ▼
celery_worker.py
   │
   ▼
Celery Worker
   │
   ▼
SQLite (Completed)
```

---

## 🐳 Why Docker?

Docker runs RabbitMQ in an isolated container, eliminating the need to install **Erlang** and **RabbitMQ** manually. This makes the project portable and easy to set up on any machine.

Start RabbitMQ:

```bash
docker run -d --hostname rabbitmq --name rabbitmq \
-p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

RabbitMQ Dashboard:

```
http://localhost:15672
```

Username: `guest`

Password: `guest`

---

## 🧵 Why 5 Threads?

The GET API creates **5 threads** to make concurrent HTTP requests.

Without threading:
- 5 requests × 2 seconds ≈ **10 seconds**

With threading:
- All requests run simultaneously ≈ **2 seconds**

This demonstrates concurrent execution for I/O-bound tasks.

---

## ▶️ Running the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start RabbitMQ (Docker)

```bash
docker run -d --hostname rabbitmq --name rabbitmq \
-p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 3. Open Three Terminals

**Terminal 1 – Flask API**

```bash
python app.py
```

**Terminal 2 – RabbitMQ Consumer**

```bash
python celery_worker.py
```

**Terminal 3 – Celery Worker**

**Windows**

```bash
celery -A tasks:celery_app worker --pool=solo --loglevel=info
```

**Linux/Mac**

```bash
celery -A tasks:celery_app worker --loglevel=info
```

---

## 📬 API Endpoints

### POST /

Creates a new item and publishes it to RabbitMQ.

Example:

```json
{
  "item": "Laptop"
}
```

### GET /?delay_value=2

Creates 5 concurrent threads to demonstrate asynchronous request handling.

---

## 📖 Key Concepts

- Producer-Consumer Architecture
- Asynchronous Task Processing
- Message Queues
- Background Jobs
- Python Threading
- REST APIs
- Docker Containerization