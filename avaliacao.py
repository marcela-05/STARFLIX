from utils import gerar_id_unico, salvar_dados_no_json, carregar_dados_do_json
from filmes import verificar_filme_unico, filmes
from conversao import converter_comentario_para_utf32, converter_comentario_para_utf8

# Nome do arquivo JSON para persistência
ARQUIVO_JSON = "dados_starflix.json"

# Carregar dados existentes do arquivo JSON
dados = carregar_dados_do_json(ARQUIVO_JSON)
avaliacoes = dados.get("avaliacoes", [])

def avaliarFilme(nome_filme: str, usuario_id: int, nota: int, comentario: str = "") -> dict:
    resposta = verificar_filme_unico(nome_filme)
    if resposta["status"] == "erro":
        return resposta

    filme = resposta["filme"]
    if any(a for a in avaliacoes if a["filme_id"] == filme["id"] and a["usuario_id"] == usuario_id):
        return {"status": "erro", "mensagem": "Você já avaliou este filme."}

    if not (1 <= nota <= 5):
        return {"status": "erro", "mensagem": "Nota inválida."}

    status_conversao, comentario_utf32 = converter_comentario_para_utf32(comentario, avaliacoes)
    if status_conversao != 1:
        return {"status": "erro", "mensagem": "Falha ao converter o comentário para UTF-32."}

    avaliacao = {
        "id": gerar_id_unico(avaliacoes),
        "filme_id": filme["id"],
        "usuario_id": usuario_id,
        "nota": nota,
        "comentario_utf32": comentario_utf32.hex()
    }
    avaliacoes.append(avaliacao)
    salvar_dados_no_json(ARQUIVO_JSON, {"avaliacoes": avaliacoes})
    return {"status": "sucesso", "avaliacao": avaliacao}

def listarAvaliacao(usuario_id: int) -> dict:
    """
    Lista todas as avaliações feitas pelo usuário.

    :param usuario_id: ID do usuário cujas avaliações serão listadas.
    :return: Dicionário contendo:
        - "status": "sucesso" e a lista de avaliações do usuário.
        - "status": "erro" com uma mensagem caso nenhum filme seja encontrado.
    """
    avaliacoes_usuario = []

    for a in avaliacoes:
        if a["usuario_id"] == usuario_id:
            comentario_utf32 = bytes.fromhex(a["comentario_utf32"])
            status_conversao, comentario_utf8 = converter_comentario_para_utf8(
                comentario_utf32.decode('utf-32'), avaliacoes
            )

            if status_conversao != 1:
                comentario_utf8 = "Erro ao converter o comentário."

            avaliacoes_usuario.append({
                "nota": a["nota"],
                "comentario": comentario_utf8,
                "nome_filme": next((f["nome"] for f in filmes if f["id"] == a["filme_id"]), "Desconhecido")
            })

    if not avaliacoes_usuario:
        return {"status": "erro", "mensagem": "Você ainda não fez nenhuma avaliação."}

    return {"status": "sucesso", "avaliacoes": avaliacoes_usuario}
