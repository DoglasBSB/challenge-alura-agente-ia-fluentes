export interface Curso {
  id: string;
  titulo: string;
  idioma: string;
  nivel: string;
  descricao: string;
  imagem: string;
  categoria: "tecnologia" | "ia" | "preparatorio";
}

export interface Depoimento {
  id: string;
  nome: string;
  avatar: string;
  curso: string;
  comentario: string;
  estrelas: number;
}

export interface FAQItem {
  id: string;
  pergunta: string;
  resposta: string;
}

export const CURSOS: Curso[] = [
  {
    id: "py-ia",
    titulo: "Python & Lógica para IA",
    idioma: "Tecnologia",
    nivel: "Iniciante A1-A2",
    descricao: "Dê seus primeiros passos na programação voltada para inteligência artificial. Domine lógica, estruturas de dados e manipulação de arquivos.",
    imagem: "from-blue-500 to-indigo-600",
    categoria: "tecnologia",
  },
  {
    id: "prompt-eng",
    titulo: "Engenharia de Prompt Avançada",
    idioma: "Inteligência Artificial",
    nivel: "Intermediário B1-B2",
    descricao: "Aprenda a estruturar comandos eficientes para LLMs como Gemini e ChatGPT. Técnicas de Few-Shot, Chain-of-Thought e controle de saída.",
    imagem: "from-indigo-500 to-purple-600",
    categoria: "ia",
  },
  {
    id: "rag-langchain",
    titulo: "Desenvolvimento de RAG com LangChain",
    idioma: "Inteligência Artificial",
    nivel: "Intermediário B2",
    descricao: "Conecte modelos de linguagem a documentos internos (PDF/CSV/Bancos de Dados). Construa assistentes virtuais precisos e livres de alucinações.",
    imagem: "from-emerald-500 to-teal-600",
    categoria: "ia",
  },
  {
    id: "agents-cloud",
    titulo: "Agentes de IA e Deploy na Nuvem (OCI)",
    idioma: "Engenharia de IA",
    nivel: "Avançado C1",
    descricao: "Desenvolva agentes autônomos com tomada de decisão e ferramentas. Implante sua aplicação na Oracle Cloud Infrastructure (OCI).",
    imagem: "from-orange-500 to-amber-600",
    categoria: "preparatorio",
  },
];

export const DEPOIMENTOS: Depoimento[] = [
  {
    id: "dep-1",
    nome: "Juliana Mendes",
    avatar: "JM",
    curso: "Desenvolvimento de RAG com LangChain",
    comentario: "O assistente virtual tirou minhas dúvidas sobre a política de reembolso e o programa de certificados. O curso me ajudou a ser promovida a desenvolvedora de IA!",
    estrelas: 5,
  },
  {
    id: "dep-2",
    nome: "Lucas Ferreira",
    avatar: "LF",
    curso: "Python & Lógica para IA",
    comentario: "Excelente didática! Consegui emitir meu certificado digital com QR Code e comprovar minhas horas de estudos na faculdade.",
    estrelas: 5,
  },
  {
    id: "dep-3",
    nome: "Mariana Souza",
    avatar: "MS",
    curso: "Engenharia de Prompt Avançada",
    comentario: "A plataforma é super amigável e o suporte a alunos respondeu minhas dúvidas em poucas horas pelo Discord.",
    estrelas: 5,
  },
];

export const FAQ_ITEMS: FAQItem[] = [
  {
    id: "faq-1",
    pergunta: "Como funciona a emissão dos certificados?",
    resposta: "Os certificados são emitidos digitalmente em PDF com QR Code de validação mediante a conclusão de no mínimo 80% das aulas e envio dos projetos.",
  },
  {
    id: "faq-2",
    pergunta: "Qual é a política de reembolso da matrícula?",
    resposta: "Oferecemos garantia incondicional de 7 dias corridos. Você pode solicitar 100% de reembolso diretamente no painel de usuário sem burocracia.",
  },
  {
    id: "faq-3",
    pergunta: "Como funciona o programa de bolsas de estudos?",
    resposta: "O programa 'IA para Todos' concede bolsas integrais e parciais para estudantes de baixa renda mediante processo seletivo semestral.",
  },
  {
    id: "faq-4",
    pergunta: "Onde posso tirar dúvidas sobre os códigos das aulas?",
    resposta: "Você pode usar nosso Fórum de Alunos abaixo de cada aula ou a comunidade do Discord no canal #suporte-ia. Além disso, nosso Assistente Virtual está disponível 24h.",
  },
];
