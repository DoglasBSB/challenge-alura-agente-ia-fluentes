# 🌐 IA Fluentes — Landing Page com Assistente de IA & RAG 🤖

![Next.js](https://img.shields.io/badge/Next.js-15-black)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

![IA Fluentes Mockup](nextjs-teste-fluentes/docs/images/img-readme.png)

**IA Fluentes** é uma Landing Page integrada a um assistente conversacional autônomo baseado em LLM local (Ollama) utilizando a técnica de **RAG (Retrieval-Augmented Generation)** para responder exclusivamente sobre os cursos ativos cadastrados no Sanity CMS.

Além do desenvolvimento da aplicação, o projeto serve como laboratório de **Engenharia de Confiabilidade para LLMs (LLM Reliability Engineering)**, explorando testes funcionais, semânticos, segurança (Red Teaming) e desempenho sob carga.


## 1. Descrição e Propósito

Diferente do software tradicional (onde os resultados são estritamente determinísticos), a IA apresenta respostas probabilísticas. Para garantir que o assistente responda apenas sobre os cursos ativos cadastrados no **Sanity CMS** e se defenda contra manipulações de prompt, o projeto implementa um pipeline completo de validação de RAG e Guardrails locais.

---

## 2. Funcionalidades

*   **Landing Page Responsiva:** Interface moderna exibindo cursos obtidos dinamicamente via CMS.
*   **Chat Widget de IA:** Assistente virtual integrado no canto inferior direito para atendimento aos alunos.
*   **RAG Local (Sanity CMS):** A IA só responde utilizando o contexto de cursos ativos recuperados da API.
*   **Persona & Guardrail de Escopo:** Recusa amigável de perguntas fora de domínio (receitas, política, etc.).
*   **Filtros de Output (Data Leakage):** Bloqueio de respostas que tentem revelar o System Prompt ou chaves de API.
*   **Suíte de QA Automatizada:** Validações de latência, integridade lógica, relevância semântica e Red Teaming.

---

## 3. Arquitetura do Sistema

```text
      Usuário
         │
         ▼
Landing Page (Next.js)
         │
         ▼
     API Routes
         │
     ┌───┴──────────────┐
     ▼                  ▼
Sanity CMS           Ollama (Llama 3.2 3B)
     │                  │
     └─────── RAG ──────┘
             │
             ▼
      Resposta Final
```

---

## 4. Tecnologias Utilizadas

*   **Portal Web:** Next.js (React + TypeScript + Tailwind CSS)
*   **CMS & Database:** Sanity CMS (Vigência dinâmica de cursos)
*   **LLM Local:** Llama 3.2 (3B) rodando via Ollama
*   **Testes de IA:** Pytest + DeepEval (Gemini Pro como LLM Juiz)
*   **Auditorias:** Garak (Red Teaming), Giskard (Riscos) e Locust (Carga/Latência)

---

## 5. Pré-requisitos e Instalação

### Pré-requisitos
*   [Node.js](https://nodejs.org/) (v18+)
*   [Python](https://www.python.org/) (v3.10+)
*   [Ollama](https://ollama.com/) instalado com o modelo `llama3.2` baixado (`ollama pull llama3.2`)

### Instalação Passo a Passo
1.  **Clone o projeto:**
    ```bash
    git clone https://github.com/seu-usuario/IA-Fluentes.git
    cd IA-Fluentes
    ```
2.  **Configurar o Portal Web (Next.js):**
    ```bash
    cd nextjs-teste-fluentes
    npm install
    cp .env.example .env
    # Insira sua GOOGLE_API_KEY no .env gerado
    ```
3.  **Configurar o CMS (Sanity Studio):**
    ```bash
    cd ../studio-teste-fluentes
    npm install
    ```

---

## 6. Como Executar a Aplicação

1.  **Inicie o Ollama:**
    ```bash
    ollama run llama3.2
    ```
2.  **Inicie o Next.js** (na pasta `nextjs-teste-fluentes/`):
    ```bash
    npm run dev
    # A Landing Page abrirá em http://localhost:3000
    ```
3.  **Inicie o Sanity Studio** (na pasta `studio-teste-fluentes/`):
    ```bash
    npm run dev
    # O painel administrativo abrirá em http://localhost:3333
    ```

---

## 7. Como Rodar os Testes

O guia de comandos e parâmetros detalhados está disponível no [Plano de Testes](nextjs-teste-fluentes/docs/plano_de_testes.md).

### A. Testes Rápidos e Determinísticos (Custo Zero de API)
Ideais para execuções rotineiras locais ou em CI/CD rápido:
```bash
cd nextjs-teste-fluentes
# Testes locais de regressão e persona
./venv_qa/bin/python3 docs/suite_test_chat.py
# Testes de robustez técnica a SQL/XSS/Null bytes
./venv_qa/bin/pytest -n 0 tests/security/test_input_robustness.py
```

### B. Testes Qualitativos Semânticos (DeepEval + Gemini Juiz)
Avaliam a cognição e lógica semântica da IA (consome tokens):
```bash
./venv_qa/bin/pytest -n 0 tests/
```

### C. Auditorias e Red Teaming (Locust, Garak, Giskard)
*   **Carga (Locust):** `./venv_qa/bin/locust -f qa/locustfile.py --host=http://localhost:3000 --users=5 --spawn-rate=1 --run-time=2m --headless --html relatorios/locust_report.html`
*   **Red Teaming (Garak):** `./venv_qa/bin/garak --model_type rest.RestGenerator --model_name http://localhost:3000/api/chat --probes promptinject --report_prefix relatorios/garak`
*   **Riscos (Giskard):** `./venv_qa/bin/python3 qa/run_giskard.py`

---

## 8. Estrutura de Diretórios

```text
IA-Fluentes/
├── nextjs-teste-fluentes/      # Aplicação Web (Next.js)
│   ├── src/                    # Componentes UI e rotas de API
│   ├── tests/                  # Suíte de testes de IA (pytest/DeepEval)
│   ├── qa/                     # Configurações de Locust, Giskard e Garak
│   └── docs/                   # Plano de testes e imagens de mockup
└── studio-teste-fluentes/      # Painel Administrativo CMS (Sanity Studio)
```

---

## 9. Arquitetura de QA (Reliability Engineering)

A suíte de testes do portal adota os seguintes pilares de validação para mitigar as falhas típicas de LLMs:

*   **Pilar 1: Robustez Técnica:** Validação de segurança convencional (HTTP 400 em injeções de script/HTML, estabilidade contra falhas 500).
*   **Pilar 2: Qualidade Semântica:** Auditoria qualitativa de respostas baseada nas métricas de **Fidelidade** (alucinação), **Relevância** (foco da resposta), **Consistência** e **Histórico Multi-turn**.
*   **Pilar 3: Auditoria de Segurança:** Red Teaming em massa (530 probes de injeção de prompt e jailbreaks) e escaneamento ativo de bias/toxicidade regulatória.

### 📐 Distribuição e Consumo de Recursos
| Recurso | Tipo | Ferramentas Associadas | Objetivo |
| :--- | :--- | :--- | :--- |
| **Ollama (Llama 3.2 Local)** | Local (Custo Zero) | Pytest, Locust, Garak, Giskard, `suite_test_chat.py` | Geração de respostas e simulações técnicas. |
| **Gemini (Google AI Studio)** | Nuvem (Consumo de Tokens) | DeepEval (testes qualitativos) | LLM Juiz avaliando métricas cognitivas e jailbreaks. |

---

## 10. Licença

Este projeto está sob a licença [MIT](LICENSE). O código pode ser livremente utilizado, modificado e distribuído para fins educacionais e de estudo.
