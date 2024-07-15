from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

modelo = "gpt-4"

def carrega(nome_arquivo):
    try:
        with open(nome_arquivo,"r") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_arquivo, conteudo):
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Error ao salvar: {e}")

def analisador_transacoes(lista_transacoes):
    print("1. Executando analise de transacoes")

    prompt_sistema= """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """
   
    
    message_list = [
        {
            "role":"system",
            "content": prompt_sistema
        },
        {
            "role":"user",
            "content": f"Considere o CSV abaixo, onde cada linha é uma transacao diferente: {lista_transacoes}. Sua resposta deve adotar o #Formato de Respota (apenas um json sem outros comentarios)"
        }
    ]
    try: 
        resposta = client.chat.completions.create(
            messages=message_list,
            model=modelo,
            temperature=0
        )
        
        texto = resposta.choices[0].message.content.replace("'",'"')
        json_result = json.loads(texto)
        return json_result
    except openai.AuthenticationError as e:
        print(f"Erro de autenticacao: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")

def gerar_parecer(transacao):
    
    print("2. Gerando parecer para transacao ", transacao["id"])
    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """
        
    lista_mensagem = [ 
        {
            "role":"user",
            "content": prompt_sistema
        }
    ]
    try:
        resposta = client.chat.completions.create(
            messages=lista_mensagem,
            model=modelo
        )
    except openai.APIError as e:
        print(f"Erro de  API: {e}")
    
    conteudo = resposta.choices[0].message.content
    print("FINALIZOU A GERACÃO DO PARECER")
    return conteudo

def gerar_recomendacao(parecer):
    print("3. Gerando recomendacoes")    
    prompt_sistema=f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {parecer}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável. 
    """
    list_mensagem = [
        {
            "role":"system",
            "content": prompt_sistema
        }
    ]

    try :
        resposta = client.chat.completions.create(
            messages=list_mensagem,
            model=modelo
        )
    except openai.APIError as e:
        print(f"Erro de API enquanto gera recomendacao: {e}")

    texto = resposta.choices[0].message.content
    print("finalizou a geracao de recomendacao")
    return texto

lista_transacoes = analisador_transacoes(carrega("transacoes.csv"))

for transacao in lista_transacoes["transacoes"]:
    if transacao["status"] == "Possível Fraude":
        parecer = gerar_parecer(transacao)
        recomendacao = gerar_recomendacao(parecer)
        id_transacao = transacao["id"]
        produto_transacao = transacao["nome_produto"]
        status_transacao = transacao["status"]
        salva(f"transacao-{id_transacao}-{produto_transacao}-{status_transacao}.txt", recomendacao)
