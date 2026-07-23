export interface Curso {
  id: string;
  titulo: string;
  idioma: string;
  nivel: string;
  descricao: string;
  imagem: string;
  categoria: "ingles" | "outros" | "preparatorio";
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
    id: "ing-ini",
    titulo: "Inglês para Iniciantes",
    idioma: "Inglês",
    nivel: "A1 - A2",
    descricao: "Dê seus primeiros passos no inglês. Aprenda vocabulário básico, estruturas essenciais e ganhe confiança para falar desde o primeiro dia.",
    imagem: "from-blue-500 to-indigo-600",
    categoria: "ingles",
  },
  {
    id: "ing-int",
    titulo: "Inglês Intermediário",
    idioma: "Inglês",
    nivel: "B1 - B2",
    descricao: "Aprimore sua fluência. Melhore sua compreensão auditiva, expanda seu vocabulário e aprenda a se expressar sobre temas complexos.",
    imagem: "from-indigo-500 to-purple-600",
    categoria: "ingles",
  },
  {
    id: "ing-kids",
    titulo: "English Kids",
    idioma: "Inglês",
    nivel: "Infantil",
    descricao: "O inglês de forma divertida e natural para crianças. Jogos, músicas e atividades interativas para estimular o aprendizado bilíngue precoce.",
    imagem: "from-pink-500 to-rose-500",
    categoria: "ingles",
  },
  {
    id: "esp-via",
    titulo: "Espanhol para Viagens",
    idioma: "Espanhol",
    nivel: "A1 - B1",
    descricao: "Focado em situações práticas de viagem: aeroportos, hotéis, restaurantes e direções no mundo hispanófono.",
    imagem: "from-orange-500 to-amber-600",
    categoria: "outros",
  },
  {
    id: "fra-bas",
    titulo: "Francês Básico",
    idioma: "Francês",
    nivel: "A1 - A2",
    descricao: "Descubra o idioma da cultura e da gastronomia. Domine expressões cotidianas, pronúncia básica e gramática introdutória.",
    imagem: "from-sky-500 to-blue-600",
    categoria: "outros",
  },
  {
    id: "ita-con",
    titulo: "Italiano para Conversação",
    idioma: "Italiano",
    nivel: "A2 - B2",
    descricao: "Fale com paixão! Aulas práticas focadas em diálogo e pronúncia do italiano clássico e expressões do cotidiano.",
    imagem: "from-emerald-500 to-teal-600",
    categoria: "outros",
  },
  {
    id: "ale-int",
    titulo: "Alemão Intensivo",
    idioma: "Alemão",
    nivel: "A1 - B2",
    descricao: "Metodologia acelerada para quem quer aprender alemão por motivos acadêmicos ou profissionais em tempo recorde.",
    imagem: "from-red-500 to-orange-600",
    categoria: "outros",
  },
  {
    id: "jap-ini",
    titulo: "Japonês para Iniciantes",
    idioma: "Japonês",
    nivel: "N5 - N4",
    descricao: "Aprenda a ler Hiragana e Katakana, kanjis básicos e inicie sua comunicação falada no idioma da tecnologia e da cultura pop.",
    imagem: "from-violet-500 to-fuchsia-600",
    categoria: "outros",
  },
  {
    id: "cor-kpop",
    titulo: "Coreano para Fãs de K-pop",
    idioma: "Coreano",
    nivel: "Iniciante",
    descricao: "Aprenda o alfabeto Hangul, gramática básica e vocabulário focado em doramas, músicas de K-pop e cultura coreana.",
    imagem: "from-fuchsia-500 to-pink-600",
    categoria: "outros",
  },
  {
    id: "pre-toefl",
    titulo: "Preparação para TOEFL",
    idioma: "Inglês",
    nivel: "Avançado C1",
    descricao: "Treinamento intensivo focado nas seções do exame TOEFL. Simulados reais, dicas de redação e estratégias para obter pontuação máxima.",
    imagem: "from-slate-700 to-zinc-900",
    categoria: "preparatorio",
  },
];

export const DEPOIMENTOS: Depoimento[] = [
  {
    id: "dep-1",
    nome: "Juliana Mendes",
    avatar: "JM",
    curso: "Inglês Intermediário",
    comentario: "O assistente de IA me indicou o curso ideal para o meu nível. Consegui uma vaga em uma empresa internacional após 6 meses de curso!",
    estrelas: 5,
  },
  {
    id: "dep-2",
    nome: "Lucas Ferreira",
    avatar: "LF",
    curso: "Espanhol para Viagens",
    comentario: "Fiz o curso focado em viagens antes do meu mochilão. As aulas são super práticas e a assistente virtual tirou minhas dúvidas de certificado em segundos.",
    estrelas: 5,
  },
  {
    id: "dep-3",
    nome: "Mariana Souza",
    avatar: "MS",
    curso: "Japonês para Iniciantes",
    comentario: "Sempre achei que japonês fosse impossível de aprender, mas a metodologia desmistifica o idioma. Consigo ler frases básicas muito rápido!",
    estrelas: 5,
  },
  {
    id: "dep-4",
    nome: "Rodrigo Costa",
    avatar: "RC",
    curso: "Preparação para TOEFL",
    comentario: "Consegui a pontuação necessária para o mestrado. Os simulados do TOEFL e o suporte da comunidade foram essenciais.",
    estrelas: 5,
  },
];

export const FAQ_ITEMS: FAQItem[] = [
  {
    id: "faq-1",
    pergunta: "Como funciona a emissão dos certificados dos cursos?",
    resposta: "Os certificados são emitidos digitalmente em PDF com QR Code de validação mediante a conclusão de no mínimo 80% das aulas assistidas e envio dos exercícios.",
  },
  {
    id: "faq-2",
    pergunta: "Qual é a política de reembolso da matrícula?",
    resposta: "Oferecemos garantia incondicional de 7 dias corridos. Você pode solicitar 100% de reembolso diretamente no painel do aluno ou pelo suporte sem burocracia.",
  },
  {
    id: "faq-3",
    pergunta: "Como funciona o programa de bolsas de estudos?",
    resposta: "O programa 'IA para Todos' concede bolsas integrais (100%) e parciais (50%) para estudantes de baixa renda mediante processo seletivo semestral.",
  },
  {
    id: "faq-4",
    pergunta: "Onde posso tirar dúvidas sobre as aulas de idiomas?",
    resposta: "Você pode usar nosso Fórum de Alunos abaixo de cada aula ou a comunidade do Discord. Além disso, nosso Assistente Virtual de IA está disponível 24h.",
  },
];
