"use client";

interface BlogIaButtonProps {
  postTitle: string;
}

export default function BlogIaButton({ postTitle }: BlogIaButtonProps) {
  const handleClick = () => {
    if (typeof window !== "undefined") {
      const event = new CustomEvent("open-assistant-chat", {
        detail: { message: `Gostaria de saber mais sobre o assunto do artigo: "${postTitle}".` },
      });
      window.dispatchEvent(event);
    }
  };

  return (
    <button
      onClick={handleClick}
      className="inline-flex items-center gap-1.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded-lg text-sm font-semibold text-indigo-600 dark:text-indigo-400 cursor-pointer group hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors text-left"
    >
      <span>Perguntar para a IA</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1"
        aria-hidden="true"
      >
        <path
          fillRule="evenodd"
          d="M3 10a.75.75 0 0 1 .75-.75h10.63l-3.01-3.04a.75.75 0 1 1 1.08-1.04l4.25 4.3a.75.75 0 0 1 0 1.06l-4.25 4.3a.75.75 0 1 1-1.08-1.04l3.01-3.04H3.75A.75.75 0 0 1 3 10Z"
          clipRule="evenodd"
        />
      </svg>
    </button>
  );
}
