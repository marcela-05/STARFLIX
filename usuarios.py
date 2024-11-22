usuarios = []

def cadastrar_usuario(usuario_id, nome, email, senha):
    if any(u['email'] == email for u in usuarios):
        return "Erro: Email já cadastrado."
    if len(senha) < 6:
        return "Erro: Senha muito fraca."
    if "@" not in email:
        return "Erro: Email inválido."
    if not nome or not email:
        return "Erro: Campos obrigatórios não preenchidos."
    usuarios.append({"id": usuario_id, "nome": nome, "email": email, "senha": senha})
    return "Usuário cadastrado com sucesso."

def atualizar_usuario(usuario_id, novo_nome, novo_email, nova_senha):
    for u in usuarios:
        if u['id'] == usuario_id:
            if any(u['email'] == novo_email for u in usuarios if u['id'] != usuario_id):
                return "Erro: Email já em uso."
            if len(nova_senha) < 6:
                return "Erro: Senha muito fraca."
            if not novo_nome or not novo_email:
                return "Erro: Campos obrigatórios não preenchidos."
            u.update({"nome": novo_nome, "email": novo_email, "senha": nova_senha})
            return "Usuário atualizado com sucesso."
    return "Erro: Usuário não encontrado."

def deletar_usuario(usuario_id):
    for u in usuarios:
        if u['id'] == usuario_id:
            usuarios.remove(u)
            return "Usuário excluído com sucesso."
    return "Erro: Usuário não encontrado."

def listar_usuario(usuario_id):
    for u in usuarios:
        if u['id'] == usuario_id:
            return u
    return "Erro: Usuário não encontrado."
