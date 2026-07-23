"use client";

import { useState, useEffect, useRef } from "react";

interface Message {
  role: "user" | "assistant";
  text: string;
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<{ online: boolean; model: string }>({
    online: true,
    model: "gemini-1.5-flash",
  });
  const [pendingMessage, setPendingMessage] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll para a última mensagem
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Verificar status da IA ao montar o componente
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const res = await fetch("/api/chat");
        const data = await res.json();
        const isOnline = data.status === "ok" || data.gemini_ativo || data.ollama_conectado;
        const modelName = data.modelo_padrao || data.modelo || (data.gemini_ativo ? "gemini-1.5-flash" : "llama3.2");
        setStatus({
          online: Boolean(isOnline),
          model: modelName,
        });
      } catch {
        setStatus({ online: false, model: "" });
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  // Escutar evento para abrir o chat a partir de cliques externos
  useEffect(() => {
    const handleOpen = (e: Event) => {
      setIsOpen(true);
      const customEvent = e as CustomEvent<{ message?: string }>;
      if (customEvent.detail?.message) {
        setPendingMessage(customEvent.detail.message);
      }
    };
    window.addEventListener("open-assistant-chat", handleOpen);
    return () => window.removeEventListener("open-assistant-chat", handleOpen);
  }, []);

  // Processar o envio da mensagem pendente quando o chat estiver aberto
  useEffect(() => {
    if (isOpen && pendingMessage) {
      const msg = pendingMessage;
      setPendingMessage(null);

      const sendPending = async () => {
        setMessages((prev) => [...prev, { role: "user", text: msg }]);
        setIsLoading(true);

        try {
          const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg }),
          });

          const data = await res.json();
          if (res.ok) {
            setMessages((prev) => [...prev, { role: "assistant", text: data.reply }]);
          } else {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                text: `Ops, ocorreu um erro: ${data.detail || "Erro inesperado."}`,
              },
            ]);
          }
        } catch {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              text: "Erro de conexão com o servidor. Verifique a conexão ou chaves de API.",
            },
          ]);
        } finally {
          setIsLoading(false);
        }
      };

      const timeout = setTimeout(sendPending, 400);
      return () => clearTimeout(timeout);
    }
  }, [isOpen, pendingMessage]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userText = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      const data = await res.json();
      if (res.ok) {
        setMessages((prev) => [...prev, { role: "assistant", text: data.reply }]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            text: `Ops, ocorreu um erro: ${data.detail || "Erro inesperado."}`,
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Erro de conexão com o servidor. Verifique a conexão ou chaves de API.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 font-sans">
      {/* Botão Flutuante de Abrir/Fechar */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-tr from-indigo-600 to-violet-600 text-white shadow-lg hover:shadow-indigo-500/30 hover:scale-105 active:scale-95 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 cursor-pointer"
        aria-label="Abrir chat do assistente"
      >
        {isOpen ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-6 h-6 animate-pulse"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z"
            />
          </svg>
        )}
      </button>

      {/* Janela de Chat */}
      {isOpen && (
        <div className="absolute bottom-18 right-0 w-[90vw] sm:w-[400px] h-[500px] rounded-2xl border border-zinc-200/80 dark:border-zinc-800 bg-white/95 dark:bg-zinc-900/95 shadow-2xl backdrop-blur-md flex flex-col justify-between overflow-hidden transition-all duration-300 animate-in fade-in slide-in-from-bottom-5">
          {/* Cabeçalho */}
          <div className="bg-gradient-to-r from-indigo-600 to-violet-600 text-white p-4 flex items-center justify-between shadow-md">
            <div>
              <h3 className="font-bold text-sm">Assistente IA Fluentes</h3>
              {/* Status da IA */}
              <div className="flex items-center gap-1.5 mt-0.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    status.online ? "bg-green-400 animate-pulse" : "bg-red-400"
                  }`}
                />
                <span className="text-[10px] text-zinc-100 font-medium">
                  {status.online
                    ? `IA Conectada (${status.model || "Gemini"})`
                    : "IA Desconectada"}
                </span>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white transition-colors cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
          </div>

          {/* Histórico de Mensagens */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-zinc-50/50 dark:bg-zinc-950/20">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center text-zinc-500 dark:text-zinc-400 py-8">
                <div className="w-12 h-12 bg-zinc-100 dark:bg-zinc-800 rounded-full flex items-center justify-center mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    className="w-6 h-6 text-indigo-500"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-2.833A8.9 8.9 0 0 1 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z"
                    />
                  </svg>
                </div>
                <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                  Olá! Sou o assistente virtual da IA Fluentes.
                </p>
                <p className="text-[11px] mt-1 px-4">
                  Pergunte-me sobre regulamentos, política de reembolso, certificados, bolsas de estudo ou cursos!
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  } animate-in fade-in slide-in-from-bottom-2 duration-200`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm shadow-sm ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white rounded-tr-none"
                        : "bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-100 border border-zinc-100 dark:border-zinc-700 rounded-tl-none"
                    }`}
                  >
                    <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  </div>
                </div>
              ))
            )}

            {/* Balão de carregamento (Digitando...) */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white dark:bg-zinc-800 border border-zinc-100 dark:border-zinc-700 px-4 py-3 rounded-2xl rounded-tl-none flex gap-1 items-center shadow-sm">
                  <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Área de Entrada */}
          <form
            onSubmit={handleSend}
            className="p-3 border-t border-zinc-100 dark:border-zinc-800 bg-white dark:bg-zinc-900 flex gap-2 items-center"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pergunte sobre regulamento, reembolso, certificados..."
              className="flex-1 bg-zinc-50 dark:bg-zinc-950 border border-zinc-200/80 dark:border-zinc-800 rounded-xl px-4 py-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 dark:text-zinc-100"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:hover:bg-indigo-600 text-white p-2.5 rounded-xl transition-all shadow-md active:scale-95 flex items-center justify-center cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="w-4 h-4"
              >
                <path d="M3.105 2.289a.75.75 0 0 0-.826.95l1.414 4.925c.09.315.335.566.654.658L10.5 10l-6.153 1.178a.75.75 0 0 0-.654.658l-1.414 4.925a.75.75 0 0 0 .826.95 48.394 48.394 0 0 0 15.3-6.931a.75.75 0 0 0 0-1.25 48.394 48.394 0 0 0-15.3-6.931Z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
