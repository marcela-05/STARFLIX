from utils import gerar_id_unico

filmes = []

def cadastrar_filme(nome, ano, genero, diretor):
    if ano > 2024:
        return "Erro: Ano inválido."
    filme_id = gerar_id_unico(filmes)
    novo_filme = {"id": filme_id, "nome": nome, "ano": ano, "genero": genero, "diretor": diretor}
    filmes.append(novo_filme)
    return f"Filme cadastrado com sucesso! ID: {filme_id}"

def listar_filmes():
    if not filmes:
        return "Nenhum filme cadastrado."
    return [f"ID: {f['id']} | Nome: {f['nome']} | Ano: {f['ano']} | Diretor: {f['diretor']}" for f in filmes]

def atualizar_filme(filme_id, novo_nome, novo_ano, novo_genero, novo_diretor):
    for f in filmes:
        if f['id'] == filme_id:
            if novo_ano > 2024:
                return "Erro: Ano inválido."
            f.update({"nome": novo_nome, "ano": novo_ano, "genero": novo_genero, "diretor": novo_diretor})
            return "Filme atualizado com sucesso."
    return "Erro: Filme não encontrado."

def deletar_filme(filme_id):
    for f in filmes:
        if f['id'] == filme_id:
            filmes.remove(f)
            return "Filme excluído com sucesso."
    return "Erro: Filme não encontrado."

def menu_filme():
    while True:
        print("\n--- Gerenciar Filmes ---")
        print("1. Cadastrar Filme")
        print("2. Listar Filmes")
        print("3. Atualizar Filme")
        print("4. Deletar Filme")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do Filme: ")
            ano = int(input("Ano de Lançamento: "))
            genero = input("Gênero: ")
            diretor = input("Diretor: ")
            print(cadastrar_filme(nome, ano, genero, diretor))

        elif opcao == "2":
            filmes_cadastrados = listar_filmes()
            if isinstance(filmes_cadastrados, str):
                print(filmes_cadastrados)
            else:
                for f in filmes_cadastrados:
                    print(f)

        elif opcao == "3":
            filme_id = int(input("ID do Filme: "))
            novo_nome = input("Novo Nome: ")
            novo_ano = int(input("Novo Ano: "))
            novo_genero = input("Novo Gênero: ")
            novo_diretor = input("Novo Diretor: ")
            print(atualizar_filme(filme_id, novo_nome, novo_ano, novo_genero, novo_diretor))

        elif opcao == "4":
            filme_id = int(input("ID do Filme: "))
            print(deletar_filme(filme_id))

        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")
