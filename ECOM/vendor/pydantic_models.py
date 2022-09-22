from pydantic import BaseModel

# VENDER REGISTRATION AND LOGIN USE THIS BASE MODEL
class messageDict(BaseModel):
    emaim:str 
    access_token: str

class loginout(BaseModel):
    status:bool
    message: messageDict
    
    class config:
        orm_mode:True
  
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"   