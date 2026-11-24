#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Agente Pesquisador Ativo Intermitente (zambria.github.io - O Insólito Presente)

Pesquisa continuamente os temas do blog (UFOs, Arqueologia, Sobrenatural,
Criptozologia, Conspirações, Fenômenos Naturais, Contos) em ciclos regulares,
busca novas fontes na web em português, verifica se há novas informações sobre
cada tópico e grava relatórios em pesquisas/. O estado fica em
estado-pesquisador.json para que buscas recentes não se repitam.

Execução única (padrão):   python pesquisador_ativo.py
Modo contínuo (background): python pesquisador_ativo.py --loop --interval 21600
                               (21600 s = 6 horas; Ctrl+C para parar)
"""

from __future__ import annotations

import argparse
import html as ihtml
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --------------------------- caminhos ---------------------------
REPO = Path(__file__).resolve().parent
TOPICS_FILE = REPO / "topics.json"
ESTADO_FILE = REPO / "estado-pesquisador.json"
PESQUISAS_DIR = REPO / "pesquisas"

INTERVALO_PADRAO_SEGUNDOS = 6 * 60 * 60  # 6 horas
MAX_FONTES = 2
TIMEOUT = 20
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ZAMBRIA-PesquisadorAtivo/1.0"

# Tema 7 (Contos) não está catalogado em topics.json — lista própria do agente.
CONTOS = [
    {"id": "contos-01", "categoria": "contos", "titulo": "Lenda do Curupira e guardiões da floresta"},
    {"id": "contos-02", "categoria": "contos", "titulo": "Lendas urbanas brasileiras contemporâneas"},
    {"id": "contos-03", "categoria": "contos", "titulo": "Casos de assombrações no Brasil"},
    {"id": "contos-04", "categoria": "contos", "titulo": "Histórias de fantasmas e médiuns populares"},
]

# Consulta base por categoria (em português, com viés a notícias recentes).
QUERIES = {
    "ufo": "OVNIs UAP notícias recentes 2026 governo Brasil",
    "arch": "descoberta arqueológica recente 2026 notícia ciência mistério",
    "para": "fenômenos paranormais recentes 2026 Brasil EVP experiência de quase-morte",
    "crypto": "criptozologia Bigfoot Mothman Chupacabra avistamentos recentes 2026",
    "conspir": "documentos governamentais desclassificados recentes conspiração OVNIs",
    "nature": "fenômenos naturais inexplicáveis luzes no céu 2026 relâmpago balístico",
    "contos": "contos de terror folclore brasileiro lendas urbanas Curupira",
}


def log(msg):
    print(f"[pesquisador-ativo] {msg}", flush=True)


def agora_local():
    """Horário da máquina (offset do fuso local, sem depender de banco de IANA)."""
    offset = time.localtime().tm_gmtoff or -3 * 3600
    return datetime.now(timezone(timedelta(seconds=offset)))


def carregar_topicos():
    topicos = []
    try:
        data = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))
        for cat in data.get("categorias", []):
            if not cat.get("ativo", True):
                continue
            for t in data.get("topicos", []):
                if t.get("categoria") == cat["id"]:
                    topicos.append({"id": t["id"], "categoria": cat["id"], "titulo": t["titulo"]})
    except Exception as e:
        log(f"não foi possível ler topics.json: {e}")
    for c in CONTOS:
        topicos.append(c)
    return topicos


def consulta_para(topico):
    cat = topico["categoria"]
    base = QUERIES.get(cat, f"notícias recentes {topico['titulo']}")
    return f"{base} {topico['titulo']}".strip()


# --------------------------- web (autônomo, sem chave de API) ---------------------------
def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.status, r.read()


def buscar_web(query):
    """DuckDuckGo HTML. Retorna lista de (titulo, url), sem inventar nada."""
    url = "https://duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        status, data = http_get(url)
        text = data.decode("utf-8", "ignore")
    except Exception as e:
        log(f"busca falhou ('{query}'): {e}")
        return []
    resultados = []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.S):
        href = ihtml.unescape(m.group(1))
        titulo = re.sub(r"<[^>]+>", " ", m.group(2))
        titulo = re.sub(r"\s+", " ", ihtml.unescape(titulo)).strip()
        if href.startswith("//"):
            href = "https:" + href
        if "duckduckgo.com/l/?" in href:
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            if "uddg" in qs:
                href = qs["uddg"][0]
        if href.startswith("http") and titulo:
            resultados.append((titulo, href))
    visto = set()
    out = []
    for t, u in resultados:
        if u not in visto:
            visto.add(u)
            out.append((t, u))
    return out[:MAX_FONTES + 2]


def extrair_texto(url):
    try:
        status, data = http_get(url)
        text = data.decode("utf-8", "ignore")
    except Exception as e:
        return f"(não foi possível ler a página: {e})"
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = ihtml.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:1200]


# --------------------------- estado e relatórios ---------------------------
def carregar_estado():
    if ESTADO_FILE.exists():
        try:
            return json.loads(ESTADO_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "versao": 1,
        "criado_em": None,
        "ultima_execucao": None,
        "intervalo_horas": INTERVALO_PADRAO_SEGUNDOS // 3600,
        "topicos": {},
    }


def salvar_estado(estado):
    ESTADO_FILE.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")


def salvar_relatorio(topico, consulta, fontes, resumo, status):
    PESQUISAS_DIR.mkdir(parents=True, exist_ok=True)
    caminho = PESQUISAS_DIR / f"{agora_local().strftime('%Y-%m-%d')}-{topico['id']}.md"
    linhas = [
        f"# Pesquisa: {topico['titulo']} ({topico['categoria']})",
        "",
        f"**Data:** {agora_local().strftime('%Y-%m-%d %H:%M')}",
        f"**Consulta:** {consulta}",
        f"**Status:** {status}",
        f"**Tópico:** {topico['id']}",
        "",
        "## Fontes encontradas",
        "",
    ]
    if fontes:
        for i, (t, u) in enumerate(fontes, 1):
            linhas.append(f"{i}. [{t}]({u})")
    else:
        linhas.append("*Nenhuma fonte encontrada nesta execução.*")
    linhas += ["", "## Resumo", "", resumo or "(sem resumo — nenhuma fonte acessível)", "",
               "---", "",
               "Gerado automaticamente pelo agente Pesquisador Ativo do ZAMBRIA."]
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return str(caminho)


def topicos_devidos(estado, topicos):
    agora = agora_local()
    intervalo = timedelta(hours=estado.get("intervalo_horas", 6))
    devidos = []
    for t in topicos:
        info = estado["topicos"].get(t["id"])
        if not info or not info.get("ultima_busca"):
            devidos.append(t)
            continue
        try:
            ultimo = datetime.fromisoformat(info["ultima_busca"])
            if agora - ultimo >= intervalo:
                devidos.append(t)
        except Exception:
            devidos.append(t)
    return devidos


def ciclo(estado, topicos, limite_fontes=MAX_FONTES):
    devidos = topicos_devidos(estado, topicos)
    if not devidos:
        log("nenhum tópico devido para pesquisa neste ciclo.")
        return 0
    log(f"{len(devidos)} tópico(s) devido(s): " + ", ".join(t["id"] for t in devidos))
    n = 0
    for t in devidos:
        consulta = consulta_para(t)
        log(f"pesquisando '{t['id']}': {consulta}")
        resultados = buscar_web(consulta)
        fontes = []
        trechos = []
        for titulo, url in resultados[:limite_fontes]:
            texto = extrair_texto(url)
            trechos.append(f"- [{titulo}]({url}): {texto[:300]}")
            fontes.append((titulo, url))
        resumo = " ".join(trechos) if trechos else "Nenhuma fonte acessível nesta execução."
        relatorio = salvar_relatorio(t, consulta, fontes, resumo, "ok" if fontes else "sem_fontes")
        info = estado["topicos"].setdefault(t["id"], {})
        info.update({
            "ultima_busca": agora_local().isoformat(),
            "total_buscas": int(info.get("total_buscas", 0)) + 1,
            "fontes_encontradas": len(fontes),
            "ultimo_relatorio": relatorio,
            "status": "ok" if fontes else "sem_fontes",
        })
        n += 1
        time.sleep(1.5)
    estado["ultima_execucao"] = agora_local().isoformat()
    if not estado.get("criado_em"):
        estado["criado_em"] = estado["ultima_execucao"]
    salvar_estado(estado)
    log(f"ciclo concluído: {n} tópico(s) pesquisado(s).")
    return n


def main():
    ap = argparse.ArgumentParser(description="Agente Pesquisador Ativo do ZAMBRIA")
    ap.add_argument("--loop", action="store_true", help="roda em loop contínuo")
    ap.add_argument("--interval", type=int, default=INTERVALO_PADRAO_SEGUNDOS,
                    help="intervalo entre ciclos em segundos (padrão 21600 = 6 h)")
    ap.add_argument("--topico", default=None, help="pesquisar apenas um tópico (id)")
    args = ap.parse_args()

    PESQUISAS_DIR.mkdir(parents=True, exist_ok=True)
    topicos = carregar_topicos()
    log(f"{len(topicos)} tópico(s) carregado(s) (topics.json + contos).")
    estado = carregar_estado()

    if args.topico:
        topicos = [t for t in topicos if t["id"] == args.topico] or topicos

    if args.loop:
        log(f"modo contínuo iniciado. Ciclo a cada {args.interval // 3600} hora(s). Ctrl+C para parar.")
        while True:
            try:
                ciclo(estado, topicos)
            except Exception as e:
                log(f"erro no ciclo: {e}")
            log(f"próximo ciclo em {args.interval // 60} minuto(s).")
            time.sleep(args.interval)
    else:
        ciclo(estado, topicos)


if __name__ == "__main__":
    main()
