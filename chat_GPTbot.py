import os
import sys
from lib.openai import ChatGPT
from lib.iniciar_webdriver_uc import iniciar_webdriver
from lib.colors import *
import telebot
from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
OPENAI_USER = config("OPENAI_USER")
OPENAI_PASS = config("OPENAI_PASS")


bot = telebot.TeleBot(TELEGRAM_TOKEN)

if __name__ == "__main__":
    print(f"{verde}hola{gris}")
    chatGPT=ChatGPT(OPENAI_USER,OPENAI_PASS,headless=False)

    input("wait")

