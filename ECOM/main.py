from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from user import route as UsersRoute
from vendor import route as VendorRoute
from user import api as apiRoute
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.hash import bcrypt
from tortoise.models import Model
from tortoise import fields
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from configs.connection import DATABASE_URL


db_url = DATABASE_URL()

middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]

app = FastAPI(middleware=middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(UsersRoute.router)
app.include_router(VendorRoute.router)
app.include_router(apiRoute.router, prefix="/api")

JWT_SECRET = 'myjwtsecret'

register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['user.models','vendor.models','aerich.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
