"""Server-rendered pages and session login."""
from pathlib import Path
from flask import Blueprint, abort, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from app.auth import verify_password
from app.extensions import db
from app.models import Users, Notes

web_bp = Blueprint("web", __name__)
BASE_DIR = Path(__file__).resolve().parents[2]
IMAGE_FOLDER = BASE_DIR / "image"


@web_bp.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        login_value = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        user = db.session.execute(select(Users).where(Users.login == login_value)).scalar_one_or_none()
        if user is None or not verify_password(password, user.password_hash):
            if user is not None:
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.is_blocked = True
                db.session.commit()
            flash("Неверный логин или пароль", "error")
            return render_template("login.html"), 401
        if user.is_blocked:
            flash("Учётная запись заблокирована", "error")
            return render_template("login.html"), 403
        user.failed_attempts = 0
        db.session.commit()
        login_user(user)
        return redirect(url_for("web.admin_users" if user.role == "Администратор" else "web.dashboard"))
    return render_template("login.html")


def _page(template, title, current_page):
    return render_template(template, user=current_user, page_title=title, current_page=current_page)


@web_bp.get("/dashboard")
@login_required
def dashboard():
    return _page("base-dashboard.html", "Главная", "dashboard")


@web_bp.get("/clients")
@login_required
def clients():
    return _page("customer.html", "Клиенты", "clients")


@web_bp.get("/products")
@login_required
def products():
    return _page("items.html", "Номенклатура", "products")


@web_bp.get("/materials")
@login_required
def materials():
    return _page("items.html", "Материалы", "materials")


@web_bp.get("/operations")
@login_required
def operations():
    return _page("items.html", "Операции", "operations")


@web_bp.get("/specifications")
@login_required
def specifications():
    return _page("specification.html", "Спецификации", "specifications")


@web_bp.get("/sales-orders")
@login_required
def sales_orders():
    return _page("sales-orders.html", "Заказы покупателей", "sales-orders")


@web_bp.get("/production-orders")
@login_required
def production_orders():
    return _page("production-orders.html", "Заказы на производство", "production-orders")


@web_bp.get("/admin/users")
@login_required
def admin_users():
    if current_user.role != "Администратор":
        abort(403)
    return _page("admin-dashbord.html", "Пользователи", "admin-users")


@web_bp.get("/notes")
@login_required
def notes():
    return _page("notes.html", "Заметки", "notes")


@web_bp.get("/image/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


@web_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("web.login_page"))


@web_bp.post("/api/notes/")
@login_required
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not isinstance(data.get("content"), str):
        return {"error": "Укажите title и content"}, 400
    note = Notes(title=data["title"].strip(), content=data["content"], id_user=current_user.user_id)
    if not note.title:
        return {"error": "Заголовок не может быть пустым"}, 400
    db.session.add(note)
    db.session.commit()
    return {"id": note.note_id, "title": note.title, "content": note.content}, 201
