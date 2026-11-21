#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Agente Supervisor / Fiscal (zambria.github.io)

Monitora o site online periodicamente e detecta:
- posts ausentes (esperados/local mas no fora do ar, ou cadence abaixo do esperado)
- posts duplicados (mesmo slug mais de uma vez no índice online)
- botão da sidebar não funcionando (markup + JS de toggle)
- CSS não carregado (style.css fora do ar ou vazio/sem assinatura ZAMBRIA)

Conhece o tom editorial ZAMBRIA, a estrutura de pastas (drafts, review,
posts, publicados) e o limite de 2 posts por dia.

Execução única (padrão):   python supervisor.py
Modo contínuo:             python supervisor.py --loop --interval 3600
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# --------------------------- configuração ---------------------------
SITE_URL = "https://zambria.github.io"
CSS_URL = SITE_URL + "/style.css"
REPO = Path(__file__).resolve().parent
POSTS_DIR = REPO / "posts"
DRAFTS_DIR = REPO / "drafts"
REVIEW_DIR = REPO / "review"
PUBLICADOS_DIR = REPO / "publicados"
INDEX_FILE = REPO / "index.html"
ESTADO_FILE = REPO / "estado-publicador.json"
TOPICS_FILE = REPO / "topics.json"
REPORT_FILE = REPO / "supervisor_report.json"

POSTS_POR_DIA = 2
TIMEOUT = 20

# Assinaturas que confirmam que o CSS baixado é realmente o do ZAMBRIA.
CSS_ASSINATURAS = [".site-shell", "--bg", "--accent", ".sidebar", ".conteudo"]

# Assinatura do tom editorial ZAMBRIA (referência, usada nos relatórios).
TOM_EDITORIAL = "sério, sombrio, adulto formal, sarcástico às vezes"


def log(msg):
    print(f"[supervisor] {msg}", flush=True)


def http_get(url):
    """GET simples. Retorna (status, bytes) ou (None, None) em falha de rede."""
    try:
        req = Request(url, headers={"User-Agent": "ZAMBRIA-Supervisor/1.0"})
        with urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except (HTTPError, URLError, OSError) as exc:
        log(f"falha ao acessar {url}: {exc}")
        return None, None


def agora_iso():
    return datetime.now().isoformat(timespec="seconds")


# --------------------------- verificações ---------------------------

def checar_css():
    """Verifica se o style.css carrega online com conteúdo de verdade."""
    status, conteudo = http_get(CSS_URL)
    problema = None
    evidencia = None
    if status is None:
        problema = "style.css não respondeu (fora do ar ou sem rede)."
        evidencia = f"GET {CSS_URL} -> sem resposta"
    elif status != 200:
        problema = f"style.css retornou HTTP {status}."
        evidencia = f"GET {CSS_URL} -> HTTP {status}"
    else:
        assert conteudo is not None
        texto = conteudo.decode("utf-8", errors="replace")
        evidencia = f"GET {CSS_URL} -> HTTP 200, {len(conteudo)} bytes"
        if len(conteudo) == 0:
            problema = "style.css está vazio (0 bytes)."
        elif not any(assinatura in texto for assinatura in CSS_ASSINATURAS):
            problema = "style.css carrega, mas não tem assinatura ZAMBRIA (pode ser outro arquivo)."
            evidencia += f" | amostra: {texto[:80]!r}"
    return {
        "nome": "CSS carregado",
        "ok": problema is None,
        "problema": problema,
        "evidencia": evidencia,
        "sugere_correcao": (
            "Reenviar style.css para o repositório e fazer push para o GitHub Pages."
            if problema and "vazio" in (problema or "")
            else ("Verificar conexão e o arquivo style.css no branch publicado."
                  if problema else None)
        ),
    }


def extrair_links_posts(html):
    """Retorna lista de slugs de posts (posts/<slug>.html) encontrados no HTML."""
    return re.findall(r'href="posts/([^"/]+?)\.html"', html)


def checar_posts():
    """Compara posts online vs locais; detecta duplicados e ausentes."""
    status, conteudo = http_get(SITE_URL)
    resultado = {
        "nome": "Posts ausentes / duplicados",
        "ok": True,
        "problema": None,
        "evidencia": None,
        "sugere_correcao": None,
        "detalhes": {},
    }
    if status is None or conteudo is None:
        resultado["ok"] = False
        resultado["problema"] = "Não foi possível acessar o índice online."
        resultado["evidencia"] = f"GET {SITE_URL} -> sem resposta"
        return resultado

    html = conteudo.decode("utf-8", errors="replace")
    posts_online = extrair_links_posts(html)

    # placeholder "vazio" ainda visível quando já há posts (índice não limpo)
    tem_placeholder_vazio = '<div class="vazio">' in html
    placeholder_indevido = tem_placeholder_vazio and len(posts_online) > 0

    # posts locais (fonte da verdade do que já deveria estar no ar)
    posts_locais = sorted(p.stem for p in POSTS_DIR.glob("*.html")) if POSTS_DIR.exists() else []

    # duplicados online
    contagem = {}
    for slug in posts_online:
        contagem[slug] = contagem.get(slug, 0) + 1
    duplicados = [s for s, c in contagem.items() if c > 1]

    # ausentes online: existem localmente mas não aparecem no índice online
    ausentes_online = [s for s in posts_locais if s not in posts_online]

    # presentes online mas inexistentes localmente (desvio de deploy)
    extras_online = [s for s in posts_online if s not in posts_locais]

    resultado["detalhes"] = {
        "posts_online": posts_online,
        "posts_locais": posts_locais,
        "duplicados": duplicados,
        "ausentes_online": ausentes_online,
        "extras_online": extras_online,
        "total_online": len(posts_online),
        "total_locais": len(posts_locais),
    }

    problemas = []
    if duplicados:
        problemas.append(f"posts duplicados online: {duplicados}")
    if ausentes_online:
        problemas.append(f"posts ausentes online (existem localmente, não no índice): {ausentes_online}")
    if extras_online:
        problemas.append(f"posts online sem correspondente local: {extras_online}")
    if placeholder_indevido:
        problemas.append(
            "placeholder 'Nenhum post publicado ainda' visível apesar de já haver post(s) publicado(s)"
        )

    if problemas:
        resultado["ok"] = False
        resultado["problema"] = "; ".join(problemas)
        resultado["evidencia"] = f"online={posts_online}, local={posts_locais}"
        resultado["sugere_correcao"] = (
            "Remover entradas duplicadas do index.html, apagar o bloco <div class=\"vazio\"> quando houver posts, "
            "reenviar os posts faltantes e garantir que o publicador injete cada post uma única vez."
        )
    else:
        resultado["evidencia"] = (
            f"{len(posts_online)} post(s) online, {len(posts_locais)} local(is), sem duplicados nem ausentes."
        )
    resultado["detalhes"] = {
        "posts_online": posts_online,
        "posts_locais": posts_locais,
        "duplicados": duplicados,
        "ausentes_online": ausentes_online,
        "extras_online": extras_online,
        "placeholder_vazio_visivel": tem_placeholder_vazio,
        "total_online": len(posts_online),
        "total_locais": len(posts_locais),
    }
    return resultado


def checar_limite_diario():
    """Verifica o controle de 2 posts/dia no estado-publicador.json."""
    problema = None
    evidencias = {}
    if ESTADO_FILE.exists():
        try:
            estado = json.loads(ESTADO_FILE.read_text(encoding="utf-8"))
        except Exception as exc:
            estado = {}
            problema = f"estado-publicador.json não pôde ser lido: {exc}"
    else:
        estado = {}
        problema = "estado-publicador.json não existe."

    posts_hoje = estado.get("posts_hoje", 0)
    ultima = estado.get("ultima_publicacao")
    total = estado.get("total_publicados", 0)
    hoje = date.today().isoformat()
    evidencias = {
        "posts_hoje": posts_hoje,
        "ultima_publicacao": ultima,
        "total_publicados": total,
        "hoje": hoje,
        "limite": POSTS_POR_DIA,
    }

    if problema is None:
        if ultima != hoje:
            # contador deveria ter resetado; apenas informe (não é erro grave)
            pass
        if posts_hoje > POSTS_POR_DIA:
            problema = f"Limite de 2 posts/dia excedido: {posts_hoje} publicados hoje."
        elif posts_hoje == POSTS_POR_DIA:
            # atingiu o limite; não é erro, mas o supervisor avisa
            pass

    return {
        "nome": "Limite de 2 posts por dia",
        "ok": problema is None,
        "problema": problema,
        "evidencia": (
            f"{posts_hoje}/{POSTS_POR_DIA} posts hoje (total {total}, última {ultima})."
            if not problema else problema
        ),
        "sugere_correcao": (
            "Não publicar mais hoje; retomar amanhã após reset do contador."
            if problema else None
        ),
        "detalhes": evidencias,
    }


def checar_estrutura_pastas():
    """Confirma a estrutura ZAMBRIA (drafts, review, posts, publicados)."""
    faltando = []
    for pasta in (DRAFTS_DIR, REVIEW_DIR, POSTS_DIR, PUBLICADOS_DIR):
        if not pasta.exists():
            faltando.append(pasta.name)
    problema = f"pastas faltando: {faltando}" if faltando else None
    return {
        "nome": "Estrutura de pastas",
        "ok": problema is None,
        "problema": problema,
        "evidencia": f"drafts, review, posts, publicados presentes em {REPO.name}" if not problema else problema,
        "sugere_correcao": f"Criar as pastas faltando: {', '.join(faltando)}" if problema else None,
    }


def checar_jobs_locais():
    """Lê jobs.json e reporta status de cada agent do pipeline ZAMBRIA."""
    JOBS_FILE = Path("C:/Users/erico/AppData/Local/hermes/cron/jobs.json")
    resultado = {
        "nome": "Jobs locais (cron/schedule)",
        "ok": True,
        "problema": None,
        "evidencia": None,
        "sugere_correcao": None,
        "detalhes": {},
    }
    if not JOBS_FILE.exists():
        resultado["ok"] = False
        resultado["problema"] = f"jobs.json não encontrado em {JOBS_FILE}"
        resultado["evidencia"] = str(JOBS_FILE)
        resultado["sugere_correcao"] = "Verificar se o arquivo jobs.json existe no caminho do Hermes."
        return resultado

    try:
        dados = json.loads(JOBS_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        resultado["ok"] = False
        resultado["problema"] = f"jobs.json não pôde ser lido: {exc}"
        resultado["evidencia"] = str(JOBS_FILE)
        resultado["sugere_correcao"] = "Verificar integridade do arquivo jobs.json."
        return resultado

    jobs = dados.get("jobs", [])
    detalhes = {}
    problemas = []
    for job in jobs:
        nome = job.get("name", job.get("id", "desconhecido"))
        enabled = job.get("enabled", False)
        estado_job = job.get("state", "desconhecido")
        ultima = job.get("last_run_at", "nunca")
        status = job.get("last_status", "desconhecido")
        falhas = job.get("failure_streak", 0)
        proxima = job.get("next_run_at", "não agendado")
        detalhes[nome] = {
            "enabled": enabled,
            "state": estado_job,
            "last_status": status,
            "last_run": ultima,
            "failure_streak": falhas,
            "next_run": proxima,
        }
        if not enabled:
            problemas.append(f"{nome} está desabilitado (enabled=false)")
        elif falhas > 0:
            problemas.append(f"{nome} tem {falhas} falha(s) consecutiva(s)")
        elif status != "ok":
            problemas.append(f"{nome} com status '{status}'")

    if problemas:
        resultado["ok"] = False
        resultado["problema"] = "; ".join(problemas)

    resultado["evidencia"] = f"{len(jobs)} job(s) monitorado(s) em jobs.json"
    resultado["detalhes"] = detalhes
    if problemas:
        resultado["sugere_correcao"] = "Reativar jobs desabilitados ou investigar falhas consecutivas."
    return resultado


def verificar():
    """Executa todas as verificações e retorna o relatório estruturado."""
    relatorio = {
        "agente": "supervisor-fiscal-zambria",
        "site": SITE_URL,
        "repositorio": str(REPO),
        "executado_em": agora_iso(),
        "tom_editorial": TOM_EDITORIAL,
        "limite_posts_dia": POSTS_POR_DIA,
        "verificacoes": [],
        "resumo": {"total": 0, "ok": 0, "problemas": 0},
    }

    checagens = [
        checar_css,
        checar_sidebar_markup,
        checar_posts,
        checar_limite_diario,
        checar_estrutura_pastas,
        checar_jobs_locais,
    ]

    for fn in checagens:
        try:
            item = fn()
        except Exception as exc:  # pragma: no cover - defesa do agente
            item = {
                "nome": getattr(fn, "__name__", "verificacao"),
                "ok": False,
                "problema": f"erro ao executar verificação: {exc}",
                "evidencia": None,
                "sugere_correcao": "Revisar o código da verificação correspondente.",
            }
        relatorio["verificacoes"].append(item)
        relatorio["resumo"]["total"] += 1
        if item["ok"]:
            relatorio["resumo"]["ok"] += 1
        else:
            relatorio["resumo"]["problemas"] += 1

    relatorio["status_geral"] = "ok" if relatorio["resumo"]["problemas"] == 0 else "com_problemas"
    return relatorio


def checar_sidebar_markup():
    """Verifica se o botão de toggle da sidebar e seu JS estão no HTML online."""
    status, conteudo = http_get(SITE_URL)
    problema = None
    evidencias = {}
    if status is None or conteudo is None:
        return {
            "nome": "Botão da sidebar",
            "ok": False,
            "problema": "Não foi possível acessar o site online para verificar a sidebar.",
            "evidencia": f"GET {SITE_URL} -> sem resposta",
            "sugere_correcao": "Verificar conexão e se o site está no ar.",
        }

    html = conteudo.decode("utf-8", errors="replace")
    tem_botao = 'id="btnToggleSidebar"' in html or 'btn-toggle-sidebar' in html
    tem_js = "sidebar-hidden" in html and "toggle" in html.lower()
    tem_aside = 'class="sidebar"' in html or "<aside" in html

    evidencias = {
        "botao_presente": tem_botao,
        "js_toggle_presente": tem_js,
        "aside_presente": tem_aside,
    }

    if not tem_botao:
        problema = "Botão de toggle da sidebar (#btnToggleSidebar) não encontrado no HTML."
    elif not tem_js:
        problema = "Botão da sidebar existe, mas o script de toggle (sidebar-hidden) não foi encontrado."
    elif not tem_aside:
        problema = "Elemento <aside> da sidebar não encontrado."

    return {
        "nome": "Botão da sidebar",
        "ok": problema is None,
        "problema": problema,
        "evidencia": (
            f"botao={tem_botao}, js_toggle={tem_js}, aside={tem_aside}"
            if not problema else problema
        ),
        "sugere_correcao": (
            "Restaurar o botão <button id=\"btnToggleSidebar\"> e o script de toggle no index.html"
            if problema else None
        ),
        "detalhes": evidencias,
    }


# --------------------------- relatórios ---------------------------

def relatorio_markdown(relatorio):
    linhas = []
    linhas.append("# Relatório do Supervisor Fiscal ZAMBRIA")
    linhas.append("")
    linhas.append(f"- **Site:** {relatorio['site']}")
    linhas.append(f"- **Repositório:** {relatorio['repositorio']}")
    linhas.append(f"- **Executado em:** {relatorio['executado_em']}")
    linhas.append(f"- **Tom editorial ZAMBRIA:** {relatorio['tom_editorial']}")
    linhas.append(f"- **Limite:** {relatorio['limite_posts_dia']} posts/dia")
    linhas.append("")
    linhas.append("## Resumo")
    linhas.append(
        f"- Verificações: {relatorio['resumo']['total']} | "
        f"OK: {relatorio['resumo']['ok']} | "
        f"Problemas: {relatorio['resumo']['problemas']}"
    )
    linhas.append(f"- **Status geral:** {relatorio['status_geral']}")
    linhas.append("")
    linhas.append("## Verificações")
    for v in relatorio["verificacoes"]:
        status = "✅" if v["ok"] else "❌"
        linhas.append(f"### {status} {v['nome']}")
        if v.get("evidencia"):
            linhas.append(f"- Evidência: {v['evidencia']}")
        if v["problema"]:
            linhas.append(f"- Problema: {v['problema']}")
        if v.get("sugere_correcao"):
            linhas.append(f"- Sugere correção: {v['sugere_correcao']}")
        if v.get("detalhes"):
            linhas.append(f"- Detalhes: {json.dumps(v['detalhes'], ensure_ascii=False)}")
        linhas.append("")
    linhas.append("## Estrutura esperada ZAMBRIA")
    linhas.append("- `/drafts/` — rascunhos do agente pesquisador/revisor")
    linhas.append("- `/review/` — conteúdos aprovados aguardando publicação")
    linhas.append("- `/posts/` — artigos publicados (HTML)")
    linhas.append("- `/publicados/` — fontes arquivadas (.md)")
    linhas.append("")
    linhas.append("---\n*Gerado pelo Agente Supervisor Fiscal ZAMBRIA.*")
    return "\n".join(linhas)


def salvar_relatorio(relatorio, caminho_md=None):
    REPORT_FILE.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    md = relatorio_markdown(relatorio)
    if caminho_md is None:
        caminho_md = REPO / "supervisor_report.md"
    caminho_md.write_text(md, encoding="utf-8")
    return REPORT_FILE, caminho_md


def main():
    parser = argparse.ArgumentParser(description="Agente Supervisor Fiscal ZAMBRIA")
    parser.add_argument("--loop", action="store_true", help="rodar em loop contínuo")
    parser.add_argument("--interval", type=int, default=3600, help="intervalo entre rodadas (s)")
    parser.add_argument("--report", default=None, help="caminho do relatório markdown")
    args = parser.parse_args()

    def rodada():
        relatorio = verificar()
        salvar_relatorio(relatorio, Path(args.report) if args.report else None)
        print(relatorio_markdown(relatorio))
        return relatorio

    if args.loop:
        while True:
            relatorio = rodada()
            if relatorio["resumo"]["problemas"] > 0:
                log("Problemas detectados — veja supervisor_report.json / .md")
            time.sleep(args.interval)
    else:
        relatorio = rodada()
        sys.exit(0 if relatorio["status_geral"] == "ok" else 1)


if __name__ == "__main__":
    main()
