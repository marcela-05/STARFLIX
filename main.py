from usuarios import menu_usuario
from filmes import menu_filme
#from diretores import menu_diretor
#from avaliacao import menu_avaliacao

def menu_principal():
    print("Bem-vindo ao StarFlix!")
    while True:
        print("\nMenu Principal:")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Filmes")
        print("3. Avaliar Filmes")
        print("4. Gerenciar Diretores")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            menu_usuario()
        elif opcao == "2":
            menu_filme()
        #elif opcao == "3":
            #menu_avaliacao()
        #elif opcao == "4":
            #menu_diretor()
        elif opcao == "5":
            print("Saindo... Obrigado por usar o StarFlix!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
