"use client";

export default function CtaButton() {
  const handleClick = () => {
    if (typeof window !== "undefined") {
      window.dispatchEvent(
        new CustomEvent("open-assistant-chat", {
          detail: { message: "Quero começar um curso de inglês! Como faço minha matrícula?" },
        })
      );
    }
  };

  return (
    <button
      onClick={handleClick}
      className="px-8 py-4 rounded-xl font-bold bg-white text-indigo-950 hover:bg-zinc-100 transition-all shadow-lg active:scale-95 cursor-pointer text-sm"
    >
      Matricule-se Agora com a IA
    </button>
  );
}
