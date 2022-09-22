from configs.connection import DATABASE_URL

db_url = DATABASE_URL()
TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": ["user.models", "vendor.models","aerich.models"],
            "default_connection": "default",
        },
    },
}