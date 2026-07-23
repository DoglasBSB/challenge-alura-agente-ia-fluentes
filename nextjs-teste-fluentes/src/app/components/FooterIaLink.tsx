"use client";

export default function FooterIaLink() {
  const handleClick = () => {
    if (typeof window !== "undefined") {
      window.dispatchEvent(new CustomEvent("open-assistant-chat"));
    }
  };

  return (
    <button
      onClick={handleClick}
      className="hover:text-indigo-500 cursor-pointer text-left focus:outline-none"
    >
      Falar com IA
    </button>
  );
}
