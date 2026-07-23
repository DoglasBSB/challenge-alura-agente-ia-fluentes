export interface Curso {
  id: string;
  titulo: string;
  idioma: string;
  nivel: string;
  descricao: string;
  imagem: string; // Para uso sem imagens reais, usaremos ícones ou gradientes visuais premium
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
    descricao: "Aprenda a ler Hiragana e Katakana, kanjis básicos e inicie sua comunicação falada no idioma da tecnologia e do anime.",
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
    curso: "Inglês para Negócios",
    comentario: "O assistente de IA me indicou o curso ideal para o meu nível e objetivos. Consegui uma vaga em uma empresa multinacional após 6 meses de curso intensivo!",
    estrelas: 5,
  },
  {
    id: "dep-2",
    nome: "Lucas Ferreira",
    avatar: "LF",
    curso: "Espanhol para Viagens",
    comentario: "Fiz o curso focado em viagens antes do meu mochilão pela América do Sul. As aulas são super dinâmicas e o vocabulário prático me salvou de vários perrengues.",
    estrelas: 5,
  },
  {
    id: "dep-3",
    nome: "Mariana Souza",
    avatar: "MS",
    curso: "Japonês para Iniciantes",
    comentario: "Sempre achei que japonês fosse impossível de aprender, mas a metodologia deles desmistifica o idioma. Consigo ler e entender frases básicas muito rápido.",
    estrelas: 4,
  },
  {
    id: "dep-4",
    nome: "Rodrigo Costa",
    avatar: "RC",
    curso: "Preparação para TOEFL",
    comentario: "Consegui a nota que precisava para o meu mestrado na Europa. Os simulados do TOEFL e o feedback nas redações foram essenciais para minha aprovação.",
    estrelas: 5,
  },
];

export const FAQ_ITEMS: FAQItem[] = [
  {
    id: "faq-1",
    pergunta: "Como funciona a metodologia da escola?",
    resposta: "Nossa metodologia combina aulas focadas em conversação ativa com professores especializados e o suporte de nossa IA integrada para tirar dúvidas gramaticais, traduzir e praticar conversação 24 horas por dia.",
  },
  {
    id: "faq-2",
    pergunta: "Os cursos possuem certificado de conclusão?",
    resposta: "Sim, todos os nossos cursos oferecem certificado digital de conclusão com a carga horária detalhada e o nível de proficiência alcançado conforme o Quadro Comum Europeu de Referência para Línguas (QCE/CEFR).",
  },
  {
    id: "faq-3",
    pergunta: "As aulas são online ou presenciais?",
    resposta: "Oferecemos turmas 100% online ao vivo em nossa plataforma interativa e também modalidades híbridas com aulas de conversação presenciais em nossos polos.",
  },
  {
    id: "faq-4",
    pergunta: "Como o Assistente de IA me ajuda no dia a dia?",
    resposta: "O assistente de IA serve como um consultor pedagógico e tutor particular. Ele pode recomendar o melhor curso para seu nível, responder dúvidas de dever de casa de forma instantânea e simular diálogos realistas em outros idiomas.",
  },
  {
    id: "faq-5",
    pergunta: "Como faço para realizar a minha matrícula?",
    resposta: "Você pode falar diretamente com o nosso Assistente de IA no chat e ele guiará você no processo de inscrição ou nos horários disponíveis para o idioma que deseja estudar.",
  },
];
