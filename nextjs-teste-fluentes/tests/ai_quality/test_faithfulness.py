import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from tests.helpers import chamar_assistente, carregar_golden_dataset, JUDGE_MODEL


# Carrega o dataset completo e filtra casos específicos para validação de Faithfulness
# Exemplos: Preço do básico (índice 2), cancelamento (índice 14), garantia/reembolso (índice 16)
dataset = carregar_golden_dataset()
casos_faithfulness = [
    dataset[2],   # Preço do curso básico
    dataset[14],  # Política de cancelamento
    dataset[16]   # Reembolso de 7 dias
]

@pytest.mark.parametrize("caso_data", casos_faithfulness, ids=[
    "preco_basico",
    "politica_cancelamento",
    "garantia_reembolso"
])
def test_faithfulness_do_assistente(caso_data):
    """Garante que o assistente responda de forma estritamente fiel ao contexto RAG fornecido"""
    pergunta = caso_data["input"]
    contexto = caso_data["retrieval_context"]
    
    resposta = chamar_assistente(pergunta, contexto=contexto)
    
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta,
        retrieval_context=[contexto]
    )
    
    # A resposta deve ter alto nível de fidelidade com o contexto
    metric = FaithfulnessMetric(threshold=0.8, verbose_mode=True, model=JUDGE_MODEL)
    assert_test(test_case, [metric])
