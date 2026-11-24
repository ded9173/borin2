# Borin

## Требования

Python 3.10+ и PostgreSQL (для production). Для локальной разработки приложение по умолчанию использует SQLite.

## Установка и запуск

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Задайте в `.env` случайный `SECRET_KEY` длиной не менее 32 символов. Для PostgreSQL задайте `DATABASE_URL`, например:

```text
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/borin
```

Запуск локально:

```bash
python run.py
```

Проверка состояния приложения и БД: `GET /health`. По умолчанию сервер слушает `127.0.0.1:5000`, debug выключен. Не используйте встроенный сервер Flask в production.

## Проверка синтаксиса

```bash
python -m compileall -q app run.py
```

## Ревью

Итоговые документы находятся в `docs/review/`, включая `review_report.md`, `findings_summary.md` и PR draft.
