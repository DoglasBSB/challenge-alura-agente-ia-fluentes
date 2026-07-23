"""
Gerador customizado do Garak para o Assistente Chat LLM (FastAPI).

Uso:
  garak --generator_option_file garak_generator.py \
        --generator_name AssistenteChatGenerator \
        --probes promptinject,dan,toxicity \
        --report_prefix relatorios/garak-fastapi
"""

import os
import requests
from garak.generators.base import Generator


# ── Assistente Portal Next.js ───────────────────────────────────────────────────

class AssistenteChatGenerator(Generator):
    """
    Conecta o Garak à API de chat da Landing Page (porta 3000).
    Endpoint: POST /api/chat  →  {"message": "..."}
    """

    name = "assistente-chat-local"
    supports_multiple_generations = False

    ENDPOINT = os.environ.get("PORTAL_URL", "http://localhost:3000") + "/api/chat"

    def _call_model(self, prompt: str, generations_this_call: int = 1) -> list[str]:
        try:
            resp = requests.post(
                self.ENDPOINT,
                json={"message": prompt},
                timeout=60
            )
            resp.raise_for_status()
            return [resp.json()["reply"]]

        except requests.Timeout:
            return ["[ERRO: timeout]"]
        except Exception as e:
            return [f"[ERRO: {str(e)}]"]

