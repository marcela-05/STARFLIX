import json

def salvar_dados_no_json(nome_arquivo: str, dados: dict):
    """
    Salva os dados em um arquivo JSON para persistência.

    :param nome_arquivo: Nome do arquivo JSON onde os dados serão salvos.
    :param dados: Dicionário contendo os dados a serem salvos.
    """
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar os dados no arquivo {nome_arquivo}: {e}")


def carregar_dados_do_json(nome_arquivo: str) -> dict:
    """
    Carrega os dados de um arquivo JSON.

    :param nome_arquivo: Nome do arquivo JSON de onde os dados serão carregados.
    :return: Dicionário com os dados carregados.
    """
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (IOError, json.JSONDecodeError):
        return {}


def converter_comentario_para_utf32(comentario: str, dicionario_avaliacoes: dict) -> tuple:
    """
    Converte um comentário de texto UTF-8 para UTF-32 (little-endian).

    :param comentario: Texto do comentário em formato UTF-8.
    :param dicionario_avaliacoes: Dicionário que contém as avaliações registradas no sistema.
    :return: Tupla com:
        - (-1, ""): Parâmetros inválidos ou ausência de dados.
        - (1, comentario_utf32): Comentário convertido com sucesso em UTF-32.
    """
    if not comentario:
        return -1, ""  # Comentário vazio ou inválido

    try:
        comentario_bytes = comentario.encode('utf-8')
    except UnicodeEncodeError:
        return -1, ""  # Comentário em formato inválido

    # Cria o cabeçalho BOM para UTF-32 little-endian
    cabecalho_utf32 = [0xFF, 0xFE, 0x00, 0x00]
    comentario_utf32 = bytearray(cabecalho_utf32)

    for char in comentario:
        unicode_char = ord(char)
        comentario_utf32.extend(unicode_char.to_bytes(4, 'little'))

    return 1, comentario_utf32


def converter_comentario_para_utf8(comentario_utf32: str, dicionario_avaliacoes: dict) -> tuple:
    """
    Converte um comentário do formato UTF-32 para UTF-8.

    :param comentario_utf32: Texto do comentário em formato UTF-32.
    :param dicionario_avaliacoes: Dicionário que contém as avaliações registradas no sistema.
    :return: Tupla com:
        - (-1, ""): Parâmetros inválidos ou ausência de dados.
        - (1, comentario_utf8): Comentário convertido com sucesso.
    """
    if not comentario_utf32:
        return -1, ""  # Parâmetros inválidos

    try:
        comentario_bytes = comentario_utf32.encode('utf-32')
    except UnicodeEncodeError:
        return -1, ""  # Formato inválido

    # Detecta o cabeçalho BOM para endianess
    if comentario_bytes[:4] == b'\xFF\xFE\x00\x00':
        little_endian = True
    elif comentario_bytes[:4] == b'\x00\x00\xFE\xFF':
        little_endian = False
    else:
        return -1, ""  # BOM inválido

    comentario_utf8 = bytearray()
    i = 4
    while i < len(comentario_bytes):
        if little_endian:
            unicode_char = int.from_bytes(comentario_bytes[i:i+4], 'little')
        else:
            unicode_char = int.from_bytes(comentario_bytes[i:i+4], 'big')
        i += 4

        if unicode_char < 0x80:
            comentario_utf8.append(unicode_char)
        elif unicode_char < 0x800:
            comentario_utf8.extend([
                0xC0 | (unicode_char >> 6),
                0x80 | (unicode_char & 0x3F)
            ])
        elif unicode_char < 0x10000:
            comentario_utf8.extend([
                0xE0 | (unicode_char >> 12),
                0x80 | ((unicode_char >> 6) & 0x3F),
                0x80 | (unicode_char & 0x3F)
            ])
        else:
            comentario_utf8.extend([
                0xF0 | (unicode_char >> 18),
                0x80 | ((unicode_char >> 12) & 0x3F),
                0x80 | ((unicode_char >> 6) & 0x3F),
                0x80 | (unicode_char & 0x3F)
            ])

    return 1, comentario_utf8.decode('utf-8')
