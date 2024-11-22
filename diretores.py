from utils import gerar_id_unico

# Dados mockados
diretores = []

def criar_diretor(nome_diretor):
    if any(d['nome'] == nome_diretor for d in diretores):
        return {"status": "erro", "mensagem": "Diretor já cadastrado."}
    diretor = {"id": gerar_id_unico(diretores), "nome": nome_diretor}
    diretores.append(diretor)
    return {"status": "sucesso", "diretor": diretor}

def listar_diretor(diretor_id):
    for d in diretores:
        if d['id'] == diretor_id:
            return {"status": "sucesso", "diretor": d}
    return {"status": "erro", "mensagem": "Nenhum diretor encontrado."}

def buscar_diretor(nome_diretor):
    return [d for d in diretores if nome_diretor.lower() in d['nome'].lower()]
