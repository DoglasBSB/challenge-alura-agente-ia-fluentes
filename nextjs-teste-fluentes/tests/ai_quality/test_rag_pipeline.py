import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from tests.helpers import chamar_assistente, carregar_golden_dataset, JUDGE_MODEL


# Carrega o dataset completo e filtra casos que necessitam de contexto RAG dinâmico
# Exemplos: Fluentes Kids (índice 7), Esqueci minha senha (índice 10)
dataset = carregar_golden_dataset()
casos_rag = [
    dataset[7],   # Fluentes Kids
    dataset[10]   # Recuperação de senha no portal
]

@pytest.mark.parametrize("caso_data", casos_rag, ids=[
    "fluentes_kids",
    "recuperar_senha"
])
def test_rag_pipeline_corretude(caso_data):
    """Garante que a integração RAG funcione de ponta a ponta (resposta é relevante e fiel ao contexto de suporte e regras)"""
    pergunta = caso_data["input"]
    contexto = caso_data["retrieval_context"]
    
    # Chama o assistente injetando o contexto de recuperação
    resposta = chamar_assistente(pergunta, contexto=contexto)
    
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta,
        retrieval_context=[contexto]
    )
    
    # Executa verificação cruzada de duas métricas essenciais para RAG
    metric_faithfulness = FaithfulnessMetric(threshold=0.8, verbose_mode=True, model=JUDGE_MODEL)
    metric_relevancy = AnswerRelevancyMetric(threshold=0.7, verbose_mode=True, model=JUDGE_MODEL)
    
    assert_test(test_case, [metric_faithfulness, metric_relevancy])
