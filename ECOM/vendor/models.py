import email
from pyexpat import model
from fastapi import FastAPI
from typing import Optional
from tortoise.models import Model
from datetime import datetime
from tortoise import Tortoise,fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Vendor(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(80)
    Mobile = fields.CharField(10,unique =True)
    alternet_mobile_number = fields.CharField(10, unique =True)
    email = fields.CharField(50, unique =True)
    business_name = fields.CharField(200, unique =True)
    shop_image = fields.TextField()
    password = fields.CharField(250)
    shop_documents = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)    
    is_active = fields.BooleanField(default=True)

   
class vendor_products(Model):
    product = fields.ForeignKeyField("models.product", related_name = "vendor_products",on_delete="CASCADE")
    vendor = fields.ForeignKeyField("models.Vendor", related_name = "saller_profile", on_delete="CASCADE")
    created_at = fields.DatetimeField(auto_now_add=True)    
   

Tortoise.init_models(['vendor.models','user.models'], 'models')
