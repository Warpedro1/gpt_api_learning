from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"


def categoriza_sexo(descricao, categorias):
    #engenharia de prompt 
    prompt_system = f"""
        Você é uma categorizador de sexualidades.
            Você deve assumir uma das categorias presentes na lista abaixo.

            # Lista de Categorias Válidas
            {categorias.split(",")}

            # Formato da Saída
            Produto: pontos relevantes
            Categoria: categoria 

            # Exemplo de Saída
            Produto: Pelo fato do usuario beijar homens e mulheres
            Categoria: Bissexual

    """

    resposta = cliente.chat.completions.create(
        messages = [
            {
                "role" : "system",
                "content" : prompt_system
            },
            {
                "role":"user",
                "content": descricao
            }
        ],
        model = modelo,
        temperature = 0.5,
        max_tokens=200,
        #n =3, # qunatidade de respostas devolvidas 
    )
    return resposta

categorias = input("orientacoes sexuais >>>")

while True: 
    descricao = input("informe a descricao do individuo >>>")
    resposta_inteira = categoriza_sexo(descricao,categorias)
    texto_resposta = resposta_inteira.choices[0].message.content
    print(texto_resposta)