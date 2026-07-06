from celery import Celery
from flask import Flask

from models import db, Item
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Celery
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest:guest@localhost:5672//",
    backend="rpc://"
)

@celery_app.task(name="process_item_task")
def process_item_task(item_id, item_name):
    """Process item and update status to completed"""

    with app.app_context():
        try:
            item = Item.query.get(item_id)

            if item:
                item.status = "completed"
                db.session.commit()

                print(f" Updated item {item_id}")

                return {
                    "status": "success",
                    "item_id": item_id,
                    "item": item_name,
                }

            return {
                "status": "error",
                "message": "Item not found",
            }

        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": str(e),
            }