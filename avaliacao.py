from utils import gerar_id_unico
from filmes import filmes, verificar_filme_unico

# Dados mockados
avaliacoes = []

def avaliar_filme_por_nome(nome_filme, usuario_id, nota, comentario=""):
    # Verificar se o filme é único
    resposta = verificar_filme_unico(nome_filme)
    if resposta["status"] == "erro":
        return resposta

    filme = resposta["filme"]

    # Verificar se o usuário já avaliou o filme
    if any(a for a in avaliacoes if a["filme_id"] == filme["id"] and a["usuario_id"] == usuario_id):
        return {"status": "erro", "mensagem": "Você já avaliou este filme."}

    # Validar a nota
    if not (1 <= nota <= 5):
        return {"status": "erro", "mensagem": "Nota inválida. Deve ser entre 1 e 5."}

    # Criar a avaliação
    avaliacao = {
        "id": gerar_id_unico(avaliacoes),
        "filme_id": filme["id"],
        "usuario_id": usuario_id,
        "nota": nota,
        "comentario": comentario
    }
    avaliacoes.append(avaliacao)
    return {"status": "sucesso", "avaliacao": avaliacao}


def listar_avaliacoes_por_usuario(usuario_id):
    # Retorna avaliações do usuário com os nomes dos filmes
    avaliacoes_usuario = [
        {
            "nota": a["nota"],
            "comentario": a["comentario"],
            "nome_filme": next((f["nome"] for f in filmes if f["id"] == a["filme_id"]), "Desconhecido")
        }
        for a in avaliacoes if a["usuario_id"] == usuario_id
    ]
    if not avaliacoes_usuario:
        return {"status": "erro", "mensagem": "Você ainda não fez nenhuma avaliação."}
    return {"status": "sucesso", "avaliacoes": avaliacoes_usuario}
