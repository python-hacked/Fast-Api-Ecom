from email.mime import message
from http.client import HTTPException, HTTPResponse
# from msilib.schema import Class
from fastapi import APIRouter, Request,Form,status,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi import FastAPI, File, UploadFile
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from slugify import slugify
from datetime import datetime
import secrets
from user.models import product
import vendor
from vendor.pydantic_models import Token
from .models import *

SECRET = 'your-secret-key'
router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")   


@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

async def save_images(image,image_path):
                    FILEPATH = image_path
                    filename = image.filename
                    extension = filename.split(".")[1] 
                    imagename = filename.split(".")[0] 

                    if extension not in ["png", "jpg", "jpeg"]:
                        return{"status": "error","detial": "File extension not allowed"}

                    dt = datetime.now()
                    dt_timestamp = round(datetime.timestamp(dt))

                    modified_image_name = imagename+"_"+str(dt_timestamp)+"."+extension
                    genrated_name = FILEPATH + modified_image_name
                    file_content = await image.read()

                    with open (genrated_name, "wb") as file:
                        file.write(file_content)

                    file.close()
                    return genrated_name



@router.post('/vendor_registration/',)
async def create_vendor(email: str = Form(...), password: str = Form(...), 
                    name:str = Form(...), Mobile: int = Form(...), 
                    alternet_mobile_number: int = Form(...),
                    business_name:str = Form(...), 
                    shop_image:UploadFile = File(...),
                    shop_documents:UploadFile = File(...),
                        ):

               
                shop_image_url = await save_images(shop_image,'vendor/media/images/')
                shop_doc_url = await save_images(shop_documents,'vendor/media/documents/')

                vendor_obj = await Vendor.create( name = name,Mobile = Mobile,email= email,
                                                password= get_password_hash(password),alternet_mobile_number = alternet_mobile_number,
                                                business_name = business_name,shop_image =shop_image_url,
                                                shop_documents = shop_doc_url)

                return{"message":"registration successful"}


@router.get("/all_vendor",)
async def read_item(request: Request):
    vendor_obj = await Vendor.all()
    return vendor_obj

@manager.user_loader()
async def load_user(email: str):
    if await Vendor.exists(email=email):
        user = await Vendor.get(email = email)
        return user

         
    
@router.post('/vendor_login/', response_model=Token)
async def login(request:Request,data:  OAuth2PasswordRequestForm = Depends()):
                

    email = data.username
    user = await load_user(email)
    
    if not user:
        return {'USER NOT REGISTERED'}
       
    elif not verify_password(data.password,user.password):
        return {'PASSWORD IS WRONG'}
   
    access_token = manager.create_access_token(
        data={"sub":jsonable_encoder(user.email)}
    )
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token":access_token})
    return Token(access_token=access_token, token_type='bearer')       

@router.post("/vendor_product/")
async def create_vendor_product(
            product_id:str = Form(...),
            vendor_id:str = Form(...)):

        if await product.exists(id = product_id):
            
            if await Vendor.exists(id =vendor_id): 
                product_ins = await product.get(id=product_id)   
                vendor_ins = await Vendor.get(id=vendor_id)

                product_obj = await vendor_products.create(
                        product = product_ins,
                        vendor = vendor_ins)
            
                return {"product added."}                    