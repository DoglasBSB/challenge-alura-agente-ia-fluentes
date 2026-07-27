import os
import json
import requests
from pathlib import Path
from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai
from google.genai import types

BASE_URL = "http://localhost:3000"
RAIZ = Path(__file__).parent.parent
DATASET_PATH = RAIZ / "datasets" / "golden_dataset.json"
ENV_PATH = RAIZ / ".env"

# Carrega as chaves do .env manualmente para evitar dependências extras
if ENV_PATH.exists():
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key not in os.environ:
                    os.environ[key] = val

# Classe de LLM customizada para o DeepEval baseada no SDK oficial google-genai
class GeminiJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="gemini-flash-latest"):
        self.model_name = model_name
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def load_model(self):
        return self.client

    def generate(self, prompt: str, schema=None) -> str:
        import time
        # Se schema for passado, usamos a restrição nativa de JSON Schema do Gemini
        for tentativa in range(4):
            try:
                if schema:
                    config = types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema
                    )
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=config
                    )
                else:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt
                    )
                return response.text
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(4 * (tentativa + 1))
                else:
                    raise e
        return ""

    async def a_generate(self, prompt: str, schema=None) -> str:
        # Execução síncrona envelopada em coroutine para compatibilidade assíncrona
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_name

# Configura o modelo Juiz do DeepEval
# Se houver chaves do Gemini no ambiente, usamos o GeminiJudge para avaliações robustas
if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    chave = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    os.environ["GEMINI_API_KEY"] = chave
    os.environ["GOOGLE_API_KEY"] = chave
    try:
        JUDGE_MODEL = GeminiJudge(model_name="gemini-flash-latest")
    except Exception:
        JUDGE_MODEL = None
else:
    JUDGE_MODEL = None

def chamar_assistente(mensagem: str, contexto: str = "") -> str:
    """Helper que faz requisição ao endpoint do assistente"""
    resp = requests.post(
        f"{BASE_URL}/api/chat",
        json={"message": mensagem, "context": contexto},
        timeout=180
    )
    resp.raise_for_status()
    return resp.json()["reply"]

def carregar_golden_dataset():
    """Helper para carregar o arquivo golden_dataset.json"""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset não encontrado em: {DATASET_PATH}")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
