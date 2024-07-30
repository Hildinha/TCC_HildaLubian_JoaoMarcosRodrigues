### bibliotecas usadas ###
import random
import string

### funcao para simular um uid aleatorio de um cartao ###
def Uid_aleatorio():
    letras = random.choices(string.ascii_lowercase, k=4)
    numeros = random.choices(string.digits, k=4)
    lista = [char for pair in zip(letras, numeros) for char in pair]
    return ''.join(lista)

### gera e imprime na tela um uid que foi gerado pela funcao Uid_aleatorio ###
uid = Uid_aleatorio()
print("UID gerado:", uid)
