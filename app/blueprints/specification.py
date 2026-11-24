from flask import Blueprint, request, jsonify
from app.models import Specification
from app.extensions import db

specification_bp = Blueprint('specification', __name__)




@specification_bp.route('/specification', methods=['GET'])
def list_specification():
    specifications = db.session.query(Specification).all()
    return jsonify({
        "specifications": [
            {
                "specification_id": str(s.spec_id),
                "quantity_per_unit": float(s.quantity_per_unit),
            }
            for s in specifications
        ]
    }), 200

@specification_bp.route('/specification', methods=['POST'])
def create_specification():
    data = request.get_json()
    if not data or "specification_id" not in data or "quantity_per_unit" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Укажите specification_id, quantity_per_unit ",
        }), 400

    new_specification = Specification(
        specification_id=data["specification_id"],
        quantity_per_unit=data["quantity_per_unit"]
    )
    db.session.add(new_specification)
    db.session.commit()

    return jsonify({
        "message": "Спецификация создана",
        "specification_id": str(new_specification.spec_id),}), 201



