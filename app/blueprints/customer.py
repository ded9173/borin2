import uuid
from flask import Blueprint, request, jsonify
from app.models import Customer
from app.extensions import db

customer = Blueprint('countreparties', __name__)

@customer.route('/countreparties', methods=['GET'])
def list_customer():
    countreparties = db.session.execute(db.select(Customer)).scalars().all()
    return jsonify({
        "customer":[
            {
                "customer_id": str(c.countreparties_id),
                "name": c.name,
                "inn": c.inn,
                "address": c.address,
                "phone": c.phone,
                "customer_type": c.countreparties_type,
                "created_ap": c.created_ap,
            }
            for c in countreparties
        ]
    }), 200

@customer.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or "name" not in data or "customer_type" not in data:
        return jsonify({
            "error": "Bad request",
            "message": "Необходимо указать name и customer_type",
        }), 400

    new_customer = Customer(
        name=data["name"],
        inn=data.get["inn"],
        address=data.get["address"],
        phone=data.get["phone"],
        customer_type=data["customer_type"],
    )
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({
        "message": "Клиент Создан",
        "client_id": str(new_customer.customer_id),
    }), 201

@customer.route('/customer_id', methods=['PUT'])
def get_customer_id(customer_id):

    try:
        customer_uuid = uuid.UUID(customer_id)
    except (ValueError, AttributeError):
        return jsonify({
            "error": "Bad request", "message": "Неверный формат UUID"})

    customer = db.session.get(Customer, customer_uuid)
    if not customer:
        return jsonify({"error": "Not found", "message": "Клиент не найден"}), 404
    return jsonify({
        "customer_id": str(customer.countreparties_id),
        "name": customer.name,
        "inn": customer.inn,
        "address": customer.address,
        "phone": customer.phone,
        "created_at": customer.created_at.isoformat() if customer.created_at else None,
        "countreparties_type": customer.countreparties_type,
    }), 200

@customer.route('/customer_id', methods=['PUT'])
def update_customer_id(customer_id):

    try:
        customer_uuid = uuid.UUID(customer_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Bad Request", "message":"Неверный формат UUID"}), 400

    customer = db.session.get(Customer, customer_uuid)
    if not customer:
        return jsonify({
            "error": "Not Found", "message":"Клиент не найден"
        }), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message":"Нет данных"}), 400

    customer.name = data.get("name", Customer.name)
    customer.inn = data.get("inn", Customer.inn)
    customer.customer = data.get("address", Customer.address)
    customer.phone = data.get("phone", Customer.phone)
    customer.counttreparties_type = data.get("countreparties_type", Customer.countreparties_type)

    db.session.commit()
    return jsonify({"message": "Клиент обновлен"}), 200


@customer.route('/countreparties_id', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer_uuid = uuid.UUID(customer_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Bad Request", "message":"Неверный формат UUID"}), 400

    customer = db.session.get(Customer, customer_uuid)
    if not customer:
        return jsonify({"error": "Not Found", "message":"Клиент найден"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Клиент найден"}), 200