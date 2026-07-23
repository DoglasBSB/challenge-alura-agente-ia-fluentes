"use client";

const SUGGESTIONS = [
  "Quero aprender inglês para iniciantes.",
  "Existe curso de idiomas para crianças?",
  "Quero aprender espanhol para viajar.",
  "Qual curso prepara para o TOEFL?",
  "Vocês oferecem certificado de conclusão?",
];

export default function IaInteractiveSection() {
  const handleSuggestionClick = (suggestion: string) => {
    if (typeof window !== "undefined") {
      const event = new CustomEvent("open-assistant-chat", {
        detail: { message: suggestion },
      });
      window.dispatchEvent(event);
    }
  };

  return (
    <section className="py-20 bg-gradient-to-br from-indigo-900 via-indigo-950 to-violet-950 text-white rounded-3xl overflow-hidden shadow-2xl relative">
      {/* Background radial effects */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(120,119,198,0.2),transparent_50%)]" />
      <div className="absolute -bottom-48 -left-48 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl" />

      <div className="container mx-auto max-w-4xl px-6 relative z-10">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold bg-white/10 text-indigo-300 border border-white/10 backdrop-blur-md mb-6">
              Consultor Inteligente
            </div>
            
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight mb-6 leading-tight">
              Seu consultor inteligente para aprender um novo idioma
            </h2>
            
            <p className="text-zinc-300 mb-8 text-base leading-relaxed">
              Está em dúvida sobre qual idioma escolher, qual é o seu nível atual ou como funcionam os horários? Pergunte diretamente ao nosso Assistente IA! Ele foi treinado para guiar você rumo à fluência.
            </p>

            <button
              onClick={() => handleSuggestionClick("Olá! Como você pode me ajudar a escolher um curso?")}
              className="px-6 py-3.5 rounded-xl font-bold bg-white text-indigo-950 hover:bg-zinc-100 transition-all shadow-lg active:scale-95 inline-flex items-center gap-2 cursor-pointer"
            >
              <span>Conversar agora</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="w-4 h-4"
              >
                <path
                  fillRule="evenodd"
                  d="M3 10a.75.75 0 0 1 .75-.75h10.63l-3.01-3.04a.75.75 0 1 1 1.08-1.04l4.25 4.3a.75.75 0 0 1 0 1.06l-4.25 4.3a.75.75 0 1 1-1.08-1.04l3.01-3.04H3.75A.75.75 0 0 1 3 10Z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>

          {/* Interface Simulada do Chat */}
          <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md p-6 shadow-xl flex flex-col justify-between h-[340px]">
            <div>
              <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
                <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center font-bold text-sm text-white">IA</div>
                <div>
                  <h4 className="font-bold text-xs text-white">Assistente Virtual</h4>
                  <span className="text-[10px] text-green-400 font-medium">● Sugestões de perguntas</span>
                </div>
              </div>

              <div className="space-y-2.5 max-h-[220px] overflow-y-auto">
                <p className="text-[11px] text-indigo-200 font-semibold mb-3">Selecione uma dúvida para ver a IA respondendo no chat:</p>
                {SUGGESTIONS.map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="w-full text-left p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-505/30 text-xs text-zinc-200 font-medium transition-all flex items-center justify-between group cursor-pointer"
                  >
                    <span className="line-clamp-1">{suggestion}</span>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                      className="w-3.5 h-3.5 text-zinc-400 group-hover:text-white transition-colors shrink-0 ml-2"
                    >
                      <path
                        fillRule="evenodd"
                        d="M3 10a.75.75 0 0 1 .75-.75h10.63l-3.01-3.04a.75.75 0 1 1 1.08-1.04l4.25 4.3a.75.75 0 0 1 0 1.06l-4.25 4.3a.75.75 0 1 1-1.08-1.04l3.01-3.04H3.75A.75.75 0 0 1 3 10Z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
