# 🛠️ Guia de Execução de Testes e Consolidação de Relatórios

> **Projeto:** IA Fluentes (Escola Online & Assistente RAG)  
> **Última atualização:** 23/07/2026  

Este guia fornece os comandos rápidos para execução de cada suíte de testes e consolidação do relatório executivo HTML.

---

## 1. 🚀 Execução dos Testes

### A. Regressão Rápida da API (Custo Zero - ~15s a 1min)
```bash
cd nextjs-teste-fluentes

# 1. Smoke Test Rápido (11 casos essenciais das 7 categorias lógicas em ~15s)
python3 tests/suite_test_chat.py

# 2. Regressão Completa (11 casos + 50 perguntas do golden_dataset.json em ~1min)
python3 tests/suite_test_chat.py --full
```
*Gera:* `relatorios/suite_test_chat_results.json`

### B. Testes Pytest por Módulo (Com Venv de QA)
```bash
# 1. Testar apenas Robustez Técnica (Anti-XSS e HTTP 400 em 0.23s)
./venv_qa/bin/pytest -n 0 tests/security/test_input_robustness.py

# 2. Testar apenas Segurança (Injeção de Prompt e Vazamento)
./venv_qa/bin/pytest -n 0 tests/security/

# 3. Testar apenas Qualidade Semântica RAG (DeepEval)
./venv_qa/bin/pytest -n 0 tests/ai_quality/

# 4. Executar TODOS os testes Pytest
./venv_qa/bin/pytest -n 0 tests/
```
*Gera:* `relatorios/pytest_all_results.json` e `relatorios/deepeval_results.json`

### C. Teste de Carga e Estresse (Locust)
```bash
./venv_qa/bin/locust -f qa/locustfile.py --host=http://localhost:3000 --users=5 --spawn-rate=1 --run-time=2m --headless
```
*Gera:* `relatorios/locust_stats.csv` e `relatorios/locust_report.html`

### D. Red Teaming em Massa (Garak)
```bash
./venv_qa/bin/python3 qa/garak_generator.py
```
*Gera:* `relatorios/garak.report.jsonl`

### E. Varredura de Riscos (Giskard)
```bash
./venv_qa/bin/python3 qa/giskard_scan.py
```
*Gera:* `relatorios/giskard_scan.html`

---

## 2. 📊 Consolidação do Dashboard HTML Executivo

Para gerar ou atualizar o relatório unificado com gráficos e indicadores de qualidade/segurança:

```bash
cd nextjs-teste-fluentes
python3 qa/relatorio_consolidado.py
```

- **Dashboard HTML Consolidado:** [`relatorios/qa_llm_report.html`](abra no navegador).
