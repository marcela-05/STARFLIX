from utils import gerar_id_unico

usuarios = []

def cadastrar_usuario(nome, email, senha):
    if any(u['email'] == email for u in usuarios):
        return "Erro: Email já cadastrado."
    if len(senha) < 6:
        return "Erro: Senha muito fraca."
    if "@" not in email:
        return "Erro: Email inválido."
    if not nome or not email:
        return "Erro: Campos obrigatórios não preenchidos."

    usuario_id = gerar_id_unico(usuarios)
    novo_usuario = {"id": usuario_id, "nome": nome, "email": email, "senha": senha}
    usuarios.append(novo_usuario)
    return f"Usuário cadastrado com sucesso! ID: {usuario_id}"

def listar_usuarios():
    if not usuarios:
        return "Nenhum usuário cadastrado."
    return [f"ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']}" for u in usuarios]

def atualizar_usuario(usuario_id, novo_nome, novo_email, nova_senha):
    for u in usuarios:
        if u['id'] == usuario_id:
            if any(u2['email'] == novo_email for u2 in usuarios if u2['id'] != usuario_id):
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

def menu_usuario():
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Deletar Usuário")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            print(cadastrar_usuario(nome, email, senha))

        elif opcao == "2":
            usuarios_cadastrados = listar_usuarios()
            if isinstance(usuarios_cadastrados, str):
                print(usuarios_cadastrados)
            else:
                for u in usuarios_cadastrados:
                    print(u)

        elif opcao == "3":
            usuario_id = int(input("ID do Usuário: "))
            novo_nome = input("Novo Nome: ")
            novo_email = input("Novo Email: ")
            nova_senha = input("Nova Senha: ")
            print(atualizar_usuario(usuario_id, novo_nome, novo_email, nova_senha))

        elif opcao == "4":
            usuario_id = int(input("ID do Usuário: "))
            print(deletar_usuario(usuario_id))

        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")
