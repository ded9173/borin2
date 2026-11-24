# Отчёт по логике приложения, API, БД и тестам

## Общий результат
Проверены обработчики в `app/blueprints/` и `app/views/`, сервисы, репозитории, `app/models.py` и `database/db.sql`. Найдены блокирующие ошибки, из-за которых часть endpoint не сможет корректно зарегистрироваться или выполнить запрос. Запуск интеграционных тестов невозможен: `tests/`, `requirements.txt` (пустой) и конфигурация тестовой БД отсутствуют.

## Ключевые дефекты логики
- `app/__init__.py`: инициализация расширений и регистрация Blueprint выполняются только при наличии `SQLALCHEMY_DATABASE_URI`; фабрика может вернуть `None`, если URI не задан. `config_name` принимается, но выбор конфигурации фактически делается через `ENV` внутри `get_config()`, а не по аргументу.
- `app/config.py`: URL БД формируется функцией `_bild_database_url()`, но классы конфигурации не присваивают результат `SQLALCHEMY_DATABASE_URI` (кроме тестового класса). `get_config()` читает `ENV`, тогда как фабрика предварительно читает `FLASK_ENV`.
- `app/views/base_views.py`: базовый класс предоставляет `_success`, `error_response`, `_not_found_response`, тогда как дочерние классы вызывают `_success_response` и `_error_response`; этих методов в базовом классе нет.
- `app/views/customer_view.py`: используется несуществующий/неопределённый `CustomerServise`; проверки и возвраты обращаются к переменной `Customer` вместо результата `co`; в DELETE используется `Customer_id`, который не определён; в URL регистрируется `Customer.as_view`, хотя `Customer` импортирован из `app.blueprints`.
- `app/views/items_views.py`: используются несуществующие идентификаторы `itemsListAPI`; регистрация detail endpoint привязана к list-классу; аргументы маршрутов/методов не согласованы.
- `app/views/admin_view.py`: импорты из `run.*` не соответствуют пакетной структуре; методы репозитория/сервиса не согласованы.
- `app/views/notes_view.py`: GET списка формирует `notes`, но возвращает `{"notes": Notes, ...}` (класс модели), а не список `notes`.
- `app/blueprints/auth.py`: вложенная функция `login` затеняет внешний обработчик и не вызывается; `/me` объявляется внутри тела обработчика и фактически не регистрируется при импорте модуля; используется `Users` (класс) в проверках вместо `user`; обращение `user.user.id` не соответствует модели; регистрация передаёт `passwrod_hash`, тогда как модель содержит `password`.
- `app/blueprints/web.py`: в проверке пароля условие `if not Users or ...` проверяет класс, а не результат поиска; шаблоны `dashboard.html`, `clients.html`, `products.html`, `materials.html`, `operations.html` не совпадают с имеющимися именами файлов в `web/` (например `base-dashboard.html`, `customer.html`, `items.html`).
- `app/services/customer_servise.py`: `get_all_dto()` вызывает методы базового сервиса, но класс не наследуется от `BaseService`; `create_countreparties()` ссылается на несуществующие переменные `name`, `inn`, `address`, `phone`, `type`.
- `app/services/user_servise.py`: передаёт в `BaseService` класс репозитория без создания экземпляра; импортирует тестовый класс SQLAlchemy `User`; `get_all_dto()` итерируется по `User`, а не по записям; метод создания назван `vcreate_user`.
- `app/repository/base_repository.py`: `db.select([self.model])` использует устаревший/несовместимый стиль SQLAlchemy 2; commit выполняется внутри цикла обновления атрибутов; нет проверки диапазонов пагинации и централизованного rollback.
- `app/blueprints/notes.py` и `app/views/notes_view.py`: существуют параллельные обработчики заметок с разным поведением; в `web.py` есть ещё один endpoint создания заметки.

## База данных
`database/db.sql` создаёт таблицы `counterparties`, `items`, `price`, `cost_price`, `customer_order`, `manufactur_order`, `production_orders`, `users`, `notes`. ORM-модели содержат иные таблицы/поля, включая `countrerparties`, `products`, `production_order_items`, `Specification`, `Production_Order`; имена PK/FK и типы UUID/INTEGER не согласованы. Примеры:
- SQL `counterparties.id`, ORM `Customer.__tablename__ = "countrerparties"` (опечатка и иное имя).
- SQL `users.users_id`, ORM `Users.user_id`; SQL `password_hash`, ORM `password`.
- SQL `customer_order.items_id`/`counterparties_id`, ORM `CustomerOrder` содержит иные/неполные поля.
- SQL `production_orders` с integer `id`, ORM `ProductionOrderItem` ссылается на `production_orders.order_id` и `products.product_id`, которых в DDL нет.
- В `models.py` используются `column(...)` вместо `Column(...)`, `Column()` без типа, `Column(int)` вместо SQLAlchemy `Integer`, а `Column(uuid=...)` задаёт неизвестный именованный аргумент.
- Связи `relationship()` ссылаются на имена классов/атрибутов с разным регистром и на отсутствующие модели (`Product`, `ProductionOrder`, `CustomerOrderItem`, `SalesOrder`).

ER-диаграмма `er_diagram.pdf` в архиве отсутствует, поэтому сверка с ней не выполнена.

## SQL-инъекции и транзакции
В изученных репозиториях и обработчиках встречаются SQLAlchemy expression API и ORM-запросы; явный конкатенированный SQL в просмотренных ключевых фрагментах не является основным способом доступа. Это снижает риск классической SQL-инъекции, но не заменяет аудит всех файлов и динамических фильтров. Ошибки транзакций: часть обработчиков делает commit без обработки исключения; часть перехватывает общий Exception и скрывает детали; в базовом репозитории commit расположен внутри цикла.

## Таблица замечаний по маршрутам и БД
См. `route_db_findings.md`.

## Рекомендации
Сначала согласовать единую схему данных и имена моделей, затем привести в соответствие миграции/DDL/ORM, после этого починить маршруты и сервисы. Только затем имеет смысл строить тесты CRUD, авторизации, разграничения доступа и негативных сценариев.
