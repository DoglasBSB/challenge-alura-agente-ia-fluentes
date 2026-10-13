"""
Gerador customizado do Garak para o Assistente Chat LLM (FastAPI).

Uso:
  garak --generator_option_file garak_generator.py \
        --generator_name AssistenteChatGenerator \
        --probes promptinject,dan,toxicity \
        --report_prefix relatorios/garak-fastapi
"""

import os
import re
import requests
from urllib.parse import urlparse, urlunparse
from garak.generators.base import Generator


def build_validated_url(base_url: str) -> str:
    try:
        # Minimal path validation
        if "/../" in base_url or re.search(r"/%2e%2e/", base_url, re.IGNORECASE):
            raise ValueError("Invalid path")
        
        parsed = urlparse(base_url)
        
        # Protocol + host checks
        if parsed.scheme not in ("http", "https"):
            raise ValueError("Invalid protocol")
        if not parsed.hostname:
            raise ValueError("Invalid host")
        allowed_domains = ["localhost"]  # add your allowed domains here
        if parsed.hostname.lower() not in allowed_domains:
            raise ValueError("Invalid host")
        
        return urlunparse(parsed)
    except Exception:
        raise ValueError("Invalid URL")


# ── Assistente Portal Next.js ───────────────────────────────────────────────────

class AssistenteChatGenerator(Generator):
    """
    Conecta o Garak à API de chat da Landing Page (porta 3000).
    Endpoint: POST /api/chat  →  {"message": "..."}
    """

    name = "assistente-chat-local"
    supports_multiple_generations = False

    ENDPOINT = build_validated_url(os.environ.get("PORTAL_URL", "http://localhost:3000")) + "/api/chat"

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

