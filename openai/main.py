from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resposta = cliente.chat.completions.create(
    messages = [
        {
            "role" : "system",
            "content" : "responda como se estivesse flertando"
        },
        {
            "role":"user",
            "content":"me diga como posso ganhar dinheiro emcima da api do chat gpt"
        }
    ],
    model = "gpt-4"
)

print(resposta.choices[0].message.content)