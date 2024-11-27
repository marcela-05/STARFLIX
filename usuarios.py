from utils import gerar_id_unico, salvar_dados_no_json, carregar_dados_do_json

ARQUIVO_JSON = "dados_starflix.json"
dados = carregar_dados_do_json(ARQUIVO_JSON)
usuarios = dados.get("usuarios", [])

def cadastrarUsuario(nome, email, senha):
    if any(u['email'] == email for u in usuarios):
        return {"status": "erro", "mensagem": "Email já cadastrado."}
    usuario = {"id": gerar_id_unico(usuarios), "nome": nome, "email": email, "senha": senha}
    usuarios.append(usuario)
    salvar_dados_no_json(ARQUIVO_JSON, {"usuarios": usuarios})
    return {"status": "sucesso", "usuario": usuario}

def atualizarUsuario(usuario_id, novo_nome, novo_email, nova_senha):
    for u in usuarios:
        if u['id'] == usuario_id:
            if any(u2['email'] == novo_email and u2['id'] != usuario_id for u2 in usuarios):
                return {"status": "erro", "mensagem": "Email já em uso."}
            u['nome'] = novo_nome
            u['email'] = novo_email
            u['senha'] = nova_senha
            salvar_dados_no_json(ARQUIVO_JSON, {"usuarios": usuarios})
            return {"status": "sucesso", "mensagem": "Conta atualizada com sucesso."}
    return {"status": "erro", "mensagem": "Usuário não encontrado."}

def deletarUsuario(usuario_id):
    global usuarios
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario:
        usuarios = [u for u in usuarios if u['id'] != usuario_id]
        salvar_dados_no_json(ARQUIVO_JSON, {"usuarios": usuarios})
        return {"status": "sucesso", "mensagem": "Conta excluída com sucesso."}
    return {"status": "erro", "mensagem": "Usuário não encontrado."}

def listarUsuario(usuario_id):
    for u in usuarios:
        if u['id'] == usuario_id:
            return {"status": "sucesso", "usuario": u}
    return {"status": "erro", "mensagem": "Usuário não encontrado."}

def login(email, senha):
    for u in usuarios:
        if u['email'] == email:
            if u['senha'] == senha:
                return {"status": "sucesso", "usuario": u}
            else:
                return {"status": "erro", "mensagem": "Senha errada."}
    return {"status": "erro", "mensagem": "Email não cadastrado."}
