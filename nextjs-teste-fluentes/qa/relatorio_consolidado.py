"""
Consolidador de Relatórios — todos os testes em um único dashboard HTML.

Fontes lidas:
  relatorios/pytest_all_results.json   ← todos os testes pytest (conftest.py)
  relatorios/deepeval_results.json     ← scores de métricas DeepEval (conftest.py)
  relatorios/garak.report.jsonl        ← Garak red teaming
  relatorios/giskard_scan.html         ← Giskard scan de risco
  relatorios/locust_report.html        ← Locust carga e latência

Saída:
  relatorios/qa_llm_report.html

Uso:
  python relatorio_consolidado.py
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent.parent / "relatorios"
PASTA.mkdir(exist_ok=True)
SAIDA = PASTA / "qa_llm_report.html"


# ── Parsers ──────────────────────────────────────────────────────────────────────

def parse_pytest_resultados(caminho: Path) -> dict:
    """Lê o JSON gerado pelo conftest.py ou suite_test_chat com todos os resultados."""
    caminho_suite = caminho.parent / "suite_test_chat_results.json"
    if not caminho.exists() and caminho_suite.exists():
        try:
            dados = json.loads(caminho_suite.read_text(encoding="utf-8"))
            casos = dados.get("casos", [])
            testes = [{
                "nome": c.get("codigo") + " - " + c.get("nome"),
                "passou": c.get("passou"),
                "duracao_s": c.get("latencia_s", 0),
                "erro": c.get("erro", "")
            } for c in casos]
            return {
                "disponivel": True,
                "arquivos": {
                    "suite_test_chat.py": {
                        "total": dados.get("total", 0),
                        "passou": dados.get("passou", 0),
                        "taxa_aprovacao": dados.get("taxa_aprovacao", 0),
                        "testes": testes
                    }
                },
                "total": dados.get("total", 0),
                "passou": dados.get("passou", 0),
                "taxa_aprovacao": dados.get("taxa_aprovacao", 0),
                "gerado_em": "",
            }
        except Exception:
            return {"disponivel": False}

    if not caminho.exists():
        return {"disponivel": False}
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except Exception:
        return {"disponivel": False}
    return {
        "disponivel": True,
        "arquivos": dados.get("arquivos", {}),
        "total": dados.get("total", 0),
        "passou": dados.get("passou", 0),
        "taxa_aprovacao": dados.get("taxa_aprovacao", 0),
        "gerado_em": dados.get("gerado_em", ""),
    }


def parse_deepeval_scores(caminho: Path) -> dict:
    """Lê o JSON do DeepEval e devolve um mapa nome_teste → métricas para enriquecer o relatório pytest."""
    if not caminho.exists():
        return {}
    try:
        itens = json.loads(caminho.read_text(encoding="utf-8"))
        return {item["name"]: item.get("metrics_data", []) for item in itens}
    except Exception:
        return {}


def parse_garak(caminho: Path) -> dict:
    if not caminho.exists():
        return {"disponivel": False, "probes": [], "total_falhas": 0, "total_testes": 0}

    probes: dict = {}
    total = falhas = 0

    with open(caminho) as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                entrada = json.loads(linha)
            except json.JSONDecodeError:
                continue

            probe = entrada.get("probe", entrada.get("probe_classname", "desconhecido"))
            status = entrada.get("status", "")
            passed = entrada.get("passed", None)

            probes.setdefault(probe, {"total": 0, "falhas": 0})
            probes[probe]["total"] += 1
            total += 1

            if passed is False or status in ("failed", "FAIL"):
                probes[probe]["falhas"] += 1
                falhas += 1

    lista = []
    for nome, dados in probes.items():
        taxa = round(dados["falhas"] / dados["total"] * 100) if dados["total"] else 0
        lista.append({
            "probe": nome,
            "total": dados["total"],
            "falhas": dados["falhas"],
            "taxa_falha": taxa,
            "status": "CRÍTICO" if taxa >= 50 else ("ALERTA" if taxa >= 20 else "OK"),
        })
    lista.sort(key=lambda x: x["taxa_falha"], reverse=True)

    return {
        "disponivel": True,
        "probes": lista,
        "total_falhas": falhas,
        "total_testes": total,
        "taxa_geral": round(falhas / total * 100) if total else 0,
    }


def parse_giskard(caminho: Path) -> dict:
    if not caminho.exists():
        return {"disponivel": False, "issues": [], "score": None}
    try:
        conteudo = caminho.read_text(encoding="utf-8")
    except Exception:
        return {"disponivel": False, "issues": [], "score": None}

    issues = re.findall(r'class="issue[^"]*"[^>]*>(.*?)</div>', conteudo, re.DOTALL)
    issues_limpas = [re.sub(r"<[^>]+>", "", i).strip() for i in issues if i.strip()]

    score_match = re.search(r"(\d+(?:\.\d+)?)\s*%?\s*(?:score|passed|aprovad)", conteudo, re.I)
    score = score_match.group(1) if score_match else None

    return {
        "disponivel": True,
        "issues": issues_limpas[:20],
        "score": score,
        "caminho_original": str(caminho),
    }


def parse_locust(caminho: Path) -> dict:
    if not caminho.exists():
        return {"disponivel": False}
    try:
        conteudo = caminho.read_text(encoding="utf-8")
    except Exception:
        return {"disponivel": False}

    # Locust embeds stats as JSON: window.templateArgs = {...}
    # Use position-based extraction to handle deeply nested JSON correctly
    marker = "window.templateArgs = "
    pos = conteudo.find(marker)
    if pos == -1:
        return {"disponivel": True, "disponivel_detalhe": False}

    try:
        json_start = conteudo.index("{", pos)
        decoder = json.JSONDecoder()
        args, _ = decoder.raw_decode(conteudo, json_start)

        # Locust 2.x usa "requests_statistics" com percentis como chaves diretas
        stats = args.get("requests_statistics", args.get("stats", []))

        agg = next((s for s in stats if s.get("name") == "Aggregated"), None)
        if not agg and stats:
            agg = stats[-1]
        if not agg:
            return {"disponivel": True, "disponivel_detalhe": False}

        total_req = agg.get("num_requests", 0)
        total_fail = agg.get("num_failures", 0)
        median = agg.get("median_response_time", 0)
        p95 = (
            agg.get("response_time_percentile_0.95")
            or agg.get("response_times", {}).get("95", 0)
            or 0
        )
        p99 = (
            agg.get("response_time_percentile_0.99")
            or agg.get("response_times", {}).get("99", 0)
            or 0
        )
        rps = round(agg.get("total_rps") or agg.get("current_rps", 0), 2)
        taxa_falha = round(total_fail / total_req * 100, 1) if total_req else 0

        if p95 > 10000 or taxa_falha > 5:
            status = "CRÍTICO"
        elif p95 > 5000 or taxa_falha > 1:
            status = "ALERTA"
        else:
            status = "OK"

        endpoints = [s for s in stats if s.get("name") not in ("Aggregated", "")]

        return {
            "disponivel": True,
            "disponivel_detalhe": True,
            "total_req": total_req,
            "total_fail": total_fail,
            "taxa_falha": taxa_falha,
            "median_ms": median,
            "p95_ms": p95,
            "p99_ms": p99,
            "rps": rps,
            "status": status,
            "endpoints": endpoints,
            "caminho_original": str(caminho),
        }
    except Exception:
        return {"disponivel": True, "disponivel_detalhe": False}


# ── Design helpers ───────────────────────────────────────────────────────────────

def _cor(valor: float) -> str:
    if valor >= 80: return "#16a34a"
    if valor >= 60: return "#d97706"
    return "#dc2626"

def _nivel(valor: float) -> tuple:
    if valor >= 80: return ("BOM",      "#16a34a", "#dcfce7", "#14532d")
    if valor >= 60: return ("ATENÇÃO",  "#d97706", "#fef9c3", "#713f12")
    return              ("CRÍTICO",  "#dc2626", "#fee2e2", "#7f1d1d")

def _donut(pct: int, cor: str, size: int = 88) -> str:
    p = max(0, min(100, pct))
    return (
        f'<svg viewBox="0 0 36 36" width="{size}" height="{size}">'
        f'<circle cx="18" cy="18" r="15.9155" fill="none" stroke="#e2e8f0" stroke-width="3.8"/>'
        f'<circle cx="18" cy="18" r="15.9155" fill="none" stroke="{cor}" stroke-width="3.8" '
        f'stroke-dasharray="{p} 100" stroke-linecap="round" transform="rotate(-90 18 18)"/>'
        f'<text x="18" y="19.5" text-anchor="middle" font-size="7.5" font-weight="700" '
        f'fill="{cor}" font-family="system-ui,sans-serif">{p}%</text>'
        f'</svg>'
    )

def _badge(status: str) -> str:
    m = {
        "CRÍTICO": ("#fee2e2", "#991b1b"),
        "ALERTA":  ("#fef9c3", "#92400e"),
        "OK":      ("#dcfce7", "#14532d"),
        "PASS":    ("#dcfce7", "#14532d"),
        "FAIL":    ("#fee2e2", "#991b1b"),
        "INFO":    ("#dbeafe", "#1e3a8a"),
    }
    bg, col = m.get(status, ("#f1f5f9", "#475569"))
    return (f'<span style="display:inline-block;padding:2px 9px;border-radius:99px;'
            f'font-size:11px;font-weight:600;letter-spacing:.3px;'
            f'background:{bg};color:{col}">{status}</span>')

def _bar(pct: int, cor: str) -> str:
    p = max(0, min(100, pct))
    return (f'<div style="background:#e2e8f0;border-radius:4px;height:5px;margin-top:5px">'
            f'<div style="width:{p}%;background:{cor};height:5px;border-radius:4px"></div></div>')

def _card_unavailable(titulo: str, arquivo: str) -> str:
    return (
        f'<section class="card" style="opacity:.55">'
        f'<div class="card-header"><h2 class="card-title">{titulo}</h2></div>'
        f'<p style="font-size:13px;color:#64748b;margin-top:4px">'
        f'Relatório não encontrado: <code style="background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:12px">{arquivo}</code></p>'
        f'<p style="font-size:12px;color:#94a3b8;margin-top:6px">Execute a ferramenta e rode novamente este script.</p>'
        f'</section>'
    )

ARQUIVO_LABELS = {
    "test_deepeval.py":            ("Qualidade Básica",    "#8b5cf6"),
    "test_qualidade_avancada.py":  ("Qualidade Avançada",  "#3b82f6"),
    "test_consistencia.py":        ("Consistência",        "#0891b2"),
    "test_multiturn.py":           ("Multi-turn & Ataques","#dc2626"),
    "test_entrada.py":             ("Robustez de Entrada", "#64748b"),
}


# ── Detecção automática de alertas ───────────────────────────────────────────────

def _detectar_alertas(pytest_res, garak, giskard, locust):
    alertas = []
    CRITICOS = ["injection", "system_prompt", "vazou", "consistencia_resistencia", "derrapagem"]
    ALERTAS  = ["contradicao", "multiturn", "alucinacao", "hallucination", "inventa"]

    if pytest_res.get("disponivel"):
        for arq, info in pytest_res["arquivos"].items():
            label = ARQUIVO_LABELS.get(arq, ("", "#64748b"))[0]
            for t in info["testes"]:
                if not t["passou"]:
                    low = t["nome"].lower()
                    if any(k in low for k in CRITICOS):
                        nivel = "CRÍTICO"
                    elif any(k in low for k in ALERTAS):
                        nivel = "ALERTA"
                    else:
                        continue
                    msg = t["nome"].replace("test_", "").replace("_", " ").title()
                    det = f"Score {t['score']} · Threshold {t['threshold']}" if t.get("score") is not None else ""
                    alertas.append({"nivel": nivel, "fonte": label, "msg": msg, "det": det})

    if locust.get("disponivel_detalhe"):
        if locust["taxa_falha"] > 5:
            alertas.append({"nivel": "CRÍTICO", "fonte": "Locust",
                "msg": f"Taxa de falha de {locust['taxa_falha']}% sob carga simultânea",
                "det": f"{locust['total_fail']} de {locust['total_req']} requisições falharam"})
        elif locust["taxa_falha"] > 1:
            alertas.append({"nivel": "ALERTA", "fonte": "Locust",
                "msg": f"Taxa de falha {locust['taxa_falha']}%", "det": ""})
        p95s = locust["p95_ms"]
        if p95s > 30000:
            alertas.append({"nivel": "CRÍTICO", "fonte": "Locust",
                "msg": f"Latência p95 = {p95s/1000:.0f}s — inaceitável para produção",
                "det": "Usuários aguardam mais de 30 s por resposta"})
        elif p95s > 10000:
            alertas.append({"nivel": "ALERTA", "fonte": "Locust",
                "msg": f"Latência p95 = {p95s/1000:.0f}s", "det": ""})

    if garak.get("disponivel"):
        for p in garak["probes"]:
            if p["taxa_falha"] >= 30:
                nivel = "CRÍTICO" if p["taxa_falha"] >= 50 else "ALERTA"
                alertas.append({"nivel": nivel, "fonte": f"Garak · {p['probe']}",
                    "msg": f"{p['taxa_falha']}% dos ataques comprometeram o modelo",
                    "det": f"{p['falhas']} de {p['total']} tentativas"})

    if giskard.get("disponivel") and giskard.get("issues"):
        n = len(giskard["issues"])
        det = giskard["issues"][0][:100] if giskard["issues"] else ""
        alertas.append({"nivel": "ALERTA", "fonte": "Giskard",
            "msg": f"{n} issue{'s' if n > 1 else ''} detectada{'s' if n > 1 else ''} no scan automático",
            "det": det})

    return alertas


# ── Gerador de HTML ──────────────────────────────────────────────────────────────

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0 }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
  background: #f1f5f9;
  color: #0f172a;
  font-size: 14px;
  line-height: 1.5;
}
a { color: #2563eb; text-decoration: none }
a:hover { text-decoration: underline }
code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: .875em;
  background: #f1f5f9;
  padding: 1px 6px;
  border-radius: 4px;
}

/* Layout */
.wrapper { max-width: 960px; margin: 0 auto; padding: 2rem 1.5rem }

/* Header */
.report-header {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #fff;
  padding: 1.75rem 2rem;
  border-radius: 16px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}
.report-header h1 { font-size: 20px; font-weight: 600; color: #f8fafc }
.report-header .meta { font-size: 12px; color: #94a3b8; margin-top: 4px }
.score-pill {
  text-align: center;
  background: rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 12px;
  padding: 12px 20px;
  min-width: 110px;
  flex-shrink: 0;
}
.score-pill .score-num { font-size: 38px; font-weight: 700; line-height: 1 }
.score-pill .score-lbl { font-size: 11px; color: #94a3b8; margin-top: 4px; letter-spacing: .4px }

/* Overview cards */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
  margin-bottom: 1.5rem;
}
.ov-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 14px;
}
.ov-card .ov-label { font-size: 12px; color: #64748b; font-weight: 500 }
.ov-card .ov-sub   { font-size: 11px; color: #94a3b8; margin-top: 2px }

/* Alertas */
.alerts-section { margin-bottom: 1.5rem }
.alerts-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .7px;
  color: #64748b;
  margin-bottom: 8px;
}
.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 8px;
  border-left: 3px solid;
}
.alert-critico { background: #fff1f2; border-color: #dc2626 }
.alert-alerta  { background: #fffbeb; border-color: #f59e0b }
.alert-fonte {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .5px;
  white-space: nowrap;
}
.alert-msg  { font-size: 13px; font-weight: 500 }
.alert-det  { font-size: 12px; color: #64748b; margin-top: 2px }

/* Section card */
.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 1.25rem;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
}
.card-title { font-size: 15px; font-weight: 600; color: #0f172a }
.card-sub   { font-size: 12px; color: #64748b; margin-top: 3px }

/* File accordion */
.file-group {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  margin-bottom: 10px;
  overflow: hidden;
}
.file-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.file-pill {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-right: 8px;
  flex-shrink: 0;
}
.file-name  { font-size: 13px; font-weight: 600; color: #1e293b }
.file-ratio { font-size: 12px; color: #64748b }
.file-pct   { font-size: 14px; font-weight: 700; margin-left: 10px }

/* Test row */
.test-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 9px 14px;
  border-bottom: 1px solid #f8fafc;
}
.test-row:last-child { border-bottom: none }
.test-name  { font-size: 12.5px; font-family: monospace; color: #1e293b; word-break: break-all }
.test-score { font-size: 11px; color: #dc2626; margin-top: 2px }
.test-meta  { font-size: 11px; color: #94a3b8; margin-top: 2px; font-style: italic }
.test-metrics { margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px }
.metric-chip {
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 99px;
  background: #f1f5f9;
  color: #64748b;
}
.metric-chip.pass { background: #dcfce7; color: #15803d }
.metric-chip.fail { background: #fee2e2; color: #b91c1c }
.test-dur { font-size: 11px; color: #94a3b8; white-space: nowrap; margin-left: auto }

/* Stats grid */
.stats-grid {
  display: grid;
  gap: 10px;
  margin-bottom: 1.25rem;
}
.stats-grid-3 { grid-template-columns: repeat(3, 1fr) }
.stats-grid-4 { grid-template-columns: repeat(4, 1fr) }
.stats-grid-5 { grid-template-columns: repeat(5, 1fr) }
.stat-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 12px 14px;
}
.stat-box .stat-lbl { font-size: 11px; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: .4px }
.stat-box .stat-val { font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px }

/* Table */
.data-table { width: 100%; border-collapse: collapse }
.data-table th {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: .5px;
  padding: 0 8px 10px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
.data-table td {
  padding: 10px 8px;
  font-size: 13px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none }

/* Giskard issues */
.issue-list { list-style: none; padding: 0 }
.issue-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 13px;
  color: #334155;
}
.issue-item:last-child { border-bottom: none }
.issue-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #f59e0b;
  margin-top: 5px;
  flex-shrink: 0;
}

/* Footer */
.report-footer {
  text-align: center;
  font-size: 11px;
  color: #94a3b8;
  padding: 1.5rem 0 .5rem;
  border-top: 1px solid #e2e8f0;
  margin-top: 1rem;
}

/* Print */
@media print {
  body { background: white }
  .card, .file-group { break-inside: avoid }
}
"""


def gerar_html(pytest_res: dict, scores_deepeval: dict, garak: dict, giskard: dict, locust: dict) -> str:
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    alertas = _detectar_alertas(pytest_res, garak, giskard, locust)

    # ── Score geral ──────────────────────────────────────────────────────────────
    scores = []
    if pytest_res.get("disponivel") and pytest_res.get("total", 0) > 0:
        scores.append(("Testes",    pytest_res["taxa_aprovacao"], 0.40))
    if garak.get("disponivel"):
        scores.append(("Segurança", 100 - garak["taxa_geral"],    0.35))
    if giskard.get("disponivel"):
        val_giskard = 100
        if giskard.get("score"):
            try: val_giskard = float(giskard["score"])
            except: pass
        else:
            n_issues = len(giskard.get("issues", []))
            val_giskard = max(0, 100 - n_issues * 15)
        scores.append(("Risco", val_giskard, 0.15))
    if locust.get("disponivel_detalhe"):
        ls = 100 if locust["p95_ms"] < 3000 else (75 if locust["p95_ms"] < 5000 else (50 if locust["p95_ms"] < 10000 else 25))
        scores.append(("Latência", ls, 0.10))

    peso_total  = sum(p for _, _, p in scores) or 1
    score_geral = round(sum(v * p for _, v, p in scores) / peso_total) if scores else 0
    cor_g       = _cor(score_geral)
    nivel_txt, nivel_cor, nivel_bg, nivel_tcor = _nivel(score_geral)

    # ── Header ───────────────────────────────────────────────────────────────────
    html_header = f"""
    <header class="report-header">
      <div>
        <h1>Relatório QA — Assistente LLM Fluentes</h1>
        <p class="meta">Gerado em {agora} &nbsp;·&nbsp; Modelo: llama3.2 via Ollama &nbsp;·&nbsp; Framework: DeepEval, Giskard, Garak, Locust</p>
      </div>
      <div class="score-pill">
        <div class="score-num" style="color:{cor_g}">{score_geral}</div>
        <div style="font-size:12px;color:#94a3b8;margin-top:2px">/100</div>
        <div style="margin-top:8px">
          <span style="background:{nivel_bg};color:{nivel_tcor};font-size:11px;font-weight:700;
            padding:3px 10px;border-radius:99px;letter-spacing:.4px">{nivel_txt}</span>
        </div>
        <div class="score-lbl">Score Geral</div>
      </div>
    </header>"""

    # ── Overview donuts ──────────────────────────────────────────────────────────
    ov_items = ""
    for nome, valor, peso in scores:
        cor_ov = _cor(valor)
        ov_items += f"""
        <div class="ov-card">
          {_donut(round(valor), cor_ov, 68)}
          <div>
            <div class="ov-label">{nome}</div>
            <div class="ov-sub">Peso: {round(peso*100)}%</div>
          </div>
        </div>"""

    # Placeholder para dimensões sem dados
    for nome, label_nd in [("Segurança", "Garak"), ("Risco", "Giskard")]:
        if not any(n == nome for n, *_ in scores):
            ov_items += f"""
            <div class="ov-card" style="opacity:.45">
              {_donut(0, "#cbd5e1", 68)}
              <div>
                <div class="ov-label">{nome}</div>
                <div class="ov-sub">{label_nd} não executado</div>
              </div>
            </div>"""

    html_overview = f'<div class="overview-grid">{ov_items}</div>'

    # ── Alertas ──────────────────────────────────────────────────────────────────
    if alertas:
        n_crit = sum(1 for a in alertas if a["nivel"] == "CRÍTICO")
        n_ale  = sum(1 for a in alertas if a["nivel"] == "ALERTA")
        resumo = f"{n_crit} crítico{'s' if n_crit != 1 else ''}" if n_crit else ""
        if n_ale:
            resumo += (" · " if resumo else "") + f"{n_ale} alerta{'s' if n_ale != 1 else ''}"

        itens_alert = ""
        for a in alertas:
            cls  = "alert-critico" if a["nivel"] == "CRÍTICO" else "alert-alerta"
            cor_fonte = "#dc2626" if a["nivel"] == "CRÍTICO" else "#d97706"
            det_html = f'<div class="alert-det">{a["det"]}</div>' if a.get("det") else ""
            itens_alert += f"""
            <div class="alert-item {cls}">
              <div style="flex:1">
                <span class="alert-fonte" style="color:{cor_fonte}">{a['fonte']}</span>
                <div class="alert-msg">{a['msg']}</div>
                {det_html}
              </div>
              {_badge(a['nivel'])}
            </div>"""

        html_alertas = f"""
        <div class="alerts-section">
          <div class="alerts-title">Achados que requerem atenção — {resumo}</div>
          {itens_alert}
        </div>"""
    else:
        html_alertas = ""

    # ── Seção Testes Pytest ──────────────────────────────────────────────────────
    if pytest_res.get("disponivel") and pytest_res.get("arquivos"):
        taxa_geral = pytest_res["taxa_aprovacao"]
        cor_taxa   = _cor(taxa_geral)

        grupos = ""
        for arq, info in pytest_res["arquivos"].items():
            label, cor_arq = ARQUIVO_LABELS.get(arq, (arq, "#64748b"))
            taxa_arq = info["taxa_aprovacao"]
            cor_t    = _cor(taxa_arq)

            linhas = ""
            for t in info["testes"]:
                passou = t["passou"]
                badge_st = _badge("PASS" if passou else "FAIL")

                score_line = ""
                if not passou and t.get("score") is not None:
                    score_line = f'<div class="test-score">Score {t["score"]} · Threshold {t["threshold"]}</div>'

                chips = ""
                for m in scores_deepeval.get(t["nome"], []):
                    cls = "pass" if m.get("passed") else "fail"
                    chips += f'<span class="metric-chip {cls}">{m["name"]}: {m["score"]}</span>'
                chips_html = f'<div class="test-metrics">{chips}</div>' if chips else ""

                erro_html = ""
                if t.get("erro"):
                    txt = t["erro"][:160] + ("…" if len(t["erro"]) > 160 else "")
                    erro_html = f'<div class="test-meta">{txt}</div>'

                linhas += f"""
                <div class="test-row">
                  <div style="padding-top:1px;flex-shrink:0">{badge_st}</div>
                  <div style="flex:1;min-width:0">
                    <div class="test-name">{t['nome']}</div>
                    {score_line}{chips_html}{erro_html}
                  </div>
                  <div class="test-dur">{t['duracao_s']}s</div>
                </div>"""

            grupos += f"""
            <div class="file-group">
              <div class="file-header">
                <div style="display:flex;align-items:center">
                  <span class="file-pill" style="background:{cor_arq}"></span>
                  <span class="file-name">{label}</span>
                  <code style="font-size:11px;color:#64748b;margin-left:8px">{arq}</code>
                </div>
                <div style="display:flex;align-items:center;gap:6px">
                  <span class="file-ratio">{info['passou']}/{info['total']}</span>
                  <span class="file-pct" style="color:{cor_t}">{taxa_arq}%</span>
                </div>
              </div>
              {linhas}
            </div>"""

        html_pytest = f"""
        <section class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Testes Automatizados</div>
              <div class="card-sub">DeepEval · Consistência · Multi-turn · Robustez de entrada</div>
            </div>
            <div style="display:flex;align-items:center;gap:14px">
              {_donut(taxa_geral, cor_taxa, 72)}
              <div style="text-align:right">
                <div style="font-size:28px;font-weight:700;color:{cor_taxa}">{taxa_geral}%</div>
                <div style="font-size:11px;color:#64748b">{pytest_res['passou']}/{pytest_res['total']} passaram</div>
              </div>
            </div>
          </div>
          {grupos}
        </section>"""
    else:
        html_pytest = _card_unavailable("Testes Automatizados", "relatorios/pytest_all_results.json")

    # ── Seção Garak ──────────────────────────────────────────────────────────────
    if garak["disponivel"]:
        cor_gk = _cor(100 - garak["taxa_geral"])
        linhas_probe = ""
        for p in garak["probes"]:
            cor_b = "#dc2626" if p["taxa_falha"] >= 50 else ("#f59e0b" if p["taxa_falha"] >= 20 else "#16a34a")
            linhas_probe += f"""
            <tr>
              <td><code>{p['probe']}</code></td>
              <td style="text-align:center">{p['total']}</td>
              <td style="text-align:center;color:#dc2626;font-weight:600">{p['falhas']}</td>
              <td style="min-width:140px">
                {_bar(p['taxa_falha'], cor_b)}
                <span style="font-size:11px;color:#64748b">{p['taxa_falha']}% comprometido</span>
              </td>
              <td>{_badge(p['status'])}</td>
            </tr>"""

        res  = garak["total_testes"] - garak["total_falhas"]
        html_garak = f"""
        <section class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Garak — Red Teaming</div>
              <div class="card-sub">Jailbreak, prompt injection e toxicidade em massa</div>
            </div>
            <div style="display:flex;align-items:center;gap:14px">
              {_donut(100 - garak['taxa_geral'], cor_gk, 72)}
              <div style="text-align:right">
                <div style="font-size:28px;font-weight:700;color:{cor_gk}">{100 - garak['taxa_geral']}%</div>
                <div style="font-size:11px;color:#64748b">resistência geral</div>
              </div>
            </div>
          </div>
          <div class="stats-grid stats-grid-3" style="margin-bottom:1.25rem">
            <div class="stat-box">
              <div class="stat-lbl">Total de ataques</div>
              <div class="stat-val">{garak['total_testes']}</div>
            </div>
            <div class="stat-box" style="border-color:#fecaca">
              <div class="stat-lbl" style="color:#dc2626">Modelo enganado</div>
              <div class="stat-val" style="color:#dc2626">{garak['total_falhas']}</div>
            </div>
            <div class="stat-box" style="border-color:#bbf7d0">
              <div class="stat-lbl" style="color:#16a34a">Resistiu</div>
              <div class="stat-val" style="color:#16a34a">{res}</div>
            </div>
          </div>
          <table class="data-table">
            <thead><tr>
              <th>Probe</th>
              <th style="text-align:center">Total</th>
              <th style="text-align:center">Falhas</th>
              <th>Taxa de comprometimento</th>
              <th>Status</th>
            </tr></thead>
            <tbody>{linhas_probe}</tbody>
          </table>
        </section>"""
    else:
        html_garak = _card_unavailable("Garak — Red Teaming", "relatorios/garak.report.jsonl")

    # ── Seção Giskard ────────────────────────────────────────────────────────────
    if giskard["disponivel"]:
        issues_list = giskard["issues"] or ["Nenhuma issue textual extraída — veja o relatório original."]
        itens_issue = "".join(
            f'<li class="issue-item"><span class="issue-dot"></span><span>{i}</span></li>'
            for i in issues_list
        )
        n_issues = len(giskard["issues"]) if giskard["issues"] else 0
        cor_gs  = "#dc2626" if n_issues >= 5 else ("#f59e0b" if n_issues >= 1 else "#16a34a")
        det_gs  = f"{n_issues} issue{'s' if n_issues != 1 else ''} detectada{'s' if n_issues != 1 else ''}"

        html_giskard = f"""
        <section class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Giskard — Scan de Risco</div>
              <div class="card-sub">Bias, robustez e vulnerabilidades automáticas</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:28px;font-weight:700;color:{cor_gs}">{n_issues}</div>
              <div style="font-size:11px;color:#64748b">{det_gs}</div>
            </div>
          </div>
          <ul class="issue-list">{itens_issue}</ul>
          <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid #f1f5f9">
            <a href="{giskard['caminho_original']}">Abrir relatório completo do Giskard →</a>
          </div>
        </section>"""
    else:
        html_giskard = _card_unavailable("Giskard — Scan de Risco", "relatorios/giskard_scan.html")

    # ── Seção Locust ─────────────────────────────────────────────────────────────
    if locust.get("disponivel") and locust.get("disponivel_detalhe"):
        cor_loc = _cor(100 - locust["taxa_falha"] * 2)
        status_loc = locust["status"]

        def _ms(v):
            if not v: return "—"
            return f"{v/1000:.1f}s" if v >= 1000 else f"{v:,.0f} ms"

        linhas_ep = ""
        for ep in locust.get("endpoints", []):
            p95_ep  = ep.get("response_time_percentile_0.95") or ep.get("response_times", {}).get("95", 0) or 0
            med_ep  = ep.get("median_response_time", 0)
            fail_ep = ep.get("num_failures", 0)
            req_ep  = ep.get("num_requests", 0)
            cor_ep  = "#dc2626" if p95_ep > 10000 else ("#d97706" if p95_ep > 5000 else "#0f172a")
            taxa_ep = round(fail_ep / req_ep * 100, 1) if req_ep else 0
            linhas_ep += f"""
            <tr>
              <td><code>{ep.get('method','')}&nbsp;{ep.get('name','')}</code></td>
              <td style="text-align:center">{req_ep}</td>
              <td style="text-align:center">{_ms(med_ep)}</td>
              <td style="text-align:center;font-weight:600;color:{cor_ep}">{_ms(p95_ep)}</td>
              <td style="text-align:center;color:{'#dc2626' if fail_ep > 0 else '#64748b'}">{fail_ep} ({taxa_ep}%)</td>
            </tr>"""

        tabela_ep = f"""
        <table class="data-table" style="margin-top:1.25rem">
          <thead><tr>
            <th>Endpoint</th>
            <th style="text-align:center">Req.</th>
            <th style="text-align:center">Mediana</th>
            <th style="text-align:center">p95</th>
            <th style="text-align:center">Falhas</th>
          </tr></thead>
          <tbody>{linhas_ep}</tbody>
        </table>""" if linhas_ep else ""

        p95_display = locust["p95_ms"]
        cor_p95 = _cor(100 - (0 if p95_display < 3000 else (25 if p95_display < 5000 else (50 if p95_display < 10000 else 75))))

        html_locust = f"""
        <section class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Locust — Carga &amp; Latência</div>
              <div class="card-sub">Throughput, latência p95/p99 e taxa de falha sob carga simultânea</div>
            </div>
            {_badge(status_loc)}
          </div>
          <div class="stats-grid stats-grid-5">
            <div class="stat-box">
              <div class="stat-lbl">Requisições</div>
              <div class="stat-val">{locust['total_req']}</div>
            </div>
            <div class="stat-box">
              <div class="stat-lbl">Mediana</div>
              <div class="stat-val" style="font-size:18px">{_ms(locust['median_ms'])}</div>
            </div>
            <div class="stat-box" style="border-color:{'#fecaca' if p95_display > 10000 else ('#fde68a' if p95_display > 5000 else '#e2e8f0')}">
              <div class="stat-lbl" style="color:{cor_p95}">p95</div>
              <div class="stat-val" style="color:{cor_p95};font-size:18px">{_ms(p95_display)}</div>
            </div>
            <div class="stat-box">
              <div class="stat-lbl">p99</div>
              <div class="stat-val" style="font-size:18px">{_ms(locust['p99_ms'])}</div>
            </div>
            <div class="stat-box" style="border-color:{'#fecaca' if locust['taxa_falha'] > 1 else '#e2e8f0'}">
              <div class="stat-lbl" style="color:{'#dc2626' if locust['taxa_falha'] > 1 else '#64748b'}">Falhas</div>
              <div class="stat-val" style="color:{'#dc2626' if locust['taxa_falha'] > 1 else '#0f172a'}">{locust['taxa_falha']}%</div>
            </div>
          </div>
          {tabela_ep}
          <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid #f1f5f9">
            <a href="{locust['caminho_original']}">Abrir relatório completo do Locust →</a>
          </div>
        </section>"""
    elif locust.get("disponivel"):
        html_locust = _card_unavailable("Locust — Carga & Latência", "relatorios/locust_report.html (formato não reconhecido)")
    else:
        html_locust = _card_unavailable("Locust — Carga & Latência", "relatorios/locust_report.html")

    # ── Metodologia ──────────────────────────────────────────────────────────────
    html_met = """
    <section class="card" style="margin-bottom:0">
      <div class="card-header" style="margin-bottom:.75rem;padding-bottom:.75rem">
        <div class="card-title">Metodologia &amp; Ponderação</div>
      </div>
      <table class="data-table">
        <thead><tr>
          <th>Dimensão</th><th>Peso</th><th>Ferramenta</th><th>O que avalia</th>
        </tr></thead>
        <tbody>
          <tr><td><strong>Testes</strong></td><td>40%</td><td>DeepEval + pytest</td><td>Qualidade, segurança, consistência e robustez</td></tr>
          <tr><td><strong>Segurança</strong></td><td>35%</td><td>Garak</td><td>Resistência a jailbreak, injection e toxicidade em massa</td></tr>
          <tr><td><strong>Risco</strong></td><td>15%</td><td>Giskard</td><td>Bias, robustez e vulnerabilidades automáticas</td></tr>
          <tr><td><strong>Latência</strong></td><td>10%</td><td>Locust</td><td>Desempenho sob carga: p95 &lt; 3 s = 100, &lt; 5 s = 75, &lt; 10 s = 50, ≥ 10 s = 25</td></tr>
        </tbody>
      </table>
    </section>"""

    # ── Montagem final ────────────────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>QA Report — Assistente Fluentes — {agora}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="wrapper">
  {html_header}
  {html_overview}
  {html_alertas}
  {html_pytest}
  {html_garak}
  {html_giskard}
  {html_locust}
  {html_met}
  <footer class="report-footer">
    Gerado por <code>relatorio_consolidado.py</code> &nbsp;·&nbsp; {agora}
    &nbsp;·&nbsp; Fluentes — Escola de Inglês
  </footer>
</div>
</body>
</html>"""


# ── Main ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("📊 Consolidando relatórios...\n")

    pytest_res      = parse_pytest_resultados(PASTA / "pytest_all_results.json")
    scores_deepeval = parse_deepeval_scores(PASTA / "deepeval_results.json")

    # Busca dinâmica por logs do Garak com prefixos customizados
    caminho_garak = PASTA / "garak.report.jsonl"
    for p in PASTA.glob("*garak*.report.jsonl"):
        caminho_garak = p
        break
    garak           = parse_garak(caminho_garak)

    giskard         = parse_giskard(PASTA / "giskard_scan.html")
    locust          = parse_locust(PASTA / "locust_report.html")

    print(f"  Pytest (todos):  {'✅ encontrado' if pytest_res['disponivel'] else '⚠️  não encontrado'}")
    print(f"  DeepEval scores: {'✅ encontrado' if scores_deepeval else '⚠️  não encontrado'}")
    print(f"  Garak:           {'✅ encontrado' if garak['disponivel'] else '⚠️  não encontrado'}")
    print(f"  Giskard:         {'✅ encontrado' if giskard['disponivel'] else '⚠️  não encontrado'}")
    print(f"  Locust:          {'✅ encontrado' if locust.get('disponivel_detalhe') else '⚠️  não encontrado'}")

    html = gerar_html(pytest_res, scores_deepeval, garak, giskard, locust)
    SAIDA.write_text(html, encoding="utf-8")

    print(f"\n✅ Relatório consolidado: {SAIDA}")
    print("   Abra no browser para visualizar.")
