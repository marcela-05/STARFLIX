from utils import gerar_id_unico, salvar_dados_no_json, carregar_dados_do_json

ARQUIVO_JSON = "dados_starflix.json"
dados = carregar_dados_do_json(ARQUIVO_JSON)
filmes = dados.get("filmes", [])

def cadastrarFilme(nome, ano, genero, diretor, usuario_id):
    if ano > 2024:
        return {"status": "erro", "mensagem": "Ano inválido. O ano do filme não pode ser maior que 2024."}

    if any(f['nome'].lower() == nome.lower() for f in filmes):
        return {"status": "erro", "mensagem": "Já existe um filme com este nome."}

    filme = {
        "id": gerar_id_unico(filmes),
        "nome": nome,
        "ano": ano,
        "genero": genero,
        "diretor": diretor,
        "usuario_id": usuario_id
    }
    filmes.append(filme)
    salvar_dados_no_json(ARQUIVO_JSON, {"filmes": filmes})
    return {"status": "sucesso", "filme": filme}

def atualizarFilme(filme_id, nome, ano, genero, diretor, usuario_id):
    if ano > 2024:
        return {"status": "erro", "mensagem": "Ano inválido."}

    for f in filmes:
        if f['id'] == filme_id and f['usuario_id'] == usuario_id:
            if any(f2['nome'].lower() == nome.lower() and f2['id'] != filme_id for f2 in filmes):
                return {"status": "erro", "mensagem": "Já existe um filme com este nome."}

            f['nome'] = nome
            f['ano'] = ano
            f['genero'] = genero
            f['diretor'] = diretor
            salvar_dados_no_json(ARQUIVO_JSON, {"filmes": filmes})
            return {"status": "sucesso", "mensagem": "Filme atualizado com sucesso."}
    return {"status": "erro", "mensagem": "Filme não encontrado."}

def deletarFilme(filme_id, usuario_id):
    global filmes
    filmes_iniciais = len(filmes)
    filmes = [f for f in filmes if not (f['id'] == filme_id and f['usuario_id'] == usuario_id)]
    if len(filmes) < filmes_iniciais:
        salvar_dados_no_json(ARQUIVO_JSON, {"filmes": filmes})
        return {"status": "sucesso", "mensagem": "Filme deletado com sucesso."}
    return {"status": "erro", "mensagem": "Filme não encontrado."}

def listarFilme(usuario_id: int) -> dict:
    """
    Lista os filmes cadastrados pelo usuário.

    :param usuario_id: ID do usuário que cadastrou os filmes.
    :return: Dicionário contendo:
        - "status": "sucesso" e a lista de filmes do usuário.
        - "status": "erro" com uma mensagem caso nenhum filme seja encontrado.
    """
    filmes_usuario = [f for f in filmes if f["usuario_id"] == usuario_id]

    if not filmes_usuario:
        return {"status": "erro", "mensagem": "Nenhum filme cadastrado."}

    return {"status": "sucesso", "filmes": filmes_usuario}

def verificar_filme_unico(nome):
    """
    Verifica se um filme com o nome fornecido é único no sistema.

    :param nome: Nome do filme a ser verificado.
    :return: Dicionário contendo:
        - "status": "sucesso" e o filme correspondente se for único.
        - "status": "erro" com uma mensagem se houver mais de um filme ou nenhum filme encontrado.
    """
    # Busca por filmes com o mesmo nome
    encontrados = [f for f in filmes if nome.lower() == f['nome'].lower()]

    # Caso nenhum filme seja encontrado
    if len(encontrados) == 0:
        return {"status": "erro", "mensagem": "Filme não encontrado."}

    # Caso mais de um filme seja encontrado
    elif len(encontrados) > 1:
        return {"status": "erro", "mensagem": "Existe mais de um filme com este nome."}

    # Se apenas um filme for encontrado
    return {"status": "sucesso", "filme": encontrados[0]}
