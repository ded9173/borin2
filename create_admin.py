"""Create or reset the default Borin administrator account.

Run from the project root after configuring the database:
    python create_admin.py

Default credentials requested for the development/demo environment:
    login: admin
    password: admin1234

WARNING: This is a deliberately simple bootstrap credential. Change it before
exposing the application to a network or using it outside a local demo.
"""

import sys

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.auth import hash_password
from app.extensions import db
from app.models import Users

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin1234"
ADMIN_ROLE = "Администратор"


def main() -> int:
    app = create_app()
    with app.app_context():
        try:
            user = db.session.execute(
                select(Users).where(Users.login == ADMIN_LOGIN)
            ).scalar_one_or_none()

            if user is None:
                user = Users(
                    login=ADMIN_LOGIN,
                    password_hash=hash_password(ADMIN_PASSWORD),
                    role=ADMIN_ROLE,
                    is_blocked=False,
                    failed_attempts=0,
                    blocked_until=None,
                )
                db.session.add(user)
                action = "Создан"
            else:
                user.password_hash = hash_password(ADMIN_PASSWORD)
                user.role = ADMIN_ROLE
                user.is_blocked = False
                user.failed_attempts = 0
                user.blocked_until = None
                action = "Обновлён"

            db.session.commit()
            print(f"{action} администратор: {ADMIN_LOGIN}")
            print(f"Пароль: {ADMIN_PASSWORD}")
            print("ВНИМАНИЕ: смените пароль перед публикацией приложения в сети.")
            return 0
        except SQLAlchemyError as error:
            db.session.rollback()
            print(
                "Не удалось создать администратора. Проверьте DATABASE_URL, "
                "доступность БД и применённость схемы database/db.sql/миграций.",
                file=sys.stderr,
            )
            print(f"Подробности: {error}", file=sys.stderr)
            return 1
        finally:
            db.session.remove()


if __name__ == "__main__":
    raise SystemExit(main())
