-- upgrade --
ALTER TABLE "user" ADD "phone" VARCHAR(10) NOT NULL;

-- downgrade --
ALTER TABLE "user" DROP COLUMN "phone";
