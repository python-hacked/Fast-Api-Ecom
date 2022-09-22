import fnmatch
from http.client import ACCEPTED, HTTPException, HTTPResponse
from typing import List
from fastapi import APIRouter, Request,Form,status,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from passlib.context import CryptContext
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from slugify import slugify
from datetime import datetime,timedelta
import secrets
import user
from user.pydantic_models import Itemcart, cartItems

from vendor.models import Vendor, vendor_products
from .models import *

SECRET = 'your-secret-key'
router = APIRouter()
manager = LoginManager(SECRET, token_url='/api/login/')
templates = Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class loginModel(BaseModel):
    email: str
    name: str
    phone: str
    password: str

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    email = None
    if "_messages" in request.session:
        print(request.session["_messages"][0]['email']) 
        email = request.session["_messages"][0]['email']
    cat = await Category_pydantic.from_queryset(Category.filter(is_active = True))
    
    return templates.TemplateResponse("home.html", {"request": request,
    "categories": cat,
    "username": email})

@router.post('/add_registration/',)
async def create_user(request: Request, data:loginModel):
    if await User.exists(phone=data.phone):
        return {"message": "This number already register"}
    elif await User.exists(email=data.email):
        return {"message": "This email id is already registered"}
    else:
        add_user = await User.create(email= data.email,name=data.name,phone=data.phone ,password= get_password_hash(data.password))
        return JSONResponse({
                        "registration": jsonable_encoder(add_user),
                        })
    
@router.delete("/all_user",)
async def read_item(request: Request):
    userObject = await User.all().delete()
    return {"message": "user deleted"}    

@router.get("/all_user",)
async def read_item(request: Request):
    userObject = await User.all()
    return userObject

@manager.user_loader()
async def load_user(email: str):
    if await User.exists(email=email):
        user = await User.get(email = email)
        return user
    
import uuid
class messageDict(BaseModel):
    email: str
    access_token: str

class loginOutput(BaseModel):
    status: bool
    message: messageDict
    
    class config: 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
@router.post('/login/', )
async def login(request:Request,data:  OAuth2PasswordRequestForm = Depends()):
#   try:
     
    # sess = request.session
    email = data.username
    user = await load_user(email)
    
    if not user:
        return JSONResponse({'status':False,'message':'User not Registered'},status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'Invalid password'},status_code=403)
    print(user.id)
    access_token = manager.create_access_token(
        data={'sub':jsonable_encoder(user.email),"name":jsonable_encoder(user.name),"phone":jsonable_encoder(user.phone)},expires=timedelta(minutes=120)
    )
    
    '''test  current user'''
    
    
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token":access_token})
    return Token(access_token=access_token, token_type='bearer')

@router.get("/profile/", response_class=HTMLResponse)
async def read_item(request: Request):

    email = None
    if "_messages" in request.session:
        print(request.session["_messages"][0]['username']) 
        email = request.session["_messages"][0]['username']

    if await Profile.exists(user__email= email):
        user_obj= await Profile.get(user__email=email)
    else:
        user_obj = None
    state = await State.all()
   
    for i in STATE_CHOICES:
        print(i[1])
    return JSONResponse({
                   "status": True, "message": jsonable_encoder(update_profile)
                    })
 
@router.post("/update_profile/")
async def update_profile(request: Request, name: str = Form(...),
            address: str = Form(...),address2: str = Form(...),
            city:str = Form(...),zipcode:str = Form(...),
            state:str = Form(...)):
    email = request.session["_messages"][0]['username']
    user = await User.get(email= email)
    if await Profile.exists(user__email= email):

        user_obj = await Profile.filter(user=user).update(name=name,address=address,
                        address2=address2,city=city, zipcode=zipcode, 
                        state=state)
    else:
        user_obj = await Profile.create(user=user,name=name,
                        address=address,address2=address2,
                        city=city, zipcode=zipcode, state=state)
    return {"massage": "update profile"}

# ALL CATEGORY
@router.get("/Category/", )
async def read_item(request: Request):
    cat = await Category_pydantic.from_queryset(Category.filter(is_active = True))
    return cat
                                
@router.post("/Category/")
async def create_category(category_image: UploadFile = File(...),
            name: str = Form(...),
            ):
    if await Category.exists(name=name):
        return {"message": "category already exists"}
    else:

          slug = slugify(name)

          FILEPATH = "static/images/product/"
          filename = category_image.filename
          extension = filename.split(".")[1] 
          imagename = filename.split(".")[0] 

          if extension not in ["png", "jpg", "jpeg"]:
              return{"status": "error","detial": "File extension not allowed"}

          dt = datetime.now()
          dt_timestamp = round(datetime.timestamp(dt))

          modified_image_name = imagename+"_"+str(dt_timestamp)+"."+extension
          genrated_name = FILEPATH + modified_image_name
          file_content = await category_image.read()
        
          with open (genrated_name, "wb") as file:
              file.write(file_content)

          file.close()

          category_obj = await Category.create(
                 category_image=genrated_name,
                 name=name,
                 slug=slug)
                
          return {"category added"}

# ALL SUBCATEGORY
@router.get("/SubCategory/", )
async def read_item(request: Request):
    subcat = await SubCategory.filter(is_active = True)
    return subcat                 

@router.post("/SubCategory/")
async def create_subcategory(subcategory_image: UploadFile = File(...),
            name: str = Form(...),category_id: str = Form(...)
            ):
          category = await Category.get(id=category_id)
          slug = slugify(name)

          FILEPATH = "static/images/product/"
          filename = subcategory_image.filename
          extension = filename.split(".")[1] 
          imagename = filename.split(".")[0] 

          if extension not in ["png", "jpg", "jpeg"]:
                return{"status": "error","detial": "File extension not allowed"}

          dt = datetime.now()
          dt_timestamp = round(datetime.timestamp(dt))

          modified_image_name = imagename+"_"+str(dt_timestamp)+"."+extension
          genrated_name = FILEPATH + modified_image_name
          file_content = await subcategory_image.read()
        
          with open (genrated_name, "wb") as file:
              file.write(file_content)

          file.close()
 
          subcategory_obj = await SubCategory.create(
                 subcategory_image=genrated_name,
                 name=name,
                 slug=slug,
                 category=category)

          return {"message": " subcategory add"}
      
# ALL PRODUCT
@router.post("/product/")
async def create_product(image: UploadFile = File(...), title: str = Form(...),
            sellingPrice:float = Form(...),discountedPrice:int = Form(...),
            description:str = Form(...),
            brand:str = Form(...),
            sub_category_id:str = Form(...)):

          subcategory = await SubCategory.get(id=sub_category_id)
          FILEPATH = "static/images/product/"
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

          product_obj = await product.create(
                product_image=genrated_name,
                title=title,
                selling_price=sellingPrice,
                discounted_price=discountedPrice,
                description=description,
                brand=brand, 
                subcategory=subcategory,
                slug = slugify(title))
    
          return {"product added."}
      

@router.get("/productpage/{product_slug}/", )
async def product_view(request: Request, product_slug:str):
    productpage = await product_pydantic.from_queryset(
        product.filter(slug=product_slug)
        )
    return {"message": "view product"}


@router.get("/products/{sub_cat_slug}/", )
async def read_item(request: Request, sub_cat_slug:str):
    url = "http://192.168.1.101:8000"
    subcategory = await SubCategory.get(slug=sub_cat_slug)
    products = await product.filter(subcategory=subcategory)


# fatching vendore details with in product detials 
    new_product_list = []
    for each in products:
        product_dict = jsonable_encoder(each)
        product_id = each.id
        if await vendor_products.exists(product__id=product_id):
            vendors = await vendor_products.filter(product__id=product_id)
            
            vendor_list = []
            for each_vendor in vendors:
                vendor_id = each_vendor.vendor_id
                vendor_ins = await Vendor.get(id=vendor_id)
                vendor_dict = {
                    "id": vendor_id,
                    "vendor_name": vendor_ins.name,  
                    "business_name": vendor_ins.business_name,
                }
                vendor_list.append(vendor_dict)
            product_dict.update({"vendors": vendor_dict})
            new_product_list.append(product_dict)
        else:
            new_product_list.append(product_dict)

    return JSONResponse({
                    "products": jsonable_encoder(new_product_list),
                    })


@router.get("/changepassword/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("changepassword.html", {"request": request})


# @router.post("/changepassword/")
# async def forget_password(request:Request):
#     if '_messages' in request.session:
#         if 'username' in request.session['_messages'][0]:
    # User = await User.find_exist_user(request.email)
    # if not result:


@router.get("/address/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("address.html", {"request": request})

@router.post("/addtocart/",
             response_model=Itemcart
             )
async def create_cart( data:cartItems,
                        user=Depends(manager)):
 product_id = data.product_id
 quantity = data.quantity  
 flag = data.flag 
 customer_id = user.id 
 ''' new code goes here'''
 
 product_obj = await product.get(id = product_id)
 customer_obj = await User.get(id = customer_id)
 if await addtocart.exists(customer = customer_obj,product_id = product_obj,): 
    cart_obj = await addtocart.get(customer = customer_obj,product_id = product_obj,)
    add_qty  = cart_obj.quantity
    if flag == "add":      
                
                new_qty = add_qty +1 
                cart_obj.quantity = new_qty
                await cart_obj.save()
                
                
    elif flag == "minus":
                if add_qty >1:
                    new_qty = add_qty -1 
                    cart_obj.quantity = new_qty
                    await cart_obj.save()
                
                else:
                    await addtocart.get(customer = customer_obj,product_id = product_obj).all().delete()
                    item_qty = 0
    else:
                item_qty = 0
 else:
    addtocart_obj = await addtocart.create(
                        quantity=quantity,product_id=product_obj,
                        customer = customer_obj
                        )
 '''new code ends here'''   
 cart = await addtocart_Pydantic.from_queryset(addtocart.filter(customer__id=customer_id,) )
            
 bill_amount = 0
 
 new_array = []
 for cart_item in cart:
            product_sub_total = cart_item.product_id.discounted_price*cart_item.quantity
            bill_amount = bill_amount + product_sub_total
            new_dict = jsonable_encoder(cart_item.product_id)
            new_dict.update({"quantity":cart_item.quantity})
            new_dict.update({"product_sub_total":product_sub_total})
            new_array.append(new_dict)
            print(new_dict)
 resp = {
     "products": new_array,
     
     "bill_amount":bill_amount
 }
 return resp 


@router.get("/cart/", response_model=Itemcart)
async def read_item(request: Request, user=Depends(manager)): 
    
    customer_id = user.id 
    print(customer_id)
    cart = await addtocart_Pydantic.from_queryset(addtocart.filter(customer__id=customer_id,) )
    bill_amount = 0
    new_array = []
    for cart_item in cart:
                product_sub_total = cart_item.product_id.discounted_price*cart_item.quantity
                bill_amount = bill_amount + (product_sub_total)
                new_dict = jsonable_encoder(cart_item.product_id)
                new_dict.update({"quantity":cart_item.quantity})
                new_dict.update({"product_sub_total":product_sub_total})
                new_array.append(new_dict)
                print(new_dict)
    resp = {
        "products": new_array,
        
        "bill_amount":bill_amount
    }
    return resp 


@router.post("/order_placed/",)
async def place_order(user=Depends(manager)):
        customer_id = user.id
    
        cartObject = await addtocart.filter(customer=customer_id).values("product_id__discounted_price","quantity","product_id__id",)
        bill_amount = 0
        for cart_item in cartObject:
            
            bill_amount = bill_amount + ((cart_item["product_id__discounted_price"])*(cart_item["quantity"]))

        order_obj = await order_placed.create(
            user = await User.get(id = customer_id),
            bill_amount = bill_amount
        )
        for item in cartObject:
            order_items = await order_products.create(
                order_placed = order_obj,
                product = await product.get(id=item["product_id__id"]),
                product_price = item["product_id__discounted_price"],
                quantity = item["quantity"]
            )
            await addtocart.filter(customer=customer_id).delete()
            
            return JSONResponse({
                   "status": True, "message": "ORDER PLACED"
            })
        else:
            return JSONResponse({"status" : False, "message":"something went wrong"},status_code=403)

@router.post("/orders/",)
async def read_item(user=Depends(manager)):
        orders_obj = None
        customer_id = user.id
        if await order_placed.exists(user__id = customer_id):
             orders_obj = await order_place_pydantic.from_queryset(
        order_placed.filter(user__id=customer_id))
        else:
            orders_obj = None
        return JSONResponse({
                   "status": True, "message": "Accepted"
            })
        
@router.get("/all_orders",)
async def read_item(request: Request):
    orders = await order_placed,all()
    return orders       
             
# @router.put("/order/{user_id}", response_model=Item)
# async def update_order_status(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded   
             
@router.get('/logout/')
async def logout(request: Request):
    if '_messages' in request.session:
        if 'username' in request.session['_messages'][0]:
            request.session.clear()
    return {"message":"user logout"}          


