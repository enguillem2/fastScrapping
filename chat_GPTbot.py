import os
import sys
from lib.openai import ChatGPT
from lib.iniciar_webdriver_uc import iniciar_webdriver
from lib.colors import *
import telebot
from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_ENBITBOT")
OPENAI_USER = config("OPENAI_USER")
OPENAI_PASS = config("OPENAI_PASS")


bot = telebot.TeleBot(TELEGRAM_TOKEN)
chatGPT=ChatGPT(OPENAI_USER,OPENAI_PASS,headless=False)


@bot.message_handler(content_types=["text"])
def mensajes_recibidos(m):
    print(m.text)
    respuesta=chatGPT.chatear(m.text)
    bot.send_message(m.chat.id,respuesta,parse_mode="html",disable_web_page_preview=True)



if __name__ == "__main__":
    # print(f"{verde}hola{gris}")
    print(f'{verde} bot iniciado{gris}')
    bot.infinity_polling()

    # prompt=""
    # prompt=input("pregunta: ")
    # while prompt!="salir":
    #     respuesta=chatGPT.chatear(prompt)
    #     print(f'\33[K{amarillo}{respuesta}{negro}')
    #     prompt=input("pregunta: ")
    chatGPT.cerrar()
    sys.exit()

