from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

def carrega(nome_arquivo):
    try:        
        with open(nome_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_arquivo, conteudo):
    try:
        with open(nome_arquivo, "w", encoding = "utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}") 

def analisador_sentimentos(produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

    prompt_usuario = carrega(f"./dados/avaliacoes-{produto}.txt") 
    print(f"Iniciou a analise de sentimentos do produto {produto}")

    messages_list = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role":"user",
            "content": prompt_usuario
        }
    ] 
    try:       
        resposta = client.chat.completions.create(
            messages=messages_list,
            model=modelo
        )

        texto = resposta.choices[0].message.content
        salva(f"./dados/analise-{produto}.txt", texto)
    except openai.AuthenticationError as e:
        print(f"Erro de autenticacao: {e}")
    except openai.APIError as e:
        print(f"Erro de api: {e}")


lista_de_produtos = []
analisador_sentimentos("Maquiagem mineral")