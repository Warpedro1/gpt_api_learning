from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

codificador = tiktoken.encoding_for_model(modelo)

def carrega(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as arquivo: # with garante a execucao segura do codigo com a manipulacao de recursos que precisam
            dados = arquivo.read()               # ser liberados ou fechados apos o uso, como arquivos ou conexoes de rede. Fazendo isso de maneira automatica e segura
            return dados
    except IOError as e:    # IOError >>> problema relacionado à operação de entrada/saída (I/O).Isto inclui operações como abrir,  
        print(f"Erro: {e}") # ler ou gravar arquivos, ou operações de rede, que envolvem comunicação com outros dispositivos ou sistemas.

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("dados\lista_de_compras_100_clientes.csv")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario) # a somatoria nao pode ser superiro ao que o modelo suporta
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = "gpt-4-1106-preview"

print(f"Modelo escolhido: {modelo}")

lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=modelo
)

print(resposta.choices[0].message.content)