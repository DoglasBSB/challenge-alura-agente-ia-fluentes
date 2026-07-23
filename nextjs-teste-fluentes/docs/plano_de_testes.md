# Plano de Testes — IA Fluentes

> **Versão:** 1.0  
> **Última atualização:** 23/07/2026  
> **Responsável:** Francisco Dôglas (QA Engineer)  
> **Status:** Ativo  

Este documento descreve a estratégia, o escopo, os procedimentos de execução com gestão de custos e o fluxo de consolidação de relatórios para validar a qualidade, segurança e desempenho do assistente conversacional da **IA Fluentes (Plataforma Educativa / Escola Online de Idiomas)**.

---

## 1. Objetivo

Garantir que o assistente da **IA Fluentes** responda com precisão aos 10 cursos de idiomas disponíveis e diretrizes oficiais em PDF (`data/*.pdf`), bloqueie injeções de prompt e jailbreaks (Segurança), evite tópicos fora do domínio (Escopo/Guardrails) e mantenha alta disponibilidade e baixa latência sob acessos simultâneos.

---

## 2. Escopo de Validação

Os testes cobrem:
* **Integração de Dados RAG:** Leitura e consumo dos 5 documentos PDF oficiais salvos em `data/` (`Regulamento_do_Estudante.pdf`, `Politica_de_Reembolso_de_Matriculas.pdf`, `FAQ_Cursos_e_Certificados.pdf`, `Guia_de_Uso_da_Plataforma.pdf`, `Programa_de_Bolsas_e_Afiliados.pdf`).
* **Pipeline RAG & Fidelidade Semântica:** Fidelidade ao contexto (`Faithfulness`), relevância da resposta (`AnswerRelevancy`) e ausência de alucinações (`HallucinationMetric`).
* **Persona & Escopo (Guardrails):** Recusa amigável de temas fora do domínio da escola (receitas, esportes, política, etc.).
* **Segurança (Red Teaming & Anti-Jailbreak):** Bloqueio de injeções de prompt, engenharia social e vazamento de instruções internas (`Data Leakage`).
* **Robustez Técnica:** Resiliência contra payloads malformados, scripts XSS e mensagens vazias.
* **Desempenho & Carga:** Throughput e latência (p95/p99) sob acessos simultâneos.

---

## 3. Gestão de Custos na Execução dos Testes (Estratégia R$ 0,00)

Toda a suíte de testes foi projetada para permitir **execução 100% GRATUITA (Custo Zero / R$ 0,00)**:

| Categoria do Teste | Arquivos / Ferramentas | Consumo de Tokens | Como Rodar com Custo Zero (R$ 0,00) |
| :--- | :--- | :--- | :--- |
| **Regressão RAG & Escopo** | `docs/suite_test_chat.py` | Isento / Free Tier | Usa a API local ou a `GOOGLE_API_KEY` no **Free Tier da Google AI Studio** (15 requisições/min grátis). |
| **Robustez Técnica (XSS/400)** | `test_input_robustness.py` | Zero (0 tokens) | Validação pura de status HTTP e sanitização de dados no endpoint. |
| **Carga & Desempenho** | `qa/locustfile.py` | Zero (0 tokens) | Teste de estresse de servidor local via Locust. |
| **Qualitativos Semânticos** | `tests/ai_quality/*` | Consome Tokens | Utilize a chave grátis do **Google AI Studio** ou o **Ollama local** (`llama3.2`). |
| **Red Teaming & Riscos** | `qa/garak_generator.py`<br>`qa/giskard_scan.py` | Consome Tokens | Execute utilizando o **Ollama local** (`ollama run llama3.2`) sem gastar APIs pagas. |

---

## 4. Arquitetura de Testes e Rastreabilidade

```text
       Ferramentas de Teste (Pytest / DeepEval / Locust / Garak / Giskard)
                                       │
                                       ▼
                              API Chat (/api/chat)
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
Documentos PDF (data/*.pdf)                               Google Gemini / Ollama
            │                                                     │
            └────────────────────── RAG ──────────────────────────┘
                                    │
                                    ▼
                         Resposta da Aplicação
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
Resultados em relatorios/                             relatorio_consolidado.py
(JSON / JSONL / HTML)                                       │
                                                            ▼
                                                Dashboard HTML Consolidado
                                                (relatorios/qa_llm_report.html)
```

---

## 5. Taxonomia e Correspondência dos Arquivos de Teste

| Categoria | Sigla | Objetivo Técnico | Arquivo Físico | Executor |
| :--- | :--- | :--- | :--- | :--- |
| **Pipeline RAG** | `RAG` | Integração RAG de ponta a ponta | `tests/ai_quality/test_rag_pipeline.py` | Pytest + DeepEval |
| **Fidelidade** | `FAI` | Fidelidade factual com os PDFs | `tests/ai_quality/test_faithfulness.py` | Pytest + DeepEval |
| **Sem Alucinação** | `HAL` | Ausência de alucinações cognitivas | `tests/ai_quality/test_hallucination.py` | Pytest + DeepEval |
| **Relevância** | `REL` | Pertinência da resposta à dúvida | `tests/ai_quality/test_relevancy.py` | Pytest + DeepEval |
| **Guardrail Escopo** | `GRD` | Recusa amigável de temas alheios | `tests/ai_quality/test_scope_guardrail.py` | Pytest + DeepEval |
| **Histórico / Multi-turn**| `MEM` | Manutenção de contexto em chat | `tests/ai_quality/test_multiturn.py` | Pytest + DeepEval |
| **Consistência** | `CON` | Coerência de respostas repetidas | `tests/ai_quality/test_consistency.py` | Pytest + DeepEval |
| **Injeção de Prompt** | `INJ` | Bloqueio de override de persona | `tests/security/test_prompt_injection.py` | Pytest + DeepEval |
| **Vazamento de Prompt** | `LEA` | Proteção contra data leakage | `tests/security/test_data_leakage.py` | Pytest + DeepEval |
| **Robustez de Input** | `ROB` | Anti-XSS e tratamento de erros 400 | `tests/security/test_input_robustness.py` | Pytest |
| **Carga & Latência** | `PER` | Medição de throughput/p95 | `qa/locustfile.py` | Locust |
| **Red Teaming em Massa** | `RED` | Auditoria de vulnerabilidades | `qa/garak_generator.py` | Garak |
| **Varredura de Riscos** | `RSK` | Mapeamento de riscos do modelo | `qa/giskard_scan.py` | Giskard |

---

## 6. Procedimentos de Execução de Todos os Testes

### A. Teste de Regressão Rápida (Custo Zero - 100% Grátis)
```bash
cd nextjs-teste-fluentes
python3 docs/suite_test_chat.py
```

### B. Execução de Testes Pytest por Módulo Específico
```bash
# 1. Testar apenas Robustez Técnica (Anti-XSS e HTTP 400)
./venv_qa/bin/pytest -n 0 tests/security/test_input_robustness.py

# 2. Testar apenas Segurança (Injeção de Prompt e Vazamento)
./venv_qa/bin/pytest -n 0 tests/security/

# 3. Testar apenas Qualidade Semântica RAG (DeepEval)
./venv_qa/bin/pytest -n 0 tests/ai_quality/

# 4. Executar TODOS os testes Pytest
./venv_qa/bin/pytest -n 0 tests/
```

### C. Testes de Carga e Desempenho (Locust)
```bash
./venv_qa/bin/locust -f qa/locustfile.py --host=http://localhost:3000 --users=5 --spawn-rate=1 --run-time=2m --headless
```

### D. Red Teaming em Massa (Garak)
```bash
./venv_qa/bin/python3 qa/garak_generator.py
```

### E. Varredura de Riscos (Giskard)
```bash
./venv_qa/bin/python3 qa/giskard_scan.py
```

---

## 7. Consolidação dos Relatórios de QA em Dashboard Único

Após a execução das ferramentas de teste, os relatórios são armazenados em `nextjs-teste-fluentes/relatorios/`:
- `pytest_all_results.json` & `deepeval_results.json` (Resultados das métricas Pytest/DeepEval)
- `garak-nextjs.report.jsonl` (Relatório do Garak Red Teaming)
- `giskard_scan.html` (Relatório de varredura do Giskard)
- `locust_report.html` (Relatório de desempenho do Locust)

### Como Gerar o Dashboard Executivo Consolidado:
Execute o script de consolidação em Python:

```bash
cd nextjs-teste-fluentes
python3 qa/relatorio_consolidado.py
```

Este comando processará todos os arquivos acima e gerará um **Dashboard HTML Consolidado** em:
`nextjs-teste-fluentes/relatorios/qa_llm_report.html`

O relatório apresentará um score geral de qualidade/segurança (0 a 100), nível de risco do modelo, gráficos de rosca e alertas automatizados sobre os achados de teste.

---

## 8. Critérios de Aceite para Aprovação

1. **Regressão RAG:** 100% de aprovação na `suite_test_chat.py`.
2. **Fidelidade RAG (Faithfulness):** Score mínimo de `0.8` no DeepEval.
3. **Guardrail de Escopo:** 100% de recusa amigável em tentativas de desvio de tema (receitas, esportes, política).
4. **Resistência a Jailbreaks:** 0 falhas críticas nas auditorias do Garak e Pytest Security.
5. **Latência p95:** Tempo de resposta inferior a 5 segundos sob carga concorrente (Locust).
