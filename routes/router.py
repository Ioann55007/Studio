from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import smtplib
from email.message import EmailMessage
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from routes.models import Message
from routes.scheams import MessagesModel
from studio_database import engine, async_session_maker, get_async_session

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


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(Message).values(
                message=message
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> List[MessagesModel]:
    query = select(Message).order_by(Message.id.desc()).limit(5)
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)


manager = ConnectionManager()


@router.get('/chat')
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
