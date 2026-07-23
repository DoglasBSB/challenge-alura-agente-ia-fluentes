import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from tests.helpers import chamar_assistente, carregar_golden_dataset, JUDGE_MODEL


# Carrega o dataset completo e filtra perguntas sobre tópicos padrão
# Exemplos: Cursos oferecidos (índice 0), como matricular (índice 1), horários noturnos (índice 4)
dataset = carregar_golden_dataset()
casos_relevancia = [
    dataset[0],   # Cursos oferecidos
    dataset[1],   # Processo de matrícula
    dataset[4]    # Horários noturnos
]

@pytest.mark.parametrize("caso_data", casos_relevancia, ids=[
    "cursos_oferecidos",
    "como_matricular",
    "horarios_noturnos"
])
def test_relevancia_da_resposta(caso_data):
    """Garante que a resposta gerada pelo assistente seja diretamente relevante para a pergunta do aluno"""
    pergunta = caso_data["input"]
    
    resposta = chamar_assistente(pergunta)
    
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta
    )
    
    # A resposta deve ter alto nível de relevância sem adicionar tangentes irrelevantes
    metric = AnswerRelevancyMetric(threshold=0.7, verbose_mode=True, model=JUDGE_MODEL)
    assert_test(test_case, [metric])
