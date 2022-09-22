from models import *
from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



router = APIRouter()



templates = Jinja2Templates(directory="users/templates")



@router.get("/login/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("login.html", {"request": request, "id": id})


