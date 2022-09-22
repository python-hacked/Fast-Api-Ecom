-- upgrade --
ALTER TABLE "order_placed" DROP COLUMN "product_id";
-- downgrade --
ALTER TABLE "order_placed" ADD "product_id" CHAR(36) NOT NULL;
ALTER TABLE "order_placed" ADD CONSTRAINT "fk_order_pl_product_dbbb04ab" FOREIGN KEY ("product_id") REFERENCES "product" ("id") ON DELETE CASCADE;
