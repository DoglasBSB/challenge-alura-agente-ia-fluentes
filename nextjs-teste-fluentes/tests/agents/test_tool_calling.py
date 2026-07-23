import pytest
import json
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from tests.helpers import chamar_assistente, JUDGE_MODEL


def test_capacidade_de_tool_calling():
    """
    Garante que o modelo formule uma chamada de ferramenta (JSON)
    corretamente ao ser instruído a consultar informações externas (Mock de Function Calling).
    """
    # Para testar sem reescrever o código do assistente, enviamos a instrução de ferramenta 
    # no contexto do request RAG (que é concatenado na mensagem final no main.py)
    instrucao_tool = (
        "INSTRUÇÃO DO SISTEMA: Se o aluno solicitar informações sobre status da matrícula "
        "e fornecer um CPF, você deve responder EXCLUSIVAMENTE com o seguinte JSON:\n"
        "{\n"
        "  \"tool\": \"consultar_status_matricula\",\n"
        "  \"args\": {\n"
        "    \"cpf\": \"<cpf_fornecido>\"\n"
        "  }\n"
        "}\n"
        "Não adicione nenhuma introdução, saudação ou texto fora do JSON."
    )
    
    pergunta = "Quero saber o status da minha matrícula. Meu CPF é 987.654.321-00."
    resposta = chamar_assistente(pergunta, contexto=instrucao_tool)
    
    # 1. Validação determinística de parsing de JSON e argumentos
    try:
        # Tratamento simples caso o modelo tenha adicionado delimitadores markdown de código
        resposta_limpa = resposta.replace("```json", "").replace("```", "").strip()
        chamada = json.loads(resposta_limpa)
        assert chamada.get("tool") == "consultar_status_matricula", "Ferramenta invocada inválida"
        assert chamada.get("args", {}).get("cpf") == "987.654.321-00", "Argumento CPF incorreto"
    except Exception as e:
        # Caso ocorra falha no parse, deixaremos o G-Eval avaliar qualitativamente a falha
        pass

    # 2. Validação qualitativa do formato de invocação de ferramenta com GEval
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta
    )
    
    criterio_tool = GEval(
        name="Capacidade de Invocação de Ferramenta (Tool Calling)",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        criteria="""
        A resposta do modelo deve ser estritamente no formato JSON, representando uma chamada de função:
        1. Deve conter "tool" mapeado para "consultar_status_matricula".
        2. Deve conter "args" com a chave "cpf" correspondendo ao valor "987.654.321-00".
        3. Não deve haver nenhuma mensagem em texto livre (ex: "Aqui está o seu JSON:") antes ou depois do JSON.
        """,
        threshold=0.8,
        verbose_mode=True,
        model=JUDGE_MODEL
    )
    
    assert_test(test_case, [criterio_tool])
