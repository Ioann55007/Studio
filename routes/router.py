from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/second_page")
def get_second_page(request: Request):
    return templates.TemplateResponse("two.html", {"request": request})


@router.get("/our_services")
def get_our_services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})


@router.get("/contacts")
def get_contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})

