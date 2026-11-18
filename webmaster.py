#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Agente webmaster (zambria.github.io)

Mantem o site online sincronizado com o repositorio. Conhece a estrutura
especifica do ZAMBRIA: sidebar esquerda, posts em /posts/,
estado em estado-publicador.json.

Verifica:
  1. index.html reflete os posts publicados em /posts/
  2. style.css carrega (existe e esta linkado em index.html e nos posts)
  3. botao toggle da sidebar existe e funciona (botao + JS + CSS)
  4. nao ha links internos quebrados (href de arquivo e ancoras #id)

Corre automaticamente o que e mecanico (lista de posts, bloco vazio,
botao toggle, link de CSS). O que nao consegue consertar sozinho,
reporta no final para abertura de tarefa no Kanban.

Execucao: python webmaster.py
"""

from __future__ import annotations

import html as html_mod
import re
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent
POSTS_DIR = REPO / "posts"
INDEX_FILE = REPO / "index.html"
STYLE_FILE = REPO / "style.css"

FIXES: list[str] = []  # corricoes aplicadas
WARN: list[str] = []   # problemas que exigem tarefa no Kanban


def log(msg: str) -> None:
    print(f"[webmaster] {msg}")


# ---------------------------------------------------------------- posts
def listar_posts() -> list[Path]:
    return sorted(POSTS_DIR.glob("*.html"))


def extrair_post(caminho: Path) -> dict:
    texto = caminho.read_text(encoding="utf-8")
    meta: dict[str, str] = {"slug": caminho.stem}

    m = re.search(r"<h2[^>]*>(.*?)</h2>", texto, re.DOTALL | re.IGNORECASE)
    if m:
        meta["titulo"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    else:
        mt = re.search(r"<title[^>]*>(.*?)</title>", texto, re.DOTALL | re.IGNORECASE)
        meta["titulo"] = html_mod.unescape(mt.group(1)).strip().replace(" — ZAMBRIA", "") if mt else caminho.stem

    mc = re.search(r'<span class="categoria">(.*?)</span>', texto, re.DOTALL | re.IGNORECASE)
    meta["categoria"] = html_mod.unescape(mc.group(1)).strip() if mc else "geral"

    md = re.search(r'<span class="categoria">.*?</span>\s*<span>(.*?)</span>', texto, re.DOTALL | re.IGNORECASE)
    meta["data"] = html_mod.unescape(md.group(1)).strip() if md else ""

    mp = re.search(r"<p>(.*?)</p>", texto, re.DOTALL | re.IGNORECASE)
    resumo = re.sub(r"<[^>]+>", "", mp.group(1)).strip() if mp else ""
    meta["resumo"] = (resumo[:217].rstrip() + "...") if len(resumo) > 220 else resumo
    return meta


def artigo_index_html(p: dict) -> str:
    return (
        "<article class=\"post\">\n"
        "        <div class=\"post-meta\">\n"
        f'          <span class="categoria">{html_mod.escape(p["categoria"])}</span>\n'
        f'          <span>{html_mod.escape(p["data"])}</span>\n'
        "        </div>\n"
        f'        <h2><a href="posts/{p["slug"]}.html">{html_mod.escape(p["titulo"])}</a></h2>\n'
        f'        <p>{html_mod.escape(p["resumo"])}</p>\n'
        "      </article>"
    )


# ---------------------------------------------------------------- index.html
def reconstruir_posts_lista(texto: str, posts: list[dict]) -> str:
    marcador = '<section id="posts-lista">'
    pos = texto.find(marcador)
    if pos == -1:
        raise RuntimeError("secao #posts-lista nao encontrada no index.html")

    # artigos que correspondem a posts reais (mantem ordem do /posts/)
    artigos = [artigo_index_html(p) for p in posts]
    lista = "\n".join(artigos)

    inicio = texto[: pos + len(marcador)]
    fim_marcador = "</section>"
    fim_pos = texto.find(fim_marcador, pos)
    if fim_pos == -1:
        raise RuntimeError("tag de fechamento </section> nao encontrada")
    fim = texto[fim_pos:]

    bloco_vazio = '<div class="vazio">'
    tem_vazio_atual = bloco_vazio in texto[pos:fim_pos]

    if posts:
        # remove o bloco "vazio" quando ha pelo menos um post real
        if tem_vazio_atual:
            fim = re.sub(r'<div class="vazio">.*?</div>\s*', "", fim, flags=re.DOTALL)
            FIXES.append("index.html: removeu bloco 'vazio' (posts existem em /posts/)")
    else:
        if not tem_vazio_atual:
            fim = "<div class=\"vazio\">\n            <p>Nenhum post publicado ainda. O primeiro artigo esta chegando.</p>\n        </div>\n        " + fim
            FIXES.append("index.html: inseriu bloco 'vazio' (nenhum post em /posts/)")

    novo = (
        inicio
        + "\n              "
        + lista
        + ("\n            " if lista else "")
        + fim
    )
    return novo


def garantir_link_css(texto: str) -> str:
    if 'rel="stylesheet" href="style.css"' in texto:
        return texto
    m = re.search(r"<head[^>]*>", texto, re.IGNORECASE)
    if not m:
        raise RuntimeE("tag <head> nao encontrada no index.html")
    texto = texto[: m.end()] + '\n  <link rel="stylesheet" href="style.css">' + texto[m.end():]
    FIXES.append("index.html: inseriu link para style.css no <head>")
    return texto


class RuntimeE(RuntimeError):
    pass


def garantir_toggle_sidebar(texto: str) -> str:
    # id no aside
    if 'id="sidebar-zambria"' not in texto:
        texto = texto.replace('<aside class="sidebar">', '<aside class="sidebar" id="sidebar-zambria">', 1)
        FIXES.append("index.html: adicionou id='sidebar-zambria' ao <aside>")

    # botao dentro do sidebar, apos o subtitulo
    if 'class="toggle-sidebar"' not in texto:
        botao = (
            '\n      <button class="toggle-sidebar" aria-label="Mostrar ou ocultar menu de categorias"'
            ' aria-expanded="true" aria-controls="sidebar-zambria">&#x2715;</button>'
        )
        texto = texto.replace('<div class="site-subtitle">O Insólito Presente</div>',
                              '<div class="site-subtitle">O Insólito Presente</div>' + botao, 1)
        FIXES.append("index.html: inseriu botao toggle da sidebar")

    # script antes de </body>
    js = (
        '  <script>\n'
        "    (function() {\n"
        "      var btn = document.querySelector('.toggle-sidebar');\n"
        "      var sidebar = document.getElementById('sidebar-zambria');\n"
        "      if (!btn || !sidebar) return;\n"
        "      btn.addEventListener('click', function() {\n"
        "        var fechado = sidebar.classList.toggle('fechado');\n"
        "        btn.setAttribute('aria-expanded', String(!fechado));\n"
        "        btn.textContent = fechado ? '\u2630' : '\u2715';\n"
        "      });\n"
        "    })();\n"
        "  </script>\n"
    )
    if "sidebar.classList.toggle" not in texto:
        if "</body>" in texto:
            texto = texto.replace("</body>", js + "</body>", 1)
        else:
            texto = texto + js
        FIXES.append("index.html: inseriu script de toggle da sidebar antes de </body>")
    return texto


# ---------------------------------------------------------------- style.css
CSS_TOGGLE = """

/* Botao toggle da sidebar (aparece apenas em telas pequenas) */
.toggle-sidebar {
  display: none;
  background: none;
  border: none;
  color: var(--text);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  margin-bottom: 1rem;
  align-self: start;
}

@media (max-width: 768px) {
  .toggle-sidebar {
    display: block;
  }

  /* esconde/mostra a sidebar esquerda no mobile */
  .sidebar.fechado {
    display: none;
  }
}


"""


def garantir_css_toggle() -> None:
    texto = STYLE_FILE.read_text(encoding="utf-8")
    if ".toggle-sidebar" in texto:
        return
    STYLE_FILE.write_text(texto + CSS_TOGGLE, encoding="utf-8")
    FIXES.append("style.css: adicionou regras do botao toggle da sidebar")


# ---------------------------------------------------------------- links
def checar_links_internos() -> list[str]:
    quebrados: list[str] = []
    documentos = [INDEX_FILE] + listar_posts()

    for doc in documentos:
        texto = doc.read_text(encoding="utf-8")
        base = doc.parent
        ids: set[str] = set(re.findall(r'id="([^"]+)"', texto))
        ids.update(re.findall(r'name="([^"]+)"', texto))

        for href in re.findall(r'href="([^"]*)"', texto):
            if not href or href.startswith(("http:", "https:", "mailto:", "tel:", "#")):
                if href.startswith("#"):
                    alvo = href[1:]
                    if alvo not in ids:
                        quebrados.append(f"{doc.name}: ancora #{alvo} nao existe na pagina")
                continue
            alvo = (base / href).resolve()
            if not alvo.exists():
                quebrados.append(f"{doc.name}: link quebrado '{href}' (arquivo nao encontrado)")
    return quebrados


# ---------------------------------------------------------------- externos
def verificar_externo(url: str, timeout: int = 8) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "ZAMBRIA-webmaster/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False


# ---------------------------------------------------------------- fluxo
def main() -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    posts = [extrair_post(p) for p in listar_posts()]
    log(f"{len(posts)} post(s) encontrado(s) em /posts/: " + ", ".join(p["slug"] for p in posts) or "nenhum")

    texto = INDEX_FILE.read_text(encoding="utf-8")

    # 1. index.html reflete /posts/
    texto = reconstruir_posts_lista(texto, posts)

    # 2. CSS carrega
    texto = garantir_link_css(texto)
    if not STYLE_FILE.exists():
        WARN.append("style.css nao existe — nao foi possivel garantir carregamento do CSS")
    else:
        log("style.css presente e carregado por index.html")

    # 3. toggle da sidebar
    texto = garantir_toggle_sidebar(texto)
    garantir_css_toggle()

    INDEX_FILE.write_text(texto, encoding="utf-8")

    # 4. links internos
    quebrados = checar_links_internos()
    if quebrados:
        for q in quebrados:
            log("LINK QUEBRADO: " + q)
        WARN.append(f"{len(quebrados)} link(s) interno(s) quebrado(s) — ver relatorio")
    else:
        log("sem links internos quebrados")

    # links externos (fontes nos posts)
    externos: list[str] = []
    for p in listar_posts():
        texto_p = p.read_text(encoding="utf-8")
        for u in re.findall(r'https?://[^\s<"\']+', texto_p):
            u = u.rstrip(".,);]")
            externos.append(u)
    vistos = []
    for u in dict.fromkeys(externos):
        ok = verificar_externo(u)
        status = "OK" if ok else "FALHOU (ou sem rede)"
        log(f"externo {u}: {status}")
        vistos.append(f"{u} -> {status}")
        if not ok:
            WARN.append(f"link externo nao respondeu: {u}")

    # ---------------------------------------------------------------- relatorio
    linhas: list[str] = []
    linhas.append("# Relatório do webmaster ZAMBRIA")
    linhas.append("")
    linhas.append(f"Posts em /posts/: {len(posts)}")
    for p in posts:
        linhas.append(f"- {p['slug']}.html — {p['titulo']} ({p['categoria']}, {p['data']})")
    linhas.append("")
    linhas.append("## Corricoes aplicadas")
    if FIXES:
        for f in FIXES:
            linhas.append(f"- [x] {f}")
    else:
        linhas.append("- nenhuma necessaria")
    linhas.append("")
    linhas.append("## Pendentes (abrir tarefa no Kanban se aplicavel)")
    if WARN:
        for w in WARN:
            linhas.append(f"- [ ] {w}")
    else:
        linhas.append("- nenhum")
    linhas.append("")
    linhas.append("## Links internos")
    if quebrados:
        for q in quebrados:
            linhas.append(f"- [ ] quebrado: {q}")
    else:
        linhas.append("- nenhum")
    linhas.append("")
    linhas.append("## Links externos (fontes consultadas)")
    for v in vistos:
        linhas.append(f"- {v}")

    relatorio = REPO / "webmaster-relatorio.md"
    relatorio.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas))

    return 1 if WARN else 0


if __name__ == "__main__":
    raise SystemExit(main())
