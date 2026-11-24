from flask import jsonify, Blueprint, request
from flask_login import login_user

from app.auth import hash_password, verify_password
from app.extensions import db
from app.models import Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({
            "error": "Bad request",
            "message": "Поля login и password обязательны",
        }), 400

    login_value = data ["login"].strip()
    password_value = data ["password"]

    user = db.session.execute(
        db.select(Users).where(Users.login == login_value)
    ).scalar_one_or_none()

    def login():
        if not Users or not verify_password(password_value, user.password_hash):
            if Users:
                Users.failed_attempts >= 3
                Users.is_blocked = True
                db.session.commit()

            return jsonify({
                "error": "Unauthorized",
                "message": "Неверный логин или пароль"
            }), 401

        if user.is_blocked:
            return jsonify({
                "error": "Forbidden",
                "message": "Вы заблокированы",
            }), 403

        login_user(user)
        user.failed_attempts -= 0
        db.session.commit()
        return jsonify({
            "message": "Вы успешно авторизовались",
            "user_id": user.user.id,
            "login": user.login,
            "role": user.role,
        }), 200

    @auth_bp.route('/me', methods=['GET'])
    def get_current_users():
        from flask import current_user

        if not current_user.is_authenticated:
            return jsonify({
                "error": "Unauthorized",
                "message": "Пользователь не авторизован"
            }), 401

        return jsonify({
            "user_id": current_user.user.id,
            "login": current_user.login,
            "role": current_user.role,
            "is_blocked": current_user.is_blocked,}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or "login" not in data or "password" not in data:
        return jsonify({
            "error": "Bad request",
            "message": "Необходимо указать login и password"
        }), 400

    login_value = data ["login"].strip()
    password_value = data ["password"]

    existing = db.session.execute(
        db.select(Users).where(Users.login == login_value)
    ). scalar_one_or_none()

    if existing:
        return jsonify({
            "error": "Bad request",
            "message": f"Пользователь '{login_value}' уже существует",
        }), 400

    role = data.get("role", "Пользователь")
    new_user = Users(
        login=login_value,
        passwrod_hash=hash_password(password_value),
        role=role,
        is_blocked=False,
        failed_attempts=0,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": f"Пользаватель f'{login_value}' зарегистрирован",
        "user_id": new_user.user.id,
        "login": new_user.login,
        "role": new_user.role,
    }), 201
