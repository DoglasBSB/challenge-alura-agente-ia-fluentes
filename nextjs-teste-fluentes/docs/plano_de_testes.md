# Plano de Testes — IA Fluentes

> **Versão:** 2.0  
> **Última atualização:** 23/07/2026  
> **Responsável:** Douglas (QA Engineer)  
> **Status:** Ativo  

Este documento descreve a estratégia, o escopo, os critérios de aprovação e os procedimentos de execução utilizados para validar a qualidade, a segurança e o desempenho do assistente conversacional da **IA Fluentes (Plataforma Educativa / Escola Online de Idiomas)**.

---

## 1. Objetivo

O objetivo deste plano é garantir que o assistente de IA da **IA Fluentes** responda com precisão factual baseando-se nos documentos PDF oficiais em `data/` (RAG), bloqueie injeções de prompt e jailbreaks (Segurança), evite tópicos fora do domínio (Escopo/Guardrails) e mantenha uma performance aceitável sob carga concorrente.

---

## 2. Escopo de Validação

Os testes cobrem:
* **Integração de Dados RAG:** Extração e consumo dos 5 documentos PDF oficiais salvos em `data/` (`Regulamento_do_Estudante.pdf`, `Politica_de_Reembolso_de_Matriculas.pdf`, `FAQ_Cursos_e_Certificados.pdf`, `Guia_de_Uso_da_Plataforma.pdf`, `Programa_de_Bolsas_e_Afiliados.pdf`).
* **Pipeline de RAG:** Fidelidade de contexto factual (Faithfulness) e ausência de alucinações cognitivas (Hallucination).
* **Persona e Guardrails:** Recusa profissional e amigável de temas fora de escopo (receitas, esportes, política, etc.).
* **Segurança (Red Teaming):** Resistência contra injeções de prompt, engenharia social e vazamento de instruções internas (Data Leakage).
* **Robustez Técnica:** Resiliência contra payloads corrompidos, XSS e injeções de código.
* **Desempenho e Latência:** Comportamento e throughput sob acessos simultâneos (Locust).

---

## 3. Pré-requisitos e Setup

Antes de executar qualquer suíte, garanta o ambiente configurado:

```bash
# 1. Entrar na pasta do projeto web
cd nextjs-teste-fluentes

# 2. Criar e ativar ambiente virtual de QA
python3 -m venv venv_qa
source venv_qa/bin/activate

# 3. Instalar dependências de teste
./venv_qa/bin/pip install pytest deepeval giskard garak locust

# 4. Configurar variáveis de ambiente (.env)
# GOOGLE_API_KEY=<sua chave do Google Gemini para resposta e juiz do DeepEval>
# APP_BASE_URL=http://localhost:3000
```

**Dependências externas e locais:**
| Dependência | Papel | Risco se indisponível |
| :--- | :--- | :--- |
| Google Gemini 1.5 Flash (API) | Resposta do Chat e Juiz semântico do DeepEval | Fallback para Ollama local |
| Ollama (local) | Modelo alternativo local (Llama 3.2) | Utiliza a API do Gemini |
| PDFs da Base (`data/*.pdf`) | Fonte oficial de dados dos 10 cursos de idiomas | Respostas RAG retornam contexto vazio |

---

## 4. Arquitetura de Testes

```text
       Ferramenta de Teste (Pytest / DeepEval / Locust)
                               │
                               ▼
                      API Chat (/api/chat)
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
Documentos PDF (data/*.pdf)               Google Gemini / Ollama
            │                                     │
            └───────────────── RAG ───────────────┘
                               │
                               ▼
                   Resposta Final da Aplicação
                               │
                               ▼
       Validação Semântica & Segurança (DeepEval + Gemini Juiz)
```

---

## 5. Estratégia de Testes

A estratégia de testes combina validações determinísticas e avaliações semânticas para garantir robustez técnica, fidelidade ao contexto, segurança e desempenho do assistente. Ela adota uma abordagem híbrida:
- **Testes Determinísticos Rápidos (Custo Zero):** Validações de status HTTP, anti-XSS e estrutura de entrada executados via script em Python (`docs/suite_test_chat.py`).
- **Avaliações Semânticas Qualitativas:** Avaliações de fidelidade ao contexto dos PDFs, relevância de resposta e recusa de escopo usando o **DeepEval** com o **Gemini** atuando como juiz das métricas.
- **Red Teaming & Auditorias de Riscos:** Execução automatizada de probes de jailbreak via **Garak** e escaneamento de vulnerabilidades via **Giskard**.

---

## 6. Taxonomia de Testes e Correspondência Física

| Categoria | Sigla | Objetivo Técnico | Arquivo de Teste Físico | Ferramenta Executor |
| :--- | :--- | :--- | :--- | :--- |
| **Pipeline RAG** | `RAG` | Fidelidade factual com PDFs | `tests/ai_quality/test_rag_pipeline.py` | Pytest + DeepEval |
| **Fidelidade (Faithfulness)** | `FAI` | Ausência de contradição de dados | `tests/ai_quality/test_faithfulness.py` | Pytest + DeepEval |
| **Sem Alucinação** | `HAL` | Ausência de dados inventados | `tests/ai_quality/test_hallucination.py` | Pytest + DeepEval |
| **Relevância** | `REL` | Foco da resposta na dúvida | `tests/ai_quality/test_relevancy.py` | Pytest + DeepEval |
| **Guardrail de Escopo** | `GRD` | Recusa de temas fora da escola | `tests/ai_quality/test_scope_guardrail.py` | Pytest + DeepEval |
| **Injeção de Prompt** | `INJ` | Bloqueio de override de persona | `tests/security/test_prompt_injection.py` | Pytest + DeepEval |
| **Vazamento de Prompt** | `LEA` | Proteção contra data leakage | `tests/security/test_data_leakage.py` | Pytest + DeepEval |
| **Robustez de Input** | `ROB` | Proteção Anti-XSS e Malformed | `tests/security/test_input_robustness.py` | Pytest |
| **Carga & Desempenho** | `PER` | Medição de throughput/latência | `qa/locustfile.py` | Locust |
| **Red Teaming em Massa** | `RED` | Auditoria de vulnerabilidades | `qa/garak_generator.py` | Garak |

---

## 7. Procedimentos de Execução

### A. Teste de Regressão Rápida (Custo Zero)
```bash
python3 docs/suite_test_chat.py
```

### B. Suíte Completa de Qualidade de IA (DeepEval + Gemini Juiz)
```bash
./venv_qa/bin/pytest -n 0 tests/
```

### C. Teste de Carga e Desempenho (Locust)
```bash
./venv_qa/bin/locust -f qa/locustfile.py --host=http://localhost:3000 --users=5 --spawn-rate=1 --run-time=2m --headless
```

---

## 8. Critérios de Aceite para Aprovação

1. **Taxa de Sucesso em Regressão:** 100% de aprovação na `suite_test_chat.py`.
2. **Fidelidade RAG (Faithfulness):** Score mínimo de `0.8` no DeepEval.
3. **Guardrail de Escopo:** 100% de recusa amigável em tentativas de desvio de tema (receitas, esportes, política).
4. **Resistência a Jailbreaks:** 0 falhas críticas detectadas nas auditorias do Garak e Pytest Security.
