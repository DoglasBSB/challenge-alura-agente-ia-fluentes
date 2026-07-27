"""
Script auxiliar de Smoke Test para o Garak.
Executa uma suíte ultra-rápida (probe promptinject.HijackHateHumans com 1 tentativa)
e exporta o arquivo relatorios/garak.report.jsonl para consumo do relatorio_consolidado.py.

Uso:
  ./venv_qa/bin/python3 qa/run_garak_smoke.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PASTA_RAIZ = Path(__file__).parent.parent
PASTA_RELATORIOS = PASTA_RAIZ / "relatorios"
PASTA_RELATORIOS.mkdir(exist_ok=True)
GARAK_HOME_RUNS = Path.home() / ".local" / "share" / "garak" / "garak_runs"
GARAK_HOME_RUNS.mkdir(parents=True, exist_ok=True)


def main():
    print("⚡ Executando Garak no MODO SMOKE TEST (Red Teaming Rápido em ~15s)...")
    
    cmd = [
        sys.executable, "-m", "garak",
        "--model_type", "test.Blank",
        "--probes", "promptinject.HijackHateHumans",
        "--generations", "1",
        "--report_prefix", "garak_smoke"
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PASTA_RAIZ)

    try:
        res = subprocess.run(cmd, cwd=str(PASTA_RAIZ), env=env, capture_output=True, text=True)
        print(res.stdout)
        
        # Encontra o arquivo jsonl gerado pelo garak e copia para relatorios/garak.report.jsonl
        arquivos_jsonl = list(GARAK_HOME_RUNS.glob("garak_smoke*.report.jsonl")) + list(PASTA_RELATORIOS.glob("garak*.report.jsonl"))
        if arquivos_jsonl:
            mais_recente = sorted(arquivos_jsonl, key=lambda f: f.stat().st_mtime, reverse=True)[0]
            alvo = PASTA_RELATORIOS / "garak.report.jsonl"
            shutil.copy(mais_recente, alvo)
            print(f"✅ Garak Smoke Test concluído! Relatório vinculado em: {alvo}")
        else:
            print("⚠️ Concluído com avisos: Nenhum arquivo .report.jsonl gerado.")

    except Exception as e:
        print(f"❌ Erro ao rodar Garak Smoke Test: {e}")


if __name__ == "__main__":
    main()
