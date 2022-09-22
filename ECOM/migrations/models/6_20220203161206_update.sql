-- upgrade --
CREATE TABLE IF NOT EXISTS "vendor_products" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "vendor_id" CHAR(36) NOT NULL REFERENCES "vendor" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "vendor_products";
