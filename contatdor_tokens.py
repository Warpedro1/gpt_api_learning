import tiktoken 
#contabilizar qunatos tokens possuem um trecho de texto
# ajuda a monetizar os recursos de forma mais adequada

#A helpful rule of thumb is that one token generally corresponds to ~4 characters of text for common English text. 
#This translates to roughly ¾ of a word (so 100 tokens ~= 75 words).

modelo = "gpt-4"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode("voce é um categorizador de produtos") #devolve a lista de tokens que formam a frase

print("Lista de tokens >>>", lista_tokens)
print("Quantidade de tokens >>>", len(lista_tokens))
print(f"Custo para o {modelo} é de ${(len(lista_tokens)/1000)*0.03} >>>") #para ver o preco dos tokens por modelo, platform.openai.com/pricing
