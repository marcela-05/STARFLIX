import random

def gerar_id_unico(lista):
    return random.randint(1000, 9999) if not lista else max(item['id'] for item in lista) + 1
