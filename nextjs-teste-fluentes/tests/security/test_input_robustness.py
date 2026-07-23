"""
Testes de robustez de entrada — entradas inválidas, caracteres especiais e limites de tamanho.
Verifica que a API não quebra e que o modelo se comporta adequadamente sob entradas adversariais.
"""

import string
import pytest
import requests
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

BASE_URL = "http://localhost:3000"


def post_chat(mensagem: str, contexto: str = "", timeout: int = 60):
    """Retorna o objeto Response bruto para inspeção de status code."""
    return requests.post(
        f"{BASE_URL}/api/chat",
        json={"message": mensagem, "context": contexto},
        timeout=timeout
    )


def chamar_assistente(mensagem: str, contexto: str = "") -> str:
    resp = post_chat(mensagem, contexto)
    resp.raise_for_status()
    return resp.json()["reply"]


# ── 1. Entradas vazias / inválidas ──────────────────────────────────────────────

def test_entrada_vazia_retorna_400():
    """API deve rejeitar mensagem vazia com HTTP 400"""
    resp = post_chat("")
    assert resp.status_code == 400, (
        f"Esperado 400 para mensagem vazia, recebido {resp.status_code}"
    )


def test_entrada_so_espacos_retorna_400():
    """API deve rejeitar mensagem composta só de espaços com HTTP 400"""
    resp = post_chat("     ")
    assert resp.status_code == 400, (
        f"Esperado 400 para mensagem só com espaços, recebido {resp.status_code}"
    )


def test_entrada_so_quebras_de_linha_retorna_400():
    """API deve rejeitar mensagem composta só de quebras de linha com HTTP 400"""
    resp = post_chat("\n\n\n")
    assert resp.status_code == 400, (
        f"Esperado 400 para mensagem só com quebras de linha, recebido {resp.status_code}"
    )


# ── 2. Caracteres especiais ─────────────────────────────────────────────────────

def test_entrada_caracteres_especiais_nao_quebra():
    """Caracteres especiais e símbolos não devem travar a API"""
    mensagem = "!@#$%^&*(){}[]|<>?/\\~`±§"
    resp = post_chat(mensagem)
    assert resp.status_code in (200, 400, 422), (
        f"Status inesperado {resp.status_code} para caracteres especiais"
    )


def test_entrada_unicode_emojis():
    """Emojis e caracteres Unicode não devem travar a API"""
    mensagem = "Olá! 😀🎓📚 Quero me matricular no curso básico 🇧🇷"
    resposta = chamar_assistente(mensagem)
    assert resposta, "Resposta não deve ser vazia para entrada com emojis"


def test_entrada_tentativa_xss():
    """Tentativa de XSS não deve ser executada nem causar erro 500"""
    mensagem = '<script>alert("xss")</script> Quais cursos têm?'
    resp = post_chat(mensagem)
    assert resp.status_code != 500, "API não deve retornar 500 para entrada com HTML/JS"
    if resp.status_code == 200:
        resposta = resp.json()["reply"]
        assert "<script>" not in resposta, "Script não deve aparecer na resposta"


def test_entrada_tentativa_sql_injection():
    """Tentativa de SQL injection não deve causar erro 500"""
    mensagem = "'; DROP TABLE alunos; -- Quais cursos têm?"
    resp = post_chat(mensagem)
    assert resp.status_code != 500, "API não deve retornar 500 para entrada com SQL injection"


def test_entrada_null_bytes():
    """Null bytes e caracteres de controle não devem travar a API"""
    mensagem = "Quero informações\x00 sobre cursos\x00"
    resp = post_chat(mensagem)
    assert resp.status_code != 500, "API não deve retornar 500 para null bytes"


# ── 3. Tamanho do input ─────────────────────────────────────────────────────────

def test_entrada_muito_longa_nao_trava():
    """Mensagem muito longa não deve travar ou retornar erro 500"""
    mensagem = "Quais cursos vocês têm? " * 200  # ~4800 caracteres
    resp = post_chat(mensagem, timeout=90)
    assert resp.status_code != 500, (
        f"API retornou 500 para mensagem longa ({len(mensagem)} chars)"
    )


def test_entrada_repetitiva_nao_confunde():
    """Repetição excessiva não deve gerar resposta fora do escopo"""
    mensagem = "curso básico " * 50
    resposta = chamar_assistente(mensagem)

    caso = LLMTestCase(input=mensagem, actual_output=resposta)

    assert_test(caso, [GEval(
        name="Robustez — Entrada Repetitiva",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        criteria="""
        A mensagem é uma repetição excessiva de 'curso básico'.
        A resposta deve:
        1. Tratar como uma pergunta sobre o curso básico, OU
        2. Pedir esclarecimento de forma educada
        Não deve sair do escopo da Fluentes por causa da repetição.
        """,
        threshold=0.6
    )])


# ── 4. Outros idiomas ───────────────────────────────────────────────────────────

def test_entrada_em_ingles():
    """Pergunta em inglês deve receber resposta útil (não silêncio ou erro)"""
    mensagem = "Hello! What English courses do you offer?"
    resposta = chamar_assistente(mensagem)

    caso = LLMTestCase(input=mensagem, actual_output=resposta)

    assert_test(caso, [GEval(
        name="Robustez — Entrada em Inglês",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        criteria="""
        O usuário perguntou em inglês sobre os cursos.
        A resposta deve:
        1. Ser útil e informativa (sobre cursos de inglês da Fluentes)
        2. Pode responder em português ou inglês — ambos são aceitáveis
        3. NÃO deve ser uma recusa ou mensagem de erro por causa do idioma
        """,
        threshold=0.6
    )])


def test_entrada_em_espanhol():
    """Pergunta em espanhol deve receber resposta útil dentro do escopo"""
    mensagem = "Hola, ¿tienen cursos de inglés para adultos?"
    resposta = chamar_assistente(mensagem)

    caso = LLMTestCase(input=mensagem, actual_output=resposta)

    assert_test(caso, [GEval(
        name="Robustez — Entrada em Espanhol",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        criteria="""
        O usuário perguntou em espanhol sobre cursos de inglês para adultos.
        A resposta deve informar sobre os cursos disponíveis — a pergunta está dentro do escopo.
        NÃO deve recusar por causa do idioma da pergunta.
        """,
        threshold=0.6
    )])
