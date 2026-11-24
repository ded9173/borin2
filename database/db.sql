
-- =========================================
-- BORIN: PostgreSQL
-- База данных demo1
-- =========================================

-- 1. Контрагенты
CREATE TABLE IF NOT EXISTS counterparties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(20),
    address VARCHAR(255),
    phone VARCHAR(30),
    type VARCHAR(30)
);

-- 2. Номенклатура
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    item_type VARCHAR(50) NOT NULL
);

-- 3. Цены
CREATE TABLE IF NOT EXISTS price (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items(id),
    price NUMERIC(12,2) NOT NULL,
    effective_from DATE,
    effective_to DATE
);

-- 4. Себестоимость
CREATE TABLE IF NOT EXISTS cost_price (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    item_id INTEGER REFERENCES items(id),
    price_id INTEGER REFERENCES price(id),
    cost_price NUMERIC(12,2) NOT NULL
);

-- 5. Заказы покупателей
CREATE TABLE IF NOT EXISTS customer_order (
    id SERIAL PRIMARY KEY,
    items_id INTEGER REFERENCES items(id),
    counterparties_id INTEGER REFERENCES counterparties(id),
    quantity NUMERIC(12,2) NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL
);

-- 6. Производственные заказы
CREATE TABLE IF NOT EXISTS manufactur_order (
    id SERIAL PRIMARY KEY,
    items_id INTEGER REFERENCES items(id),
    cost_price INTEGER REFERENCES cost_price(id)
);

-- 7. Заказы на производство
CREATE TABLE IF NOT EXISTS production_orders (
    id SERIAL PRIMARY KEY,
    items_id INTEGER REFERENCES items(id),
    cost_price INTEGER REFERENCES cost_price(id),
    quantity NUMERIC(12,2),
    unit_price NUMERIC(12,2)
);

-- 8. Пользователи
CREATE TABLE IF NOT EXISTS users (
    users_id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'Пользователь',
    is_blocked BOOLEAN DEFAULT FALSE,
    failed_attempts INTEGER DEFAULT 0,
    blocked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Заметки
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    id_user INTEGER REFERENCES users(users_id)
        ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- ИНДЕКСЫ
-- =========================================

CREATE INDEX IF NOT EXISTS idx_price_item
ON price(item_id);

CREATE INDEX IF NOT EXISTS idx_cost_item
ON cost_price(item_id);

CREATE INDEX IF NOT EXISTS idx_customer_items
ON customer_order(items_id);

CREATE INDEX IF NOT EXISTS idx_customer_counterparties
ON customer_order(counterparties_id);

CREATE INDEX IF NOT EXISTS idx_notes_user
ON notes(id_user);

-- =========================================
-- КОНЕЦ СКРИПТА
-- =========================================
