from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import smtplib
from email.message import EmailMessage

router = APIRouter(
    prefix="",
    tags=["/"]
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


@router.post("/submit")
def submit(request: Request, name: str = Form(), tel: str = Form(), message: str = Form()):
    email_address = "ioann.basic@gmail.com"
    email_password = "ahjwamcgwgqtyrvx"

    msg = EmailMessage()
    msg['Subject'] = 'Email Subject'
    msg['To'] = 'ioann.basic@gmail.com'
    msg.set_content(
        f"""\
    Name : {name}
    tel : {tel}
    Message: {message}
         """,
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    # return "email successfully sent"
    # return "email successfully sent"
    return templates.TemplateResponse("contacts.html", {"request": request})

