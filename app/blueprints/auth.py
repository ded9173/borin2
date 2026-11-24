"""JSON authentication endpoints."""
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select
from app.auth import hash_password, verify_password
from app.extensions import db
from app.models import Users

auth_bp = Blueprint("auth", __name__)


def _payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


@auth_bp.post("/login")
def login():
    data = _payload()
    if not data or not isinstance(data.get("login"), str) or not isinstance(data.get("password"), str):
        return jsonify(error="Укажите login и password"), 400
    user = db.session.execute(select(Users).where(Users.login == data["login"].strip())).scalar_one_or_none()
    if user is None or not verify_password(data["password"], user.password_hash):
        if user is not None:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.is_blocked = True
            db.session.commit()
        return jsonify(error="Неверный логин или пароль"), 401
    if user.is_blocked:
        return jsonify(error="Учётная запись заблокирована"), 403
    user.failed_attempts = 0
    db.session.commit()
    login_user(user)
    return jsonify(user_id=user.user_id, login=user.login, role=user.role), 200


@auth_bp.post("/register")
def register():
    data = _payload()
    if not data or not isinstance(data.get("login"), str) or not isinstance(data.get("password"), str):
        return jsonify(error="Укажите login и password"), 400
    login_value = data["login"].strip()
    password = data["password"]
    if len(login_value) < 3 or len(login_value) > 50 or len(password) < 12:
        return jsonify(error="Логин: 3–50 символов; пароль: не менее 12 символов"), 400
    if data.get("role") not in (None, "Пользователь"):
        return jsonify(error="Самостоятельно можно зарегистрироваться только с ролью Пользователь"), 403
    if db.session.execute(select(Users).where(Users.login == login_value)).scalar_one_or_none():
        return jsonify(error="Пользователь уже существует"), 409
    user = Users(login=login_value, password_hash=hash_password(password), role="Пользователь")
    db.session.add(user)
    db.session.commit()
    return jsonify(user_id=user.user_id, login=user.login, role=user.role), 201


@auth_bp.get("/me")
@login_required
def me():
    return jsonify(user_id=current_user.user_id, login=current_user.login, role=current_user.role)


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(message="Вы вышли из системы")
