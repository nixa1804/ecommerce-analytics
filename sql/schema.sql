CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    category_id INT REFERENCES categories(id),
    price       NUMERIC(10, 2) NOT NULL
);

CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    country    VARCHAR(100),
    city       VARCHAR(100)
);

CREATE TABLE orders (
    id           SERIAL PRIMARY KEY,
    user_id      INT REFERENCES users(id),
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    status       VARCHAR(20) NOT NULL CHECK (status IN ('completed', 'cancelled', 'pending')),
    total_amount NUMERIC(10, 2) NOT NULL
);

CREATE TABLE order_items (
    id         SERIAL PRIMARY KEY,
    order_id   INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity   INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE sessions (
    id         SERIAL PRIMARY KEY,
    user_id    INT REFERENCES users(id),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    source     VARCHAR(50) CHECK (source IN ('organic', 'paid', 'email', 'direct')),
    converted  BOOLEAN NOT NULL DEFAULT FALSE
);
