"use client";

import { useState } from "react";
import { CURSOS } from "../data/landingData";

export default function CursosGrid() {
  const [activeCategory, setActiveCategory] = useState<"todos" | "tecnologia" | "ia" | "preparatorio">("todos");

  const filteredCursos = CURSOS.filter((curso) => {
    if (activeCategory === "todos") return true;
    return curso.categoria === activeCategory;
  });

  const handleSaibaMais = (cursoTitulo: string) => {
    if (typeof window !== "undefined") {
      const event = new CustomEvent("open-assistant-chat", {
        detail: { message: `Quero saber mais detalhes sobre o curso "${cursoTitulo}" e como funciona a emissão de certificado.` },
      });
      window.dispatchEvent(event);
    }
  };

  return (
    <section id="cursos" className="py-20 bg-zinc-100/50 dark:bg-zinc-950/30 border-y border-zinc-200/55 dark:border-zinc-900/50">
      <div className="container mx-auto max-w-5xl px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight mb-4 text-zinc-900 dark:text-zinc-50">
            Nossos Cursos de Tecnologia & IA
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 max-w-lg mx-auto">
            Projetados para capacitar você do básico da programação ao desenvolvimento de Agentes de IA e RAG.
          </p>
        </div>

        {/* Filtros */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-12">
          {[
            { id: "todos", label: "Todos os Cursos" },
            { id: "tecnologia", label: "Programação & Lógica" },
            { id: "ia", label: "IA & RAG" },
            { id: "preparatorio", label: "Agentes & Cloud" },
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id as any)}
              className={`px-4.5 py-2.5 rounded-full text-xs font-semibold border transition-all cursor-pointer ${
                activeCategory === cat.id
                  ? "bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-500/10"
                  : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Grade de Cursos */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredCursos.map((curso) => (
            <div
              key={curso.id}
              className="group relative flex flex-col justify-between rounded-2xl border border-zinc-200/60 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
            >
              <div>
                {/* Indicador de Curso */}
                <div className={`w-full h-36 rounded-xl p-4 flex flex-col justify-between text-white mb-6 shadow-inner relative overflow-hidden bg-gradient-to-tr ${curso.imagem}`}>
                  <div className="absolute inset-0 bg-black/10 mix-blend-overlay -z-10" />
                  <div className="flex items-center justify-between z-10">
                    <span className="text-[10px] font-bold tracking-wider uppercase bg-white/20 backdrop-blur-md px-2.5 py-0.5 rounded-full">
                      {curso.idioma}
                    </span>
                    <span className="text-[10px] font-bold bg-zinc-900/40 backdrop-blur-md px-2.5 py-0.5 rounded-full">
                      {curso.nivel}
                    </span>
                  </div>
                  <div className="font-black text-lg tracking-tight z-10 drop-shadow-sm">
                    {curso.titulo}
                  </div>
                </div>

                <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-6 leading-relaxed line-clamp-3">
                  {curso.descricao}
                </p>
              </div>

              {/* Botão Saiba Mais */}
              <button
                onClick={() => handleSaibaMais(curso.titulo)}
                className="w-full text-center py-2.5 rounded-xl text-xs font-bold border border-zinc-200 dark:border-zinc-800 hover:border-indigo-500/50 hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 text-zinc-800 dark:text-zinc-200 dark:hover:text-indigo-400 hover:text-indigo-600 transition-all cursor-pointer"
              >
                Tirar Dúvidas com o Assistente IA
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
