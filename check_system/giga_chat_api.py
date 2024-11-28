from django.shortcuts import get_object_or_404
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
#from pets.settings import API_KEY
from .models import Report
from PIL import Image

from pets.settings import GIGA_API_KEY

def prompt(report_img):

    print(GIGA_API_KEY)

    giga = GigaChat(credentials=GIGA_API_KEY,
                    scope="GIGACHAT_API_PERS",
                    model="GigaChat-Pro-preview",
                    verify_ssl_certs=False,
                    base_url='https://gigachat-preview.devices.sberbank.ru/api/v1/'
                    )
    
    img = report_img.open('rb')

    img = giga.upload_file(img, purpose="general")

    return giga.invoke([HumanMessage(content="Что изображено на картинке? Какое состояние животного? Какое у него настроение?", additional_kwargs={"attachments": [img
                                                                                                                                                                  .id_]})]).content