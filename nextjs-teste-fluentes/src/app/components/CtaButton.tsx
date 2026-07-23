"use client";

export default function CtaButton() {
  const handleClick = () => {
    if (typeof window !== "undefined") {
      window.dispatchEvent(
        new CustomEvent("open-assistant-chat", {
          detail: { message: "Quero saber mais sobre a escola e como funciona a emissão de certificados!" },
        })
      );
    }
  };

  return (
    <button
      onClick={handleClick}
      className="px-8 py-4 rounded-xl font-bold bg-white text-indigo-950 hover:bg-zinc-100 transition-all shadow-lg active:scale-95 cursor-pointer text-sm"
    >
      Tirar Dúvidas com a IA
    </button>
  );
}
