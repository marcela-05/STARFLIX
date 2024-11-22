from utils import gerar_id_unico

# Lista mockada de filmes
filmes = []

# Cadastrar um novo filme
def cadastrar_filme(nome, ano, genero, diretor, usuario_id):
    # Verificar se o ano é válido
    if ano > 2024:
        return {"status": "erro", "mensagem": "Ano inválido. O ano do filme não pode ser maior que 2024."}

    # Verificar se já existe um filme com o mesmo nome (independente do ano)
    if any(f['nome'].lower() == nome.lower() for f in filmes):
        return {"status": "erro", "mensagem": "Já existe um filme com este nome."}

    # Criar o filme
    filme = {
        "id": gerar_id_unico(filmes),
        "nome": nome,
        "ano": ano,
        "genero": genero,
        "diretor": diretor,
        "usuario_id": usuario_id
    }
    filmes.append(filme)
    return {"status": "sucesso", "filme": filme}

# Verificar se um filme tem um nome único
def verificar_filme_unico(nome):
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

def atualizar_filme(filme_id, nome, ano, genero, diretor, usuario_id):
    # Verificar se o ano é válido
    if ano > 2024:
        return {"status": "erro", "mensagem": "Ano inválido. O ano do filme não pode ser maior que 2024."}

    for f in filmes:
        if f['id'] == filme_id and f['usuario_id'] == usuario_id:
            # Verifica se já existe outro filme com o mesmo nome
            if any(f2['nome'].lower() == nome.lower() and f2['id'] != filme_id for f2 in filmes):
                return {"status": "erro", "mensagem": "Já existe um filme com este nome."}

            # Atualiza o filme
            f['nome'] = nome
            f['ano'] = ano
            f['genero'] = genero
            f['diretor'] = diretor
            return {"status": "sucesso", "mensagem": "Filme atualizado com sucesso."}
    return {"status": "erro", "mensagem": "Filme não encontrado ou você não tem permissão para editá-lo."}

# Deletar um filme
def deletar_filme(filme_id, usuario_id):
    global filmes
    filmes_iniciais = len(filmes)
    filmes = [f for f in filmes if not (f['id'] == filme_id and f['usuario_id'] == usuario_id)]
    if len(filmes) < filmes_iniciais:
        return {"status": "sucesso", "mensagem": "Filme deletado com sucesso."}
    return {"status": "erro", "mensagem": "Filme não encontrado ou você não tem permissão para excluí-lo."}

# Listar todos os filmes de um usuário específico
def listar_filmes_por_usuario(usuario_id):
    filmes_usuario = [f for f in filmes if f['usuario_id'] == usuario_id]
    if not filmes_usuario:
        return {"status": "erro", "mensagem": "Nenhum filme cadastrado."}
    return {"status": "sucesso", "filmes": filmes_usuario}