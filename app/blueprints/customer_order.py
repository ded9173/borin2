from flask import Blueprint, jsonify
from app.models import CustomerOrder
from app.extensions import db

Customer_order = Blueprint('countreparties_orders', __name__)


@Customer_order.route("/", methods=['GET'])
def list_countreparties_orders():
    orders = db.session.execute(db.select(CustomerOrder)).scalars().all()
    return jsonify({
        'countreparties_orders': [{
            'id': str(o.countreparties_order_id),
            "order_number": o.order_number,
            "order_date": o.order_date.isoformat() if o.order_date else None,
            "countreparties_id": str(o.countreparties_id),
            "executor_id": str(o.executor_id),
            "total_amount": str(o.total_amount) if o.total_amount else None,
            "created_at": str(o.created_at) if o.created_at else None,

        }
        for o in orders
        ]
    }), 200