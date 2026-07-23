"use client";

export default function OpenChatButton() {
  const handleClick = () => {
    if (typeof window !== "undefined") {
      const event = new CustomEvent("open-assistant-chat");
      window.dispatchEvent(event);
    }
  };

  return (
    <button
      onClick={handleClick}
      className="w-full sm:w-auto text-center px-6 py-3.5 rounded-xl font-semibold bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 hover:border-indigo-500/50 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all shadow-sm cursor-pointer"
    >
      Conversar com o Assistente
    </button>
  );
}
