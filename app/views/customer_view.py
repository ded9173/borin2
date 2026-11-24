import uuid
from flask import request, Blueprint

from app.blueprints import Customer
from app.views.base_views import BaseAPIView
from app.services.customer_servise import countrepartiesServise

Customer_bp = Blueprint("countreparties", __name__)

class CustomerListAPI(BaseAPIView):
    """Список и создание клиентов."""

    def __init__(self):
        self.service = countrepartiesServise()

    def get(self):
        """Список клиентов."""
        clients = self.service.get_all_dto()
        return self._success_response({"clients": [c.to_dict() for c in clients]})

    def post(self):
        """Создание клиента."""
        data = request.get_json()
        if not data or "name" not in data or "type" not in data:
            return self._error_response("Укажите name и type")

        try:
            Customer = self.service.create_client(
                name=data["name"], client_type=data["type"],
                inn=data.get("inn"), address=data.get("address"), phone=data.get("phone")
            )
            return self._success_response({"message": "Клиент создан", "client_id": Customer.client_id}, 201)
        except ValueError as e:
            return self._error_response(str(e))

class CustomerDetailAPI(BaseAPIView):
    """Получение, обновление, удаление клиента."""

    def __init__(self):
        self.service = CustomerServise()

    def get(self, client_id):
        """Получение клиента."""
        try:
            Customer_uuid = uuid.UUID(client_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        co = self.service.get_by_id_dto(Customer_uuid)
        if not Customer:
            return self._not_found_response("Клиент")
        return self._success_response(Customer.to_dict())

    def put(self, client_id):
        """Обновление клиента."""
        try:
            client_uuid = uuid.UUID(client_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        data = request.get_json()
        if not data:
            return self._error_response("Нет данных")

        try:
            client = self.service.update_client(
                client_uuid, name=data.get("name"), inn=data.get("inn"),
                address=data.get("address"), phone=data.get("phone"),
                client_type=data.get("client_type")
            )
            if not client:
                return self._not_found_response("Клиент")
            return self._success_response({"message": "Клиент обновлён"})
        except ValueError as e:
            return self._error_response(str(e))

    def delete(self, client_id):
        """Удаление клиента."""
        try:
            Customer_uuid = uuid.UUID(Customer_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        Customer = self.service.get_by_id(Customer_uuid)
        if not Customer:
            return self._not_found_response("Клиент")

        self.service.delete(Customer_uuid)
        return self._success_response({"message": "Клиент удалён"})

Customer_bp.add_url_rule("/", view_func=CustomerListAPI.as_view("countreparties_list"))
Customer_bp.add_url_rule("/<countreparties_id>", view_func=Customer.as_view("countreparties_detail"))