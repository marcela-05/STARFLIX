from usuarios import (
    cadastrar_usuario, login, atualizar_usuario, deletar_usuario, listar_usuario
)
from filmes import (
    cadastrar_filme, atualizar_filme, deletar_filme, listar_filme, buscar_filme
)
from diretores import criar_diretor, listar_diretor, buscar_diretor
from avaliacao import avaliar_filme, listar_avaliacoes, listar_avaliacoes_por_filme

# Função principal
def menu_principal():
    print("Bem-vindo ao StarFlix!")
    while True:
        print("\n1. Login")
        print("2. Cadastrar Usuário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")
            resposta = login(email, senha)
            if resposta['status'] == 'sucesso':
                usuario = resposta['usuario']
                print(f"\nLogin realizado com sucesso! Bem-vindo(a), {usuario['nome']}.")
                menu_usuario(usuario)
            else:
                print(f"\nErro: {resposta['mensagem']}")
        elif opcao == "2":
            nome = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")
            resposta = cadastrar_usuario(nome, email, senha)
            if resposta['status'] == 'sucesso':
                print("\nUsuário cadastrado com sucesso!")
            else:
                print(f"\nErro: {resposta['mensagem']}")
        elif opcao == "3":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_usuario(usuario):
    while True:
        print("\nMenu do Usuário")
        print("1. Gerenciar Filmes")
        print("2. Gerenciar Avaliações")
        print("3. Atualizar Perfil")
        print("4. Deletar Conta")
        print("5. Sair para o Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_filmes(usuario)
        elif opcao == "2":
            menu_avaliacoes(usuario)
        elif opcao == "3":
            novo_nome = input("Digite o novo nome: ")
            novo_email = input("Digite o novo email: ")
            nova_senha = input("Digite a nova senha: ")
            resposta = atualizar_usuario(usuario['id'], novo_nome, novo_email, nova_senha)
            print(resposta['mensagem'])
        elif opcao == "4":
            resposta = deletar_usuario(usuario['id'])
            print(resposta['mensagem'])
            if resposta['status'] == "sucesso":
                break
        elif opcao == "5":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_filmes(usuario):
    while True:
        print("\nGerenciamento de Filmes")
        print("1. Cadastrar Filme")
        print("2. Atualizar Filme")
        print("3. Deletar Filme")
        print("4. Listar Filme")
        print("5. Buscar Filme por Nome")
        print("6. Voltar ao Menu do Usuário")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do filme: ")
            ano = int(input("Digite o ano do filme: "))
            genero = input("Digite o gênero do filme: ")
            diretor = input("Digite o nome do diretor: ")
            resposta = cadastrar_filme(nome, ano, genero, diretor)
            print(resposta['mensagem'])
        elif opcao == "2":
            filme_id = int(input("Digite o ID do filme: "))
            novo_nome = input("Digite o novo nome do filme: ")
            novo_ano = int(input("Digite o novo ano do filme: "))
            novo_genero = input("Digite o novo gênero do filme: ")
            novo_diretor = input("Digite o novo nome do diretor: ")
            resposta = atualizar_filme(filme_id, novo_nome, novo_ano, novo_genero, novo_diretor)
            print(resposta['mensagem'])
        elif opcao == "3":
            filme_id = int(input("Digite o ID do filme: "))
            resposta = deletar_filme(filme_id)
            print(resposta['mensagem'])
        elif opcao == "4":
            filme_id = int(input("Digite o ID do filme: "))
            resposta = listar_filme(filme_id)
            if resposta['status'] == 'sucesso':
                print(resposta['filme'])
            else:
                print(resposta['mensagem'])
        elif opcao == "5":
            nome = input("Digite o nome do filme para buscar: ")
            filmes = buscar_filme(nome)
            if filmes:
                for filme in filmes:
                    print(filme)
            else:
                print("Nenhum filme encontrado.")
        elif opcao == "6":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_avaliacoes(usuario):
    while True:
        print("\nGerenciamento de Avaliações")
        print("1. Avaliar Filme")
        print("2. Listar Minhas Avaliações")
        print("3. Listar Avaliações de um Filme")
        print("4. Voltar ao Menu do Usuário")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            filme_id = int(input("Digite o ID do filme: "))
            nota = int(input("Digite a nota (1-5): "))
            comentario = input("Digite um comentário (opcional): ")
            resposta = avaliar_filme(filme_id, usuario['id'], nota, comentario)
            print(resposta['mensagem'])
        elif opcao == "2":
            avaliacoes = [a for a in listar_avaliacoes() if a['usuario_id'] == usuario['id']]
            if avaliacoes:
                for avaliacao in avaliacoes:
                    print(avaliacao)
            else:
                print("Você ainda não fez nenhuma avaliação.")
        elif opcao == "3":
            filme_id = int(input("Digite o ID do filme: "))
            avaliacoes = listar_avaliacoes_por_filme(filme_id)
            if avaliacoes:
                for avaliacao in avaliacoes:
                    print(avaliacao)
            else:
                print("Nenhuma avaliação encontrada para este filme.")
        elif opcao == "4":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
