import pytest
from conversao import converter_comentario_para_utf32, converter_comentario_para_utf8

@pytest.fixture
def setup_avaliacoes():
    """
    Fixture para criar um dicionário fictício de avaliações.
    """
    return {
        "avaliacoes": [
            {"id": 1, "comentario": "Ótimo filme!"},
            {"id": 2, "comentario": "Muito ruim."}
        ]
    }

# Testes para converter_comentario_para_utf32
def test_converter_comentario_para_utf32_sucesso(setup_avaliacoes):
    comentario = "Teste UTF-32"
    status, resultado = converter_comentario_para_utf32(comentario, setup_avaliacoes)
    assert status == 1
    assert isinstance(resultado, bytearray)
    assert resultado.startswith(bytearray([0xFF, 0xFE, 0x00, 0x00]))  # Verifica o cabeçalho BOM

def test_converter_comentario_para_utf32_comentario_vazio(setup_avaliacoes):
    comentario = ""
    status, resultado = converter_comentario_para_utf32(comentario, setup_avaliacoes)
    assert status == -1
    assert resultado == ""

def test_converter_comentario_para_utf32_caracteres_especiais(setup_avaliacoes):
    comentario = "🔥💡✨"
    status, resultado = converter_comentario_para_utf32(comentario, setup_avaliacoes)
    assert status == 1
    assert isinstance(resultado, bytearray)

# Testes para converter_comentario_para_utf8
def test_converter_comentario_para_utf8_sucesso(setup_avaliacoes):
    comentario_utf32 = "Teste UTF-32"
    _, comentario_utf32_bytes = converter_comentario_para_utf32(comentario_utf32, setup_avaliacoes)
    status, resultado = converter_comentario_para_utf8(comentario_utf32_bytes.decode('utf-32'), setup_avaliacoes)
    assert status == 1
    assert isinstance(resultado, str)
    assert resultado == comentario_utf32

def test_converter_comentario_para_utf8_comentario_vazio(setup_avaliacoes):
    comentario_utf32 = ""
    status, resultado = converter_comentario_para_utf8(comentario_utf32, setup_avaliacoes)
    assert status == -1
    assert resultado == ""
'''
def test_converter_comentario_para_utf8_formato_invalido(setup_avaliacoes):
    comentario_utf32 = b"\x00\x01\x02\x03".decode('utf-8', errors="ignore")
    status, resultado = converter_comentario_para_utf8(comentario_utf32, setup_avaliacoes)
    assert status == -1
    assert resultado == ""
'''