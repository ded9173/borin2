import uuid

from flask import request, Blueprint

from app.models import Items
from app.views.base_views import BaseAPIView
from app.services.items_service import  ItemService

items_db = Blueprint("items", __name__)

class ItemsListAPI(BaseAPIView):
    """Список и создание ."""

    def __init__(self):
        self.service = ItemService()

    def get(self):
        """Список ."""
        items = self.service.get_all_dto()
        return self._success_response({"items": [m.to_dict() for m in items]})

    def post(self):
        """Создание материала."""
        data = request.get_json()
        if not data or "name" not in data or "code" not in data:
            return self._error_response("Укажите name и code")

        try:
            items = self.service.create_material(name=data["name"], code=data["code"])
            return self._success_response({"message": "Материал создан", "material_id": items.material_id}, 201)
        except ValueError as e:
            return self._error_response(str(e))



class ItemsDetailAPI(BaseAPIView):
    """Получение, обновление, удаление ."""

    def __init__(self):
        self.service = ItemService()

    def get(self, material_id):
        """Получение ."""
        try:
            items_uuid = uuid.UUID(material_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        items = self.service.get_by_id_dto(items_uuid)
        if not items:
            return self._not_found_response("Материал")
        return self._success_response(items.to_dict())

    def put(self, items_id):
        """Обновление ."""
        try:
            material_uuid = uuid.UUID(items_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        data = request.get_json()
        if not data:
            return self._error_response("Нет данных")

        try:
            items = self.service.update_item(material_uuid, name=data.get("name"), code=data.get("code"))
            if not items:
                return self._not_found_response("Материал")
            return self._success_response({"message": "Материал обновлён"})
        except ValueError as e:
            return self._error_response(str(e))

    def delete(self, material_id):
        """Удаление"""
        try:
            material_uuid = uuid.UUID(material_id)
        except (ValueError, AttributeError):
            return self._error_response("Неверный формат UUID")

        material = self.service.get_by_id(material_uuid)
        if not material:
            return self._not_found_response("Материал")

        self.service.delete(material_uuid)
        return self._success_response({"message": "Материал удалён"})

Items.add_url_rule("/", view_func=itemsListAPI.as_view("materials_list"))
Items.add_url_rule("/<material_id>", view_func=itemsListAPI.as_view("material_detail"))
