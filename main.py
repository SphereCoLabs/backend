# Packages
from fastapi import FastAPI
from openai import OpenAI
from web3 import Web3
from decouple import config

# Chat Route
from routes.chat import route as chat_router

app = FastAPI()

app.include_router(chat_router)