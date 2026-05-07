from fastapi import FastAPI
from controllers.userController import user_router
from helpers.initialize_tortoise import init
from controllers.fileController import rag_router
from controllers.chatController import chat_router
from tortoise import run_async

app = FastAPI()

app.include_router(user_router, tags=["User"])
app.include_router(rag_router, tags=["Rag"])
app.include_router(chat_router, tags=["Chat"])

run_async(init())

