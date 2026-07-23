"use client";

import { useState } from "react";
import { FAQ_ITEMS } from "../data/landingData";

export default function FaqSection() {
  const [openFaqId, setOpenFaqId] = useState<string | null>(null);

  const toggleFaq = (id: string) => {
    setOpenFaqId(openFaqId === id ? null : id);
  };

  return (
    <section className="py-20">
      <div className="container mx-auto max-w-3xl px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-black tracking-tight mb-4 text-zinc-900 dark:text-zinc-50">
            Perguntas Frequentes
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400">
            Esclareça suas dúvidas rápidas sobre nossa metodologia, cursos e o assistente de IA.
          </p>
        </div>

        <div className="space-y-4">
          {FAQ_ITEMS.map((faq) => {
            const isOpen = openFaqId === faq.id;

            return (
              <div
                key={faq.id}
                className="rounded-2xl border border-zinc-200/60 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden shadow-sm transition-all"
              >
                <button
                  onClick={() => toggleFaq(faq.id)}
                  className="w-full flex items-center justify-between p-5 text-left font-bold text-sm text-zinc-800 dark:text-zinc-200 hover:bg-zinc-50/50 dark:hover:bg-zinc-850/50 transition-colors focus:outline-none cursor-pointer"
                >
                  <span>{faq.pergunta}</span>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                    stroke="currentColor"
                    className={`w-4.5 h-4.5 text-zinc-500 transition-transform duration-300 ${
                      isOpen ? "rotate-180 text-indigo-500" : ""
                    }`}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                  </svg>
                </button>

                <div
                  className={`transition-all duration-300 ease-in-out overflow-hidden ${
                    isOpen ? "max-h-[200px] border-t border-zinc-100 dark:border-zinc-800/80" : "max-h-0"
                  }`}
                >
                  <div className="p-5 text-xs sm:text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed bg-zinc-50/20 dark:bg-zinc-950/10">
                    {faq.resposta}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
