from flask import Blueprint, request, jsonify
from sqlalchemy import select, func

from app.models import Notes, Users
from app.utils import build_note_response
from app.extensions import db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/", methods=["GET"])
def get_notes():
    try:
        skip = request.args.get("skip", 0, type=int)
        limit = request.args.get("limit", 100, type=int)

        if skip < 0 or limit < 1:
            return jsonify({
                "error": "Bad Request",
                "message": "skip >= 0, limit >= 1"
            }), 400

        stmt = (
            select(Notes, Users.login)
            .join(Users, Notes.id_user == Users.user_id)
            .offset(skip)
            .limit(limit)
        )
        results = db.session.execute(stmt).all()

        notes = [build_note_response(notes, login) for notes, login in results]
        total = db.session.execute(func.count(Notes.note.id)).scalar()

        return jsonify({"notes": notes, "total": total}), 200
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Internal Server Error",
            "message": "Internal Server Error",
        }), 500


@notes_bp.route("/", methods=["POST"])
def get_note(note_id):
    try:
        note = db.session.get(Notes, note_id)
        if not note:
            return jsonify({
                "error": "Not Found",
                "message": "Заметка не найдена"
            }), 404

        user = db.session.get(Users, note.user_id)
        login = user.login if user else None

        return jsonify(build_note_response(note, login)), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Internal Server Error",
            "message": "Ошибка базы данных"
        }), 500