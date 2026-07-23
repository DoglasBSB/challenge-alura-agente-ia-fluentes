import type { Metadata } from "next";
import OpenChatButton from "./components/OpenChatButton";
import CursosGrid from "./components/CursosGrid";
import IaInteractiveSection from "./components/IaInteractiveSection";
import FaqSection from "./components/FaqSection";
import { DEPOIMENTOS } from "./data/landingData";
import CtaButton from "./components/CtaButton";
import FooterIaLink from "./components/FooterIaLink";

export const metadata: Metadata = {
  title: "IA Fluentes | Escola Online de Idiomas com IA",
  description: "Aprenda Inglês, Espanhol, Francês, Italiano, Alemão, Japonês, Coreano e TOEFL com assistente de IA 24h.",
};

export default function IndexPage() {
  return (
    <div className="flex-1 text-zinc-900 dark:text-zinc-100 selection:bg-indigo-500 selection:text-white">
      {/* Decorações de fundo */}
      <div className="absolute inset-x-0 top-0 -z-10 h-[800px] overflow-hidden">
        <div className="absolute -top-[30%] left-[50%] h-[700px] w-[1200px] -translate-x-[50%] rounded-full bg-gradient-to-tr from-indigo-500/10 via-violet-500/5 to-transparent blur-3xl dark:from-indigo-900/10 dark:via-violet-950/5" />
      </div>

      {/* 1. SEÇÃO HERO */}
      <header className="container mx-auto max-w-5xl px-6 pt-20 pb-20 text-center md:text-left md:pt-32">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full px-3.5 py-1 text-xs font-semibold bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 border border-indigo-100/50 dark:border-indigo-900/30 backdrop-blur-md mb-6">
            <span className="flex h-2 w-2 rounded-full bg-indigo-600 dark:bg-indigo-400 animate-pulse" />
            Metodologia IA Fluentes
          </div>
          
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-black tracking-tight leading-[1.1] mb-6">
            Aprenda Vários Idiomas com{" "}
            <span className="bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600 dark:from-indigo-400 dark:via-purple-400 dark:to-indigo-400 bg-clip-text text-transparent">
              Inteligência Artificial
            </span>
          </h1>
          
          <p className="text-lg text-zinc-600 dark:text-zinc-400 mb-8 max-w-xl leading-relaxed">
            Descubra uma nova forma de alcançar a fluência em Inglês, Espanhol, Francês, Italiano, Alemão, Japonês e Coreano com nosso assistente virtual 24 horas.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4">
            <a
              href="#cursos"
              className="w-full sm:w-auto text-center px-6 py-3.5 rounded-xl font-semibold bg-zinc-900 dark:bg-zinc-100 hover:bg-zinc-800 dark:hover:bg-zinc-200 text-white dark:text-zinc-950 transition-all shadow-lg shadow-zinc-900/10 cursor-pointer"
            >
              Conhecer os Cursos
            </a>
            <OpenChatButton />
          </div>
        </div>
      </header>

      {/* 2. SEÇÃO BENEFÍCIOS */}
      <section className="py-20 bg-zinc-55/30 dark:bg-zinc-900/20 border-t border-zinc-200/60 dark:border-zinc-800/60">
        <div className="container mx-auto max-w-5xl px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-black tracking-tight mb-4">Por que escolher a IA Fluentes?</h2>
            <p className="text-zinc-600 dark:text-zinc-400 max-w-md mx-auto">
              Combinamos ensino de alto nível com um ecossistema completo de suporte ao estudante.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                title: "Professores Nativos",
                desc: "Aulas com professores nativos e certificados na área de ensino de idiomas.",
                svg: (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-indigo-500">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                  </svg>
                )
              },
              {
                title: "Material Digital Completo",
                desc: "Acesso a e-books, exercícios interativos e audios sem custo adicional.",
                svg: (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-indigo-500">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                  </svg>
                )
              },
              {
                title: "Certificados com QR Code",
                desc: "Certificados digitais com verificação de autenticidade e carga horária detalhada.",
                svg: (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-indigo-500">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
                  </svg>
                )
              },
              {
                title: "Garantia de 7 Dias",
                desc: "Garantia incondicional de reembolso total dentro de 7 dias após a matrícula.",
                svg: (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-indigo-500">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                )
              },
            ].map((ben, idx) => (
              <div
                key={idx}
                className="rounded-2xl border border-zinc-200/60 dark:border-zinc-800 bg-white dark:bg-zinc-900/60 p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 flex items-center justify-center mb-4">
                  {ben.svg}
                </div>
                <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-2">{ben.title}</h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">{ben.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 3. SEÇÃO CURSOS */}
      <CursosGrid />

      {/* 4. SEÇÃO COMO FUNCIONA */}
      <section className="py-20">
        <div className="container mx-auto max-w-4xl px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-black tracking-tight mb-4">Como Funciona o Atendimento ao Aluno</h2>
            <p className="text-zinc-600 dark:text-zinc-400 max-w-md mx-auto">
              Três passos simples para tirar suas dúvidas com o nosso Assistente de IA baseado em RAG.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative">
            <div className="hidden md:block absolute top-[52px] left-[15%] right-[15%] h-[2px] bg-indigo-100 dark:bg-indigo-900 -z-10" />

            {[
              {
                step: "1",
                title: "Escolha o Idioma",
                desc: "Selecione o idioma que deseja aprender e seus objetivos acadêmicos ou profissionais.",
              },
              {
                step: "2",
                title: "Consulte a IA 24h",
                desc: "Pergunte sobre regulamento, reembolsos, certificados, bolsas ou horários.",
              },
              {
                step: "3",
                title: "Matricule-se & Comece",
                desc: "Receba a resposta do agente e dê início à sua jornada rumo à fluência.",
              },
            ].map((step, idx) => (
              <div key={idx} className="flex flex-col items-center text-center px-4">
                <div className="w-12 h-12 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 border-4 border-white dark:border-zinc-950 shadow-md flex items-center justify-center font-bold text-sm mb-4">
                  {step.step}
                </div>
                <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-2">{step.title}</h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5. SEÇÃO CENTRAL DE DESTAQUE IA */}
      <div className="container mx-auto max-w-5xl px-6 pb-20">
        <IaInteractiveSection />
      </div>

      {/* 6. SEÇÃO DEPOIMENTOS */}
      <section className="py-20 bg-zinc-100/50 dark:bg-zinc-950/30 border-y border-zinc-200/55 dark:border-zinc-900/50">
        <div className="container mx-auto max-w-5xl px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-black tracking-tight mb-4">Histórias dos Nossos Alunos</h2>
            <p className="text-zinc-600 dark:text-zinc-400 max-w-md mx-auto">
              Veja o depoimento de quem já estuda conosco e alcançou a fluência em um novo idioma.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {DEPOIMENTOS.map((dep) => (
              <div
                key={dep.id}
                className="rounded-2xl border border-zinc-200/60 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6 shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex gap-0.5 text-amber-500 mb-4">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <svg
                        key={i}
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill={i < dep.estrelas ? "currentColor" : "none"}
                        stroke="currentColor"
                        strokeWidth={1.5}
                        className="w-4 h-4"
                      >
                        <path d="M10.868 2.784c-.304-.793-1.432-.793-1.736 0l-1.39 3.63a.5.5 0 0 1-.383.328l-3.896.353c-.854.077-1.196 1.13-.538 1.691l2.95 2.518a.5.5 0 0 1 .15.462l-.886 3.82c-.195.842.71 1.499 1.439 1.053l3.352-2.073a.5.5 0 0 1 .486 0l3.352 2.073c.73.446 1.634-.21 1.44-1.053l-.887-3.82a.5.5 0 0 1 .15-.462l2.95-2.518c.658-.56.316-1.614-.538-1.69l-3.897-.354a.5.5 0 0 1-.382-.329l-1.39-3.63Z" />
                      </svg>
                    ))}
                  </div>

                  <p className="text-xs text-zinc-650 dark:text-zinc-400 italic mb-6 leading-relaxed">
                    "{dep.comentario}"
                  </p>
                </div>

                <div className="flex items-center gap-3 border-t border-zinc-100 dark:border-zinc-800/80 pt-4">
                  <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center text-xs font-bold text-white shadow-inner">
                    {dep.avatar}
                  </div>
                  <div>
                    <h4 className="font-bold text-xs text-zinc-850 dark:text-zinc-100">{dep.nome}</h4>
                    <span className="text-[10px] text-zinc-500 dark:text-zinc-400">{dep.curso}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. SEÇÃO FAQ */}
      <FaqSection />

      {/* 8. SEÇÃO CHAMADA FINAL (CTA) */}
      <section className="container mx-auto max-w-5xl px-6 py-8">
        <div className="bg-gradient-to-br from-indigo-600 to-violet-700 text-white rounded-3xl p-12 text-center shadow-xl relative overflow-hidden">
          <div className="absolute inset-0 bg-black/5" />
          <div className="relative z-10 max-w-xl mx-auto">
            <h2 className="text-3xl sm:text-4xl font-black mb-4">Comece hoje a aprender um novo idioma</h2>
            <p className="text-indigo-100 text-sm mb-8">
              Pergunte ao nosso Assistente de IA sobre regulamento, reembolsos, certificados, bolsas ou sobre os 10 cursos disponíveis!
            </p>
            <CtaButton />
          </div>
        </div>
      </section>

      {/* Rodapé da Página */}
      <footer className="bg-white dark:bg-zinc-900 border-t border-zinc-200/60 dark:border-zinc-800/80 py-12 mt-16">
        <div className="container mx-auto max-w-5xl px-6">
          <div className="grid gap-8 sm:grid-cols-2 md:grid-cols-4 text-sm mb-8">
            <div>
              <h4 className="font-bold text-sm mb-3">IA Fluentes</h4>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                Escola Online de Idiomas integrada com Inteligência Artificial e RAG para guiá-lo no seu ritmo.
              </p>
            </div>
            <div>
              <h4 className="font-bold text-sm mb-3">Links Rápidos</h4>
              <ul className="space-y-2 text-xs text-zinc-650 dark:text-zinc-400">
                <li><a href="#cursos" className="hover:text-indigo-500">Cursos</a></li>
                <li><FooterIaLink /></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-sm mb-3">Redes Sociais</h4>
              <ul className="space-y-2 text-xs text-zinc-650 dark:text-zinc-400">
                <li><a href="#" className="hover:text-indigo-500">Instagram</a></li>
                <li><a href="#" className="hover:text-indigo-500">LinkedIn</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-sm mb-3">Contato</h4>
              <ul className="space-y-2 text-xs text-zinc-500 dark:text-zinc-400">
                <li>Email: contato@iafluentes.com.br</li>
                <li>Atendimento: Assistente Virtual 24h</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-zinc-100 dark:border-zinc-800 pt-8 text-center text-xs text-zinc-500 dark:text-zinc-400">
            <p>© 2026 IA Fluentes - Desafio Alura Agent. Todos os direitos reservados.</p>
            <p className="mt-1">Construído com Next.js 16 + Tailwind CSS + PDF RAG + LLM (Gemini/Ollama).</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
