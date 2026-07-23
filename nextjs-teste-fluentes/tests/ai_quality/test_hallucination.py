import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from tests.helpers import chamar_assistente, carregar_golden_dataset, JUDGE_MODEL


# Carrega o dataset completo e filtra casos específicos para validação de alucinação no RAG (QUA)
# Exemplos: Cursos oferecidos (índice 0), matrícula (índice 1), material didático (índice 6)
dataset = carregar_golden_dataset()
casos_hallucination = [
    dataset[0],  # Cursos oferecidos
    dataset[1],  # Como se matricular
    dataset[6]   # Valor do material
]

@pytest.mark.parametrize("caso_data", casos_hallucination, ids=[
    "cursos_oferecidos",
    "processo_matricula",
    "valor_material"
])
def test_sem_alucinacao_factual_rag(caso_data):
    """Garante que o assistente responda de forma estritamente fiel aos fatos do RAG fornecidos, sem inventar dados (alucinação)"""
    pergunta = caso_data["input"]
    contexto = caso_data["retrieval_context"]
    
    resposta = chamar_assistente(pergunta, contexto=contexto)
    
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta,
        context=[contexto]
    )
    
    # HallucinationMetric compara o output com o contexto factual para verificar invenções
    metric = HallucinationMetric(threshold=0.8, verbose_mode=True, model=JUDGE_MODEL)
    assert_test(test_case, [metric])
