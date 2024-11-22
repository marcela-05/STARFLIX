from utils import gerar_id_unico

# Dados mockados
diretores = []

def listar_diretor(diretor_id):
    for d in diretores:
        if d['id'] == diretor_id:
            return {"status": "sucesso", "diretor": d}
    return {"status": "erro", "mensagem": "Nenhum diretor encontrado."}

def buscar_diretor(nome_diretor):
    return [d for d in diretores if nome_diretor.lower() in d['nome'].lower()]
