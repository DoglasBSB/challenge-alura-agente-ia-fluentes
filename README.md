# 🌐 IA Fluentes — Escola Online de Idiomas & RAG em PDF (Alura Agent Challenge) 🤖

![Next.js](https://img.shields.io/badge/Next.js-15-black)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

![IA Fluentes Mockup](nextjs-teste-fluentes/docs/images/img-readme.png)

---

## 1. 📝 Descrição e Propósito

O **IA Fluentes** é um assistente virtual inteligente e uma plataforma web educativa, desenvolvido para o **Alura Agent Challenge** (Opção 5: Plataforma Educativa / Escola Online).

O propósito do sistema é atuar como uma base de conhecimento conversacional centralizada, operando 24/7. Ele foi projetado para responder com **fidelidade factual estrita** às dúvidas de alunos e colaboradores sobre os 10 cursos de idiomas disponíveis, regulamentos acadêmicos, políticas de reembolso, emissão de certificados e programas de bolsas da escola.

A solução utiliza a arquitetura **RAG (Retrieval-Augmented Generation)** alimentada pela extração em tempo real de documentos PDF oficiais (diretório `data/`). A aplicação opera com suporte híbrido: utiliza o **Google Gemini 2.5 Flash** (nuvem) como motor principal e o **Ollama Llama 3.2** como fallback local de custo zero.

Mais do que uma simples aplicação web, o repositório engloba um laboratório avançado de **Engenharia de Confiabilidade para LLMs (LLM Reliability Engineering)**.

---

## 2. ✨ Funcionalidades

- 💬 **Assistente Virtual RAG 24h:** Respostas precisas e ancoradas exclusivamente nos 5 PDFs oficiais da escola.
- 🎓 **Catálogo de 10 Cursos de Idiomas:** Inglês Iniciante, Inglês Intermediário, English Kids, Espanhol para Viagens, Francês Básico, Italiano para Conversação, Alemão Intensivo, Japonês para Iniciantes, Coreano para Fãs de K-pop e Preparação para TOEFL.
- 💾 **Persistência Multiturn em `localStorage`:** O widget do chat preserva o histórico da conversa entre recarregamentos de página (F5) e oferece um botão dedicado para limpeza de contexto (🗑️).
- 🚦 **Tratamento de Recusas em 3 Categorias:**
  - *Categoria 1 (Fora do Domínio):* Recusa amigável com chamada para ação (CTA: *"Você gostaria de conhecer nossos cursos de idiomas disponíveis?"*).
  - *Categoria 2 (Entidade/Curso Inexistente):* Esclarecimento de que o curso não é ofertado (ex: C++ presencial), seguido de CTA.
  - *Categoria 3 (Informação Não Cadastrada):* Transparência sobre a ausência de um detalhe específico na base de dados oficial.
- 🔒 **Sigilo Técnico e Naturalidade de UI:** A IA responde de forma humana e cortês, bloqueando a exposição de termos internos de engenharia (`PDF`, `RAG`, `base vetorial`, `embeddings` ou `system prompt`).
- 🛡️ **Guardrails de Segurança & Anti-Jailbreak:** Defesa rigorosa contra injeção de prompt, override de persona (ex: comandos para "agir como pirata") e sanitização contra scripts maliciosos (Anti-XSS).

---

## 3. 🏗️ Arquitetura do Sistema

```text
               Usuário / Aluno
                      │
                      ▼
        Landing Page Web (Next.js 15)
                      │
                      ▼
         API Route (/api/chat)
                      │
         ┌────────────┴────────────────────────┐
         ▼                                     ▼
Base RAG (Documentos PDF em data/)    Google Gemini / Ollama Local
         │                                     │
         └───────────── Ingestão RAG ──────────┘
                        │
                        ▼
             Resposta Final Sanitizada
```

---

## 4. 🛠️ Tecnologias Utilizadas

- **Frontend & Aplicação Web:** Next.js 15 (React 19 + TypeScript + Tailwind CSS)
- **Processamento RAG & PDFs:** Ingestor em tempo de execução via `pdf-parse` (`data/*.pdf`)
- **Modelos de Linguagem (LLM):** Google Gemini 2.5 Flash (via API) com Fallback para Ollama (Llama 3.2 3B local via CPU)
- **Framework de Testes & Qualidade de IA:** Pytest, DeepEval (Gemini Pro como LLM Juiz)
- **Segurança & Reliability Engineering:** Garak (Red Teaming), Giskard (Varredura de Riscos) e Locust (Carga/Latência Concorrente)

---

## 5. ⚙️ Pré-requisitos e Instalação

### Pré-requisitos
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (v3.10+) — *Necessário para a execução da suíte de QA e auditorias*

### Instalação Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/franciscodoglas/IA-Fluentes.git
   cd IA-Fluentes/nextjs-teste-fluentes
   ```

2. **Instale as dependências da aplicação Web:**
   ```bash
   npm install
   ```

3. **Configure as Variáveis de Ambiente:**
   ```bash
   cp .env.example .env
   ```
   *(Adicione sua `GOOGLE_API_KEY` no arquivo `.env` para habilitar as respostas via Gemini API, ou utilize a configuração do Ollama local)*.

4. **Configure o Ambiente Virtual de QA (Python):**
   ```bash
   python3 -m venv venv_qa
   source venv_qa/bin/activate  # No Windows: venv_qa\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 6. 🚀 Como Executar a Aplicação

### Execução Local (Desenvolvimento)
```bash
cd nextjs-teste-fluentes
npm run dev
```
Acesse a aplicação em seu navegador: `http://localhost:3000`.

### Implantação na Nuvem (Oracle Cloud Infrastructure - OCI)
O projeto foi validado para execução na **OCI Compute (VM Always Free Tier)**:
1. Crie uma instância Ubuntu Server no painel da OCI.
2. Clone o repositório, instale as dependências e rode o build de produção: `npm run build`.
3. Execute o processo em background via PM2: `pm2 start npm --name "ia-fluentes" -- start`.
4. Libere a porta `3000` nas regras de Ingress da OCI e no firewall do Linux (`ufw`).

---

## 7. 🧪 Como Rodar os Testes de QA

O detalhamento completo da arquitetura de testes está disponível no [Plano de Testes](nextjs-teste-fluentes/docs/plano_de_testes.md) e no [Guia de Execução](nextjs-teste-fluentes/docs/guia_execucao_e_relatorios.md).

### A. Testes Rápidos e Determinísticos (Custo Zero)
```bash
cd nextjs-teste-fluentes

# 1. Smoke Test (11 casos essenciais das 7 categorias lógicas em ~15s)
python3 tests/suite_test_chat.py

# 2. Regressão Completa (11 casos + 50 perguntas do golden_dataset.json em ~1min)
python3 tests/suite_test_chat.py --full
```

### B. Testes Qualitativos Semânticos (DeepEval + Gemini Juiz)
```bash
# Validação de Fidelidade Factual (Faithfulness), Anti-Alucinação e Relevância
./venv_qa/bin/pytest -n 0 tests/
```

### C. Auditorias e Red Teaming (Locust, Garak, Giskard)
```bash
# 1. Teste de Carga e Latência Concorrente
./venv_qa/bin/locust -f qa/locustfile.py --host=http://localhost:3000 --users=5 --spawn-rate=1 --run-time=1m --headless

# 2. Red Teaming em Massa contra Jailbreaks
./venv_qa/bin/python3 qa/garak_generator.py

# 3. Varredura de Riscos e Viés de Modelo
./venv_qa/bin/python3 qa/giskard_scan.py

# 4. Consolidação do Dashboard HTML Executivo
python3 qa/relatorio_consolidado.py
```
*Visualização do Dashboard:* Abra o arquivo gerado em `relatorios/qa_llm_report.html` no seu navegador.

---

## 8. 📂 Estrutura de Diretórios

```text
IA-Fluentes/
├── README.md                          # Documentação principal do projeto
├── LICENSE                            # Licença MIT
└── nextjs-teste-fluentes/
    ├── data/                          # 5 PDFs oficiais da base RAG
    │   ├── Regulamento_do_Estudante.pdf
    │   ├── Politica_de_Reembolso_de_Matriculas.pdf
    │   ├── FAQ_Cursos_e_Certificados.pdf
    │   ├── Guia_de_Uso_da_Plataforma.pdf
    │   └── Programa_de_Bolsas_e_Afiliados.pdf
    ├── datasets/                      # Golden Dataset de 50 Q&As benchmark
    │   └── golden_dataset.json
    ├── docs/                          # Documentação técnica ISTQB e guias
    │   ├── plano_de_testes.md
    │   └── guia_execucao_e_relatorios.md
    ├── qa/                            # Scripts de auditoria e relatórios
    │   ├── relatorio_consolidado.py
    │   ├── locustfile.py
    │   ├── garak_generator.py
    │   └── giskard_scan.py
    ├── relatorios/                    # Dashboards HTML e relatórios JSON
    │   └── qa_llm_report.html
    ├── src/                           # Código-fonte da aplicação Next.js
    │   └── app/
    │       ├── api/chat/route.ts      # Endpoint RAG e System Prompt
    │       └── components/ChatWidget.tsx
    ├── tests/                         # Suítes de testes automatizados
    │   ├── suite_test_chat.py
    │   ├── security/
    │   └── ai_quality/
    ├── package.json
    └── requirements.txt
```

---

## 9. 🏛️ Arquitetura de QA (Reliability Engineering)

A suíte de garantia de qualidade foi estruturada em **7 Categorias Lógicas de QA**, inspiradas nos padrões do ISTQB para IAs Generativas:

1. **`GRD` (Escopo & Guardrails):** Recusa de temas alheios ao domínio com CTA ativa.
2. **`QUA` (Fidelidade Factual & RAG):** Ancoragem rigorosa aos 5 PDFs e aos 10 cursos.
3. **`SEC` (Segurança da Informação):** Proteção contra Injeção de Prompt, Data Leakage e XSS.
4. **`MEM` (Memória & Conversação):** Contexto multiturn e persistência no cliente.
5. **`INP` (Robustez de Entrada & Tom):** Resiliência a entradas vazias (HTTP 400), emojis e provocações.
6. **`UI` (Formatação & Sigilo Técnico):** Respostas limpas em Markdown sem expor jargões de backend.
7. **`PERF` (Desempenho & Latência):** Medição de throughput e latência (p95) via Locust.

### Distribuição e Consumo de Recursos (Estratégia Custo R$ 0,00)
- **Free Tier do Google AI Studio:** 15 requisições por minuto sem custo financeiro para testes semânticos em nuvem.
- **Ollama Local (`llama3.2`):** Processamento em ambiente isolado via CPU para rodar as suítes pesadas de estresse e red teaming.
- **Ponderação Padrão do Score Consolidado (`qa_llm_report.html`):**

$$\text{Score} = (\text{Pytest/DeepEval} \times 0.40) + (\text{Garak} \times 0.35) + (\text{Giskard} \times 0.15) + (\text{Locust} \times 0.10)$$

---

## 10. 📄 Licença e Autores

Este projeto está sob a licença [MIT](LICENSE). O código pode ser livremente utilizado e distribuído para fins de estudo, avaliação e contribuição com a comunidade de Quality Engineering.

### 👤 Autor & Contato

- **Desenvolvido por:** Dôglas (QA & Project Manager)
- **LinkedIn:** [linkedin.com/in/franciscodoglas](https://www.linkedin.com/in/franciscodoglas/)
- **GitHub:** [github.com/franciscodoglas](https://github.com/franciscodoglas)
- **E-mail:** franciscodoglas@gmail.com
