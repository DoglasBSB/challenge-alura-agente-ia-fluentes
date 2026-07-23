"""
Hooks de coleta de resultados para o relatório consolidado.

- @on_test_run_end (deepeval v4): captura scores de métricas → relatorios/deepeval_results.json
- pytest_runtest_makereport: captura pass/fail de TODOS os testes → relatorios/pytest_all_results.json
"""

import json
import re
import pytest
from datetime import datetime
from pathlib import Path

from deepeval import on_test_run_end
from deepeval.test_run import global_test_run_manager

PASTA = Path(__file__).parent.parent / "relatorios"
PASTA.mkdir(exist_ok=True)


# ── Hook DeepEval v4: captura scores de métricas ─────────────────────────────────

@on_test_run_end
def exportar_resultados_deepeval():
    """Salva resultados com scores de métricas após testes DeepEval."""
    test_run = global_test_run_manager.get_test_run()
    if test_run is None:
        return

    resultados = []
    for caso in test_run.test_cases:
        metricas = []
        for m in (caso.metrics_data or []):
            metricas.append({
                "name": m.name,
                "score": round(m.score, 3) if m.score is not None else 0,
                "threshold": m.threshold,
                "reason": m.reason or "",
                "passed": m.success,
            })

        resultados.append({
            "name": caso.name,
            "success": caso.success,
            "metrics_data": metricas,
        })

    caminho = PASTA / "deepeval_results.json"
    caminho.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 Resultados DeepEval exportados: {caminho}")


# ── Hook pytest: captura pass/fail de todos os testes ───────────────────────────

_resultados_sessao: dict[str, list] = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    arquivo = Path(item.fspath).name
    if arquivo not in _resultados_sessao:
        _resultados_sessao[arquivo] = []

    score = None
    threshold = None
    erro_curto = None

    if rep.failed and rep.longrepr:
        texto = str(rep.longrepr)

        m = re.search(r'score[:\s=]+([0-9.]+)', texto, re.I)
        if m:
            score = float(m.group(1))

        m = re.search(r'threshold[:\s=]+([0-9.]+)', texto, re.I)
        if m:
            threshold = float(m.group(1))

        linhas_uteis = [
            l.strip() for l in texto.split("\n")
            if l.strip() and not l.strip().startswith("E  File")
        ]
        erro_curto = linhas_uteis[0][:220] if linhas_uteis else texto[:220]

    _resultados_sessao[arquivo].append({
        "nome": item.name,
        "passou": rep.passed,
        "duracao_s": round(rep.duration, 2),
        "score": score,
        "threshold": threshold,
        "erro": erro_curto,
    })


def pytest_sessionfinish(session, exitstatus):
    try:
        exportar_resultados_deepeval()
    except Exception as e:
        print(f"Erro ao exportar deepeval: {e}")

    if not _resultados_sessao:
        return

    arquivos_info = {}
    for arq, testes in _resultados_sessao.items():
        passou = sum(1 for t in testes if t["passou"])
        arquivos_info[arq] = {
            "testes": testes,
            "passou": passou,
            "total": len(testes),
            "taxa_aprovacao": round(passou / len(testes) * 100) if testes else 0,
        }

    total = sum(len(t) for t in _resultados_sessao.values())
    total_passou = sum(i["passou"] for i in arquivos_info.values())

    dados = {
        "gerado_em": datetime.now().isoformat(),
        "arquivos": arquivos_info,
        "total": total,
        "passou": total_passou,
        "taxa_aprovacao": round(total_passou / total * 100) if total else 0,
    }

    caminho = PASTA / "pytest_all_results.json"
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 Resultados pytest exportados: {caminho}")
