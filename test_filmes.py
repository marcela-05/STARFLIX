import pytest
from filmes import (
    cadastrarFilme,
    atualizarFilme,
    deletarFilme,
    listarFilme,
    verificar_filme_unico,
    buscarFilme,
)
from filmes import filmes, salvar_dados_no_json  # Import necessário para resetar dados

@pytest.fixture
def setup_filmes():
    """
    Fixture para limpar e configurar o ambiente inicial para os testes.
    """
    global filmes
    filmes.clear()
    salvar_dados_no_json("dados_starflix.json", {"filmes": filmes})
    cadastrarFilme("Filme Teste", 2020, "Ação", "Diretor Teste", 1)

# Testes para cadastrarFilme
def test_cadastrar_filme_sucesso(setup_filmes):
    resposta = cadastrarFilme("Novo Filme", 2021, "Drama", "Outro Diretor", 1)
    assert resposta["status"] == "sucesso"
    assert resposta["filme"]["nome"] == "Novo Filme"

def test_cadastrar_filme_ano_invalido(setup_filmes):
    resposta = cadastrarFilme("Filme Futuro", 2025, "Sci-fi", "Diretor Futuro", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Ano inválido. O ano do filme não pode ser maior que 2024."

def test_cadastrar_filme_nome_duplicado(setup_filmes):
    resposta = cadastrarFilme("Filme Teste", 2020, "Ação", "Diretor Teste", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Já existe um filme com este nome."

# Testes para atualizarFilme
def test_atualizar_filme_sucesso(setup_filmes):
    filme = filmes[0]
    resposta = atualizarFilme(filme["id"], "Filme Atualizado", 2021, "Comédia", "Novo Diretor", 1)
    assert resposta["status"] == "sucesso"
    assert resposta["mensagem"] == "Filme atualizado com sucesso."

def test_atualizar_filme_ano_invalido(setup_filmes):
    filme = filmes[0]
    resposta = atualizarFilme(filme["id"], "Filme Atualizado", 2025, "Comédia", "Novo Diretor", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Ano inválido."

def test_atualizar_filme_nao_encontrado(setup_filmes):
    resposta = atualizarFilme(999, "Inexistente", 2021, "Comédia", "Diretor", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Filme não encontrado."

# Testes para deletarFilme
def test_deletar_filme_sucesso(setup_filmes):
    filme = filmes[0]
    resposta = deletarFilme(filme["id"], 1)
    assert resposta["status"] == "sucesso"
    assert resposta["mensagem"] == "Filme deletado com sucesso."

def test_deletar_filme_nao_encontrado(setup_filmes):
    resposta = deletarFilme(999, 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Filme não encontrado."

# Testes para listarFilme
'''
def test_listar_filme_sucesso(setup_filmes):
    resposta = listarFilme(1)
    assert resposta["status"] == "sucesso"
    assert len(resposta["filmes"]) > 0

def test_listar_filme_vazio(setup_filmes):
    global filmes
    filmes.clear()
    salvar_dados_no_json("dados_starflix.json", {"filmes": filmes})
    resposta = listarFilme(1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Nenhum filme cadastrado."
'''
# Testes para verificar_filme_unico
def test_verificar_filme_unico_sucesso(setup_filmes):
    resposta = verificar_filme_unico("Filme Teste")
    assert resposta["status"] == "sucesso"
    assert resposta["filme"]["nome"] == "Filme Teste"

def test_verificar_filme_unico_nao_encontrado(setup_filmes):
    resposta = verificar_filme_unico("Inexistente")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Filme não encontrado."

def test_verificar_filme_unico_duplicado(setup_filmes):
    cadastrarFilme("Filme Teste", 2021, "Drama", "Outro Diretor", 2)
    resposta = verificar_filme_unico("Filme Teste")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Existe mais de um filme com este nome."

# Testes para buscarFilme
def test_buscar_filme_sucesso(setup_filmes):
    resposta = buscarFilme("Filme", 1)
    assert resposta["status"] == "sucesso"
    assert len(resposta["filme"]) > 0

def test_buscar_filme_vazio(setup_filmes):
    resposta = buscarFilme("", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "O campo de pesquisa deve ser preenchido."

def test_buscar_filme_nao_encontrado(setup_filmes):
    resposta = buscarFilme("Inexistente", 1)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Não existem filmes com esse nome."
