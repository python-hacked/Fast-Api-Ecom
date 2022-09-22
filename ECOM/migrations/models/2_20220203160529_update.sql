-- upgrade --
CREATE TABLE IF NOT EXISTS "vendor" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(80) NOT NULL,
    "Mobile" VARCHAR(10) NOT NULL UNIQUE,
    "alternet_mobile_number" VARCHAR(10) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "business_name" VARCHAR(200) NOT NULL UNIQUE,
    "shop_image" TEXT NOT NULL,
    "password" VARCHAR(250) NOT NULL,
    "shop_documents" TEXT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_active" INT NOT NULL  DEFAULT 1
);;
CREATE TABLE IF NOT EXISTS "vendor_products" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    -- "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "vendor_id" CHAR(36) NOT NULL REFERENCES "vendor" ("id") ON DELETE CASCADE
);-- downgrade --
DROP TABLE IF EXISTS "vendor";
DROP TABLE IF EXISTS "vendor_products";
