from flask import Blueprint, jsonify
from app.models import Production_Order
from app.extensions import db
production_Order = Blueprint('production_orders', __name__)


@production_Order.route("/", methods=['GET'])
def list_countreparties_orders():
    orders = db.session.execute(db.select(Production_Order)).scalars().all()
    return jsonify({
        'production_Orders': [{
            'id': str(o.production_Order_id),
            "id_items": o.id_items,
            'cost_price':  o.cost_price,
            "quan": str(o.executor_id),
            " quantity": str(o. quantitly) if o.total_amount else None,
            "created_at": str(o.created_at) if o.created_at else None,

        }
        for o in orders
        ]
    }), 200