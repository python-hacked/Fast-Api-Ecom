from fastapi import FastAPI
from typing import Optional
from tortoise.models import Model
from datetime import datetime
from tortoise import Tortoise,fields
from .db import Base
from tortoise.contrib.pydantic import pydantic_model_creator
app = FastAPI()

STATE_CHOICES = (
('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
('Andra Pradesh', 'Andra Pradesh'),
('Arunachal Pradesh', 'Arunachal Pradesh'),
('Assam', 'Assam'),
('Bihar', 'Bihar'),
('Chhattisgarh', 'Chhattisgarh'),
('chandigarh', 'chandigarh'),
('dadra & Nagar Haveli', 'dadra & Nagar Haveli'),
('Delhi', 'Delhi'),
('Madhya Pradesh', 'Madhya Pradesh'),
('Utter Pradesh', 'Utter Pradesh'),
('Andra Pradesh', 'Andra Pradesh'),
('Mumbai', 'Mumbai'),
('Mizoram', 'Mizoram'),
('Nagaland', 'Nagaland')
)

# product category
class Category(Model):
    id = fields.UUIDField(pk = True)
    name = fields.CharField(200, unique=True)
    slug = fields.CharField(30)
    category_image = fields.TextField()
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

# product SubCategory
class SubCategory(Model):
    id = fields.UUIDField(pk = True)
    name = fields.CharField(200, unique=True)
    slug = fields.CharField(30)
    subcategory_image = fields.TextField()
    category = fields.ForeignKeyField("models.Category", related_name = "subcategory", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)    
   
CATEGORY_CHOICES =(
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)
class product(Model):
    id = fields.UUIDField(pk = True)    
    title = fields.CharField(max_length=100)
    selling_price = fields.FloatField()
    slug = fields.CharField(30)
    discounted_price = fields.FloatField()
    description = fields.TextField()
    brand = fields.CharField(max_length=100)
    subcategory = fields.ForeignKeyField("models.SubCategory", related_name ="products", on_delete="CASCADE")
    product_image = fields.TextField()

class State(Model):
    # state = fields.ForeignKeyField("models.User", related_name= "user_profile", on_delete="CASCADE")
    STATE_CHOICES = fields.CharField(choices=STATE_CHOICES, max_length=50)

class Profile(Model):
    id = fields.UUIDField(pk = True)
    user = fields.ForeignKeyField("models.User", related_name= "user_profile", on_delete="CASCADE")
    name = fields.CharField(max_length=200)
    address = fields.CharField(max_length=200)
    address2 = fields.CharField(max_length=200)
    city = fields.CharField(max_length=50)
    zipcode = fields.IntField()
    state = fields.CharField(choices=STATE_CHOICES, max_length=50)

class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(50, unique=True)
    name = fields.CharField(80)
    # phone = fields.CharField(10)
    password= fields.CharField(250,)

# class cart(Model):
#     # product = fields.ForeignKey("models.product")
#     quantity = fields.IntField(default=1)

class addtocart(Model):
    id =fields.UUIDField(pk=True)
    customer = fields.ForeignKeyField("models.User", related_name = "usercart", on_delete="CASCADE")
    product_id = fields.ForeignKeyField("models.product", related_name= "cart", on_delete="CASCADE")     
    quantity = fields.IntField(default=1)

STATUS_CHOICES =(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class order_placed(Model):
    id = fields.UUIDField(pk = True)
    user = fields.ForeignKeyField("models.User", on_delete="CASCADE")
    bill_amount = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    status = fields.CharField(max_length=50, choices=STATUS_CHOICES, default='Accepted') 

class order_products(Model):
    id = fields.UUIDField(pk = True)
    order_placed = fields.ForeignKeyField("models.order_placed", related_name= "order_placed", on_delete="CASCADE")
    product = fields.ForeignKeyField("models.product", on_delete="CASCADE")
    product_price = fields.IntField() 
    quantity = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)

class Status (Model):
    STATUS_CHOICES = fields.CharField(max_length=50, choices=STATUS_CHOICES, default='Accepted') 

Tortoise.init_models(['user.models'], 'models')

product_pydantic = pydantic_model_creator(product)
Category_pydantic = pydantic_model_creator(Category)
addtocart_Pydantic = pydantic_model_creator(addtocart)
order_place_pydantic = pydantic_model_creator(order_placed)
