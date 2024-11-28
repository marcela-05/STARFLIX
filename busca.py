from utils import carregar_dados_do_json
from filmes import filmes

def buscarFilme(nome, usuario_id):
    if len(nome) == 0:
        return {"status": "erro", "mensagem": "O campo de pesquisa deve ser preenchido."}
    
    encontrados = [
        f for f in filmes 
        if (nome.lower() in f['nome'].lower() or nome.lower() in f['diretor'].lower())
        and f['usuario_id'] == usuario_id
    ]

    if len(encontrados) == 0:
        return {"status": "erro", "mensagem": "Não existem filmes ou diretores com esse nome."}

    return {"status": "sucesso", "filme": encontrados}
