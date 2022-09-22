from http.client import HTTPException, HTTPResponse
from fastapi import APIRouter, Request,Form,status,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from tortoise.functions import Sum
from slugify import slugify
from datetime import datetime
from passlib.context import CryptContext
import secrets
from .models import *

SECRET = 'your-secret-key'
router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')
templates = Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    username = None
    if "_messages" in request.session:
        print(request.session["_messages"]) 
        username = request.session["_messages"][0]['username']
    cat = await Category_pydantic.from_queryset(Category.filter(is_active = True))
    products = await product.all()
    return templates.TemplateResponse("home.html", {"request": request,
    "categories": cat,
    "username": username,
    "products":products})

@router.get("/all_product",)
async def read_item(request: Request):
    productObject = await product.all()
    return productObject

@router.get("/registration/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("registration.html", {
        "request": request,
        })

@router.post('/add_registration/',)
async def create_user(request: Request,email: str = Form(...),
                      name: str = Form(...), \
                      phone: str = Form(...),
                      password: str = Form(...)):
    if "_messages" in request.session:
        print(request.session["_messages"][0]['username']) 
        phone = request.session["_messages"][0]['username']
        
    elif "_messages" in request.session:
        print(request.session["_messages"][0]['username']) 
        email = request.session["_messages"][0]['username']
        
    else:
        user_obj = await User.create(email=email,name=name,
                                     phone=phone
                                     ,password= get_password_hash(password))
       
    return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)

@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
manager = LoginManager(SECRET, token_url='/auth/token')

@manager.user_loader()
async def load_user(email: str):
    if await User.exists(email=email):
        user = await User.get(email = email)
        return user

@router.post('/login/')
async def login(request:Request,username: str = Form(...)
                , password: str = Form(...)):
#   try:
     
    # sess = request.session
    email = username
   
    user = await load_user(email)
    
    if not user:
        # print('u r hereeeee')
        return {'USER NOT REGISTERED'}
    elif not verify_password(password,user.password):
        return {'PASSWORD IS WRONG'}
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    print(user.id)
    # request.session.clear()
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id":str(user.id),"username": username, "access_token": str(access_token)}
        # print(new_dict)
        request.session['_messages'].append(
            new_dict
        ) 
    # else:
    #     request.session['_messages'].append(
    #         new_dict
    #     ) 
  
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@router.get("/profile/", response_class=HTMLResponse)
async def read_item(request: Request):

    email = None
    if "_messages" in request.session:
        print(request.session["_messages"][0]['username']) 
        email = request.session["_messages"][0]['username']
        username = request.session["_messages"][0]['username']
        

    if await Profile.exists(user__email= email):
        user_obj= await Profile.get(user__email=email)
    else:
        user_obj = None
    state = await State.all()
   
    for i in STATE_CHOICES:
        print(i[1])
    return templates.TemplateResponse("profile.html", 
                        {
                        "request": request, 
                        "user_obj": user_obj,
                        "username":username,
                        "STATE_CHOICES":STATE_CHOICES
                        })
    
# customer profile update    
@router.post("/update_profile/")
async def update_profile(request: Request, name: str = Form(...),
            address: str = Form(...),address2: str = Form(...),
            city:str = Form(...),zipcode:str = Form(...),
            state:str = Form(...)):
    email = request.session["_messages"][0]['email']
    user = await User.get(email= email)
    if await Profile.exists(user__email= email):

        user_obj = await Profile.filter(user=user).update(name=name,address=address,
                        address2=address2,city=city, zipcode=zipcode, 
                        state=state)
    else:
       
        user_obj = await Profile.create(user=user,name=name,
                        address=address,address2=address2,
                        city=city, zipcode=zipcode, state=state)

    return RedirectResponse("/profile/", status_code=status.HTTP_302_FOUND)

@router.get("/orders/", response_class=HTMLResponse)
async def read_item(request: Request):
        orders_obj = None

        if "_messages" in request.session:
         print(request.session["_messages"][0]) 
        user_id = request.session["_messages"][0]['user_id']  
        username = request.session["_messages"][0]['username']
        
        if await order_placed.exists(user__id = user_id):
             orders_obj = await order_place_pydantic.from_queryset(
        order_placed.filter(user__id=user_id))

        else:
            orders_obj = None
        return templates.TemplateResponse("orders.html",context = {"request": request,
                                            "orders_obj":orders_obj,
                                            "username":username}) 
        
@router.post("/order_placed/",)
async def place_order(request: Request):

    if "_messages" in request.session:
        print(request.session["_messages"][0])   
        customer_id = request.session["_messages"][0]['user_id']  
                         
        cartObject = await addtocart.filter(customer=customer_id).values("product_id__discounted_price","quantity","product_id__id",)
       
        print(cartObject)
        bill_amount = 0
        for cart_item in cartObject:
            # print(product)
            
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
            return RedirectResponse("/orders/", status_code=status.HTTP_302_FOUND)
    else:
        return {'something went wrong'}    
       
@router.get("/changepassword/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("changepassword.html", {"request": request})

@router.get("/addtocart/", response_class=HTMLResponse)
async def read_item(request: Request):

 if "_messages" in request.session: 
        customer_id = request.session["_messages"][0]['user_id']  
        username = request.session["_messages"][0]['username']
                             

        cartObject = await addtocart_Pydantic.from_queryset(
            addtocart.filter(customer=customer_id))

        cartObject2 = await addtocart.filter(customer=customer_id).values("product_id__discounted_price","quantity","product_id__id",)
       
        bill_amount = 0
        for cart_item in cartObject2:
            print(product)
            bill_amount = bill_amount + ((cart_item["product_id__discounted_price"])*(cart_item["quantity"]))
      
        return templates.TemplateResponse("addtocart.html", {"request": request, 
                                                             "cartproducts": cartObject,
                                                             "bill_amount":bill_amount,
                                                             "username":username })

@router.get("/adtocart",)
async def read_item(request: Request):

 if "_messages" in request.session:
        
        customer_id = request.session["_messages"][0]['user_id']                       

        cartObject = await addtocart_Pydantic.from_queryset(
            addtocart.filter(customer=customer_id))              
        return cartObject
    
# create addtocart
@router.get("/addtocart/{product_id}/")
async def create_cart(request: Request, product_id:str 
                       ):

 if "_messages" in request.session:
        
        customer_id = request.session["_messages"][0]['user_id']                       

 product_obj = await product.get(id = product_id)
 customer_obj = await User.get(id = customer_id)
 
#  quentity update 
 if await addtocart.exists(customer = customer_obj, product_id = product_obj):
    cart_obj = await addtocart.get(customer = customer_obj, product_id = product_obj)
    cart_qty = cart_obj.quantity
    new_qty = cart_qty + 1
    cart_obj.quantity = new_qty
    await cart_obj.save()
    # cart_obj.save()
 else:   
    addtocart_obj = await addtocart.create(
                    product_id=product_obj,
                    customer = customer_obj
                    )
 return RedirectResponse("/addtocart/", status_code=status.HTTP_302_FOUND)

# update cart quantity (+)(-)
@router.post("/updatecart/{flag}")
async def update_item(request: Request,flag:str):
    data = await request.json()
    print(data)
    product_id = data["id"]
    if "_messages" in request.session:
        customer_id = request.session["_messages"][0]['user_id'] 
        product_obj = await product.get(id = product_id)
        customer_obj = await User.get(id = customer_id)
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
        cartObject2 = await addtocart_Pydantic.from_queryset(addtocart.filter(customer__id=customer_id,) )
        
        bill_amount = 0
        new_dict = {}
        new_array = []
        for cart_item in cartObject2:
            new_dict = cart_item
            new_dict.update({"quantity":cart_item.quantity})
            new_array.append(new_dict)
            bill_amount = bill_amount + ((cart_item.product_id.discounted_price)*(cart_item.quantity))
            print(bill_amount)
        # return JSONResponse({"item_qty":item_qty, "bill_amount": bill_amount})
        return {}
        
@router.get("/buynow/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("buynow.html", {"request": request})


@router.get("/productpage/{product_slug}/", )
async def product_view(request: Request, product_slug:str):
    productpage = await product_pydantic.from_queryset(
        product.filter(slug=product_slug)
        )
    return templates.TemplateResponse("productpage.html", context={"request": request, })
   
@router.get('/logout/')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/')            

@router.get("/products/{sub_cat_slug}/", )
async def read_item(request: Request, sub_cat_slug:str):
    url = "http://127.0.0.1:8000"
    subcategory = await SubCategory.get(slug=sub_cat_slug)
    products = await product_pydantic.from_queryset(
        product.filter(subcategory=subcategory)
        )
    return templates.TemplateResponse("products.html", 
    {"request": request,
    "products": products,
    "url": url
    })

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

          return {"message": "subcategory add"}

@router.post('/checkout/',)
async def create_user(email: str = Form(...), password: str = Form(...)):
    user_obj = await User.create(email= email,password= password)
    return RedirectResponse("/checkout/", status_code=status.HTTP_302_FOUND)             
                          
