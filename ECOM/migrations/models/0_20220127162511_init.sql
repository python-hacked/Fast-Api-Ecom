-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL UNIQUE,
    "slug" VARCHAR(30) NOT NULL,
    "category_image" TEXT NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "state" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "STATE_CHOICES" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "status" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "STATUS_CHOICES" VARCHAR(50) NOT NULL  DEFAULT 'Accepted'
);
CREATE TABLE IF NOT EXISTS "subcategory" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL UNIQUE,
    "slug" VARCHAR(30) NOT NULL,
    "subcategory_image" TEXT NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category_id" CHAR(36) NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(250) NOT NULL
);
CREATE TABLE IF NOT EXISTS "profile" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "address" VARCHAR(200) NOT NULL,
    "address2" VARCHAR(200) NOT NULL,
    "city" VARCHAR(50) NOT NULL,
    "zipcode" INT NOT NULL,
    "state" VARCHAR(50) NOT NULL,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "selling_price" REAL NOT NULL,
    "slug" VARCHAR(30) NOT NULL,
    "discounted_price" REAL NOT NULL,
    "description" TEXT NOT NULL,
    "brand" VARCHAR(100) NOT NULL,
    "product_image" TEXT NOT NULL,
    "subcategory_id" CHAR(36) NOT NULL REFERENCES "subcategory" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "addtocart" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "quantity" INT NOT NULL  DEFAULT 1,
    "customer_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "product_id_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "order_placed" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "bill_amount" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(50) NOT NULL  DEFAULT 'Accepted',
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "order_products" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "product_price" INT NOT NULL,
    "quantity" INT NOT NULL  DEFAULT 1,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "order_placed_id" CHAR(36) NOT NULL REFERENCES "order_placed" ("id") ON DELETE CASCADE,
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
