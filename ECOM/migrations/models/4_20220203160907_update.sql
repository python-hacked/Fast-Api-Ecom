-- upgrade --
ALTER TABLE "vendor_products" ADD "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP;
-- downgrade --
ALTER TABLE "vendor_products" DROP COLUMN "created_at";
