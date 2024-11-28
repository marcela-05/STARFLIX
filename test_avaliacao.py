import pytest
from avaliacao import avaliarFilme, listarAvaliacao, avaliacoes
from filmes import filmes, cadastrarFilme, salvar_dados_no_json
from utils import salvar_dados_no_json

@pytest.fixture
def setup_dados():
    """
    Fixture para inicializar e limpar os dados de filmes e avaliações.
    """
    global filmes, avaliacoes
    filmes.clear()
    avaliacoes.clear()
    salvar_dados_no_json("dados_starflix.json", {"filmes": filmes, "avaliacoes": avaliacoes})

    # Cadastra um filme para os testes
    cadastrarFilme("Filme Teste", 2020, "Ação", "Diretor Teste", 1)

# Testes para avaliarFilme
def test_avaliar_filme_sucesso(setup_dados):
    resposta = avaliarFilme("Filme Teste", 1, 5, "Ótimo filme!")
    assert resposta["status"] == "sucesso"
    assert resposta["avaliacao"]["nota"] == 5
    assert "comentario_utf32" in resposta["avaliacao"]

def test_avaliar_filme_nao_encontrado(setup_dados):
    resposta = avaliarFilme("Filme Inexistente", 1, 4, "Filme não existe.")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Filme não encontrado."

def test_avaliar_filme_nao_permitido(setup_dados):
    # Cadastra um filme de outro usuário
    cadastrarFilme("Outro Filme", 2021, "Comédia", "Outro Diretor", 2)
    resposta = avaliarFilme("Outro Filme", 1, 4, "Tentativa de avaliar filme de outro usuário.")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Você só pode avaliar filmes que você criou!"

def test_avaliar_filme_nota_invalida(setup_dados):
    resposta = avaliarFilme("Filme Teste", 1, 6, "Nota fora do intervalo permitido.")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Nota inválida."

def test_avaliar_filme_ja_avaliado(setup_dados):
    avaliarFilme("Filme Teste", 1, 4, "Primeira avaliação.")
    resposta = avaliarFilme("Filme Teste", 1, 5, "Segunda tentativa.")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Você já avaliou este filme."
'''
def test_avaliar_filme_comentario_invalido(setup_dados):
    resposta = avaliarFilme("Filme Teste", 1, 4, "")
    assert resposta["status"] == "sucesso"
    assert "comentario_utf32" in resposta["avaliacao"]
'''
# Testes para listarAvaliacao
def test_listar_avaliacao_sucesso(setup_dados):
    avaliarFilme("Filme Teste", 1, 4, "Comentário do teste.")
    resposta = listarAvaliacao(1)
    assert resposta["status"] == "sucesso"
    assert len(resposta["avaliacoes"]) > 0
    assert resposta["avaliacoes"][0]["nota"] == 4
    assert resposta["avaliacoes"][0]["nome_filme"] == "Filme Teste"

def test_listar_avaliacao_vazio(setup_dados):
    resposta = listarAvaliacao(1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Você ainda não fez nenhuma avaliação."

def test_listar_avaliacao_erro_na_conversao(setup_dados, monkeypatch):
    # Simula um erro de conversão para UTF-8
    def mock_converter_comentario_para_utf8(comentario_utf32, dicionario_avaliacoes):
        return -1, ""

    monkeypatch.setattr("avaliacao.converter_comentario_para_utf8", mock_converter_comentario_para_utf8)

    avaliarFilme("Filme Teste", 1, 4, "Comentário para conversão.")
    resposta = listarAvaliacao(1)
    assert resposta["status"] == "sucesso"
    assert resposta["avaliacoes"][0]["comentario"] == "Erro ao converter o comentário."
