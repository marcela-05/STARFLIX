import random
import json

def gerar_id_unico(lista):
    """
    Gera um ID único baseado na lista existente.
    """
    return random.randint(1000, 9999) if not lista else max(item['id'] for item in lista) + 1

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
