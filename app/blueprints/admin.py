from flask import  Blueprint, request, jsonify
from flask_login import current_user, login_required

from app.auth import hash_password
from app.models import Users
from app.extensions import db

admin_bp = Blueprint('admin', __name__)

def _require_admin():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized', 'message': 'Неоьходима авторизация'}), 401
    if not current_user.role != 'admin':
        return jsonify({'error': 'Forbidden', 'message': "Доступ запрещен"}), 403
    return None

@admin_bp.before_request('/users/', methods=['GET'])
def list_users():
    admin_check = _require_admin()
    if admin_check:
        return admin_check
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Укажите login и password'}), 400

    login_value = data['login'].strip()
    password_value = data['password']

    if not login_value or not password_value:
        return jsonify({'error': 'Bad Request', 'message': 'Поля обезательны'}), 400

    existing_user = db.session.execute(
        db.session.query(Users).filter_by(login=login_value)
    ).scalar_one_or_none()

    if existing:
        return jsonify({'error': 'Bad Request', 'message': f'Пользователь "{login_value}"сушествует'})

    role = data.get('role', 'Пользователь')
    if role not in ('Администратор', 'Пользователь'):
        return jsonify({'error': 'Bad Request', 'message': 'Неверная роль'}), 400

    new_users = Users(
        login=login_value,
        password_hash=hash_password(password_value),
        role=role,
        is_blocked=False,
        failed_attempts=0
    )
    db.session.add(new_users)
    db.session.commit()

    return jsonify({'message': f'Пользователь {login_value} создан',
                   'user_id': new_users.id}), 201

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def update_user(user_id):
    admin_check = _require_admin()
    if admin_check:
        return admin_check

    user = db.session.query(Users).filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'Not found', 'massage': 'Пользователь не найден'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not found', 'massage': 'Нет данных'}), 400

    if 'role' in data:
        new_role = data['role']
        if new_role not in("Администратор", "Пользователь"):
            return jsonify({'error': 'Not found', 'massage': 'Неверная роль'}), 400

    user.role = new_role

    if 'is_blocked' in data:
        user.is_blocked = data['is_blocked']
        if not data['is_blocked']:
            user.failed_attempts = 0

        db.session.commit()
        return jsonify({'massage': 'Данные обновлены'}), 200


@admin_bp.route('/users/<int:user_id>', methods=['delete'])
@login_required
def delete_user(user_id):
    admin_check = _require_admin()
    if admin_check:
        return admin_check

    if user_id == current_user.id:
        return jsonify({'error': 'Not found', 'massage': 'Нельзя удалить себя'}), 400

    user = db.session.get(Users, user_id)
    if not user:
        return jsonify({'error': 'Not found', 'massage': 'Пользователь не найден'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'error': 'Not found', 'massage': 'удолен'}), 200