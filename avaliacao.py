avaliacoes = []

def avaliar_filme(filme_id, usuario_id, nota, comentario=""):
    if nota < 1 or nota > 5:
        return "Erro: Nota inválida."
    avaliacoes.append({"filme_id": filme_id, "usuario_id": usuario_id, "nota": nota, "comentario": comentario})
    return "Avaliação registrada com sucesso."

def listar_avaliacoes():
    if not avaliacoes:
        return "Erro: Nenhuma avaliação cadastrada."
    return avaliacoes
