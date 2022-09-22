# USE PYDANTIC ADD TO CART PRODUCT 
from typing import Optional, List
import uuid
from pydantic import BaseModel


class cartItems(BaseModel):
    product_id:str 
    quantity: int 
    flag: str


class productPydantic(BaseModel):
    id: uuid.UUID
    title: str 
    slug: str
    selling_price: Optional[int] = None
    discounted_price: Optional[int] = None
    description: Optional[str]
    brand: Optional[str]
    quantity: Optional[int] = None  
    product_sub_total : Optional[int]= None
    

class products(BaseModel):
    id: uuid.UUID
    title: str 
    slug: str
    selling_price: Optional[int] = None
    discounted_price: Optional[int] = None
    description: Optional[str]
    brand: Optional[str]
    quantity: Optional[int] = None 
    product_image:str
    product_sub_total : Optional[int]= None
    
class Itemcart(BaseModel):
    products:Optional[List[products]]
    bill_amount : Optional[float] = None
      
class Update_status(BaseModel):
    status:Optional[str]= None    