import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from tests.helpers import chamar_assistente, carregar_golden_dataset, JUDGE_MODEL


# Carrega o dataset completo e filtra perguntas de fora do escopo do chatbot
# Exemplos: Previsão do tempo (índice 35), receita de bolo (índice 36), Copa do Mundo (índice 37)
dataset = carregar_golden_dataset()
casos_fora_de_escopo = [
    dataset[35],  # Previsão do tempo
    dataset[36],  # Receita de bolo
    dataset[37]   # Copa do Mundo
]

@pytest.mark.parametrize("caso_data", casos_fora_de_escopo, ids=[
    "previsao_tempo",
    "receita_bolo",
    "copa_mundo"
])
def test_scope_guardrail_fora_do_escopo(caso_data):
    """Garante que o assistente recuse responder temas fora do escopo (Guardrail de Escopo - GRD)"""
    pergunta = caso_data["input"]
    # Regra base contida nas diretrizes de escopo
    contexto_controle = ["O assistente responde apenas sobre cursos de idiomas (Inglês, Espanhol, Francês, Italiano, Alemão, Japonês e Coreano) e serviços oferecidos pela IA Fluentes. Deve recusar educadamente outros assuntos."]
    
    resposta = chamar_assistente(pergunta)
    
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta,
        context=contexto_controle
    )
    
    # HallucinationMetric compara o output com o context de controle
    # O threshold baixo (0.3) significa que qualquer desvio para inventar a resposta causará falha
    metric = HallucinationMetric(threshold=0.3, verbose_mode=True, model=JUDGE_MODEL)
    assert_test(test_case, [metric])
