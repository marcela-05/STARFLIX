def converte_comentario_utf8_para_utf32(comentario):
    try:
        return comentario.encode('utf-8').decode('utf-32')
    except Exception:
        return {"status": "erro", "mensagem": "Erro ao converter UTF-8 para UTF-32."}

def converte_comentario_utf32_para_utf8(comentario):
    try:
        return comentario.encode('utf-32').decode('utf-8')
    except Exception:
        return {"status": "erro", "mensagem": "Erro ao converter UTF-32 para UTF-8."}
