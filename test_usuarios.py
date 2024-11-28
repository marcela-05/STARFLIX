import pytest
from usuarios import cadastrarUsuario, atualizarUsuario, deletarUsuario, listarUsuario, login, resetar_usuarios

# Fixture para configurar o ambiente inicial
@pytest.fixture
def setup_usuarios():
    resetar_usuarios()  # Redefine a lista de usuários para um estado limpo
    # Cadastra um usuário inicial para os testes
    cadastrarUsuario("Teste Inicial", "teste@inicial.com", "senha123")

# Testes para cadastrarUsuario
def test_cadastrar_usuario_sucesso(setup_usuarios):
    resposta = cadastrarUsuario("Novo Usuario", "novo@teste.com", "senhaForte")
    assert resposta["status"] == "sucesso"
    assert "usuario" in resposta
    assert resposta["usuario"]["email"] == "novo@teste.com"

def test_cadastrar_usuario_email_existente(setup_usuarios):
    resposta = cadastrarUsuario("Outro Usuario", "teste@inicial.com", "novaSenha")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Email já cadastrado."

def test_cadastrar_usuario_senha_fraca(setup_usuarios):
    resposta = cadastrarUsuario("Usuario Fraco", "fraco@teste.com", "123")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Senha fraca."

# Testes para atualizarUsuario
def test_atualizar_usuario_sucesso(setup_usuarios):
    usuario = listarUsuario(1)
    if usuario["status"] == "sucesso":
        usuario_id = usuario["usuario"]["id"]
        resposta = atualizarUsuario(usuario_id, "Usuario Atualizado", "atualizado@teste.com", "novaSenhaForte")
        assert resposta["status"] == "sucesso"
        assert resposta["mensagem"] == "Conta atualizada com sucesso."

def test_atualizar_usuario_email_em_uso(setup_usuarios):
    cadastrarUsuario("Outro Usuario", "outro@teste.com", "senhaForte")
    usuario = listarUsuario(1)
    if usuario["status"] == "sucesso":
        usuario_id = usuario["usuario"]["id"]
        resposta = atualizarUsuario(usuario_id, "Novo Nome", "outro@teste.com", "novaSenha")
        assert resposta["status"] == "erro"
        assert resposta["mensagem"] == "Email já em uso."

def test_atualizar_usuario_senha_fraca(setup_usuarios):
    usuario = listarUsuario(1)
    if usuario["status"] == "sucesso":
        usuario_id = usuario["usuario"]["id"]
        resposta = atualizarUsuario(usuario_id, "Usuario Atualizado", "atualizado@teste.com", "123")
        assert resposta["status"] == "erro"
        assert resposta["mensagem"] == "Senha fraca."

# Testes para deletarUsuario
def test_deletar_usuario_sucesso(setup_usuarios):
    usuario = listarUsuario(1)
    if usuario["status"] == "sucesso":
        usuario_id = usuario["usuario"]["id"]
        resposta = deletarUsuario(usuario_id)
        assert resposta["status"] == "sucesso"
        assert resposta["mensagem"] == "Conta excluída com sucesso."

def test_deletar_usuario_inexistente(setup_usuarios):
    resposta = deletarUsuario(999)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Usuário não encontrado."

# Testes para listarUsuario
'''
def test_listar_usuario_sucesso(setup_usuarios):
    resposta = listarUsuario(1)
    assert resposta["status"] == "sucesso"
    assert "usuario" in resposta
    assert resposta["usuario"]["email"] == "teste@inicial.com"

def test_listar_usuario_inexistente(setup_usuarios):
    resposta = listarUsuario(999)
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Usuário não encontrado."
'''
# Testes para login
def test_login_sucesso(setup_usuarios):
    resposta = login("teste@inicial.com", "senha123")
    assert resposta["status"] == "sucesso"

def test_login_email_nao_cadastrado(setup_usuarios):
    resposta = login("inexistente@teste.com", "senha123")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Email não cadastrado."

def test_login_senha_errada(setup_usuarios):
    resposta = login("teste@inicial.com", "senhaErrada")
    assert resposta["status"] == "erro"
    assert resposta["mensagem"] == "Senha errada."
