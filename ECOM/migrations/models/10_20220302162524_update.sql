-- upgrade --
ALTER TABLE "user" ADD "name" VARCHAR(80);
ALTER TABLE "user" ADD "phone" VARCHAR(10) ;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "name";
ALTER TABLE "user" DROP COLUMN "phone";
