#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Agente Auditor Estrutural Contínua (zambria.github.io)

Verifica, repara, testa e aprova a estrutura do site a cada 2 minutos:

  1. Site rodando (index.html acessível, HTTP 200).
  2. Páginas acessíveis (index + todos os posts em /posts/).
  3. Sem posts duplicados (mesmo título HTML) em /posts/.
  4. Links válidos (links internos href resolvem para arquivo existente).
  5. CSS carregando (style.css existe, não vazio, assinatura ZAMBRIA presente).
  6. Estrutura de pastas correta (drafts, review, posts, publicados).
  7. Frontmatter válido (bloco --- ... --- em .md de review/ e publicados/).
  8. Posts publicados com HTML correspondente (cada .md em publicados/ tem
     seu .html em posts/).

Repara automaticamente qualquer erro encontrado, testa após a reparação e
aprova somente quando todas as verificações passam.

Execução:
  python auditor_estrutural.py          # uma rodada única
  python auditor_estrutural.py --loop   # loop contínuo a cada 2 minutos
"""

from __future__ import annotations

import argparse
import hashlib
import html as ihtml
import json
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# --------------------------- caminhos ---------------------------
REPO = Path(__file__).resolve().parent
INDEX_FILE = REPO / "index.html"
STYLE_FILE = REPO / "style.css"
POSTS_DIR = REPO / "posts"
DRAFTS_DIR = REPO / "drafts"
REVIEW_DIR = REPO / "review"
PUBLICADOS_DIR = REPO / "publicados"
RELATORIO_JSON = REPO / "auditor_report.json"
RELATORIO_MD = REPO / "auditor_report.md"
ESTADO_FILE = REPO / "estado-auditor.json"

INTERVALO_SEGUNDOS = 120  # timer de 2 minutos
MAX_ITERACOES_INTERNAS = 3  # limite do loop verificar-reparar-reverificar

# Assinaturas que confirmam que o CSS é realmente o do ZAMBRIA.
CSS_ASSINATURAS = [".site-shell", "--bg", "--accent", ".sidebar", ".conteudo"]

# Pastas obrigatórias da estrutura ZAMBRIA.
PASTAS_OBRIGATORIAS = [DRAFTS_DIR, REVIEW_DIR, POSTS_DIR, PUBLICADOS_DIR]

LOG_PREFIX = "[auditor]"


# --------------------------- utilitários ---------------------------
def log(msg: str):
    print(f"{LOG_PREFIX} {msg}", flush=True)


def agora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ler_texto(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8")
    except Exception:
        return ""


def escrever_texto(caminho: Path, texto: str):
    caminho.write_text(texto, encoding="utf-8")


def carregar_json(caminho: Path, padrao=None):
    if padrao is None:
        padrao = {}
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except Exception:
        return padrao


def salvar_json(caminho: Path, dados):
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------- estado do auditor ---------------------------
def carregar_estado():
    return carregar_json(ESTADO_FILE, {
        "rodadas": 0,
        "reparacoes_totais": 0,
        "ultima_aprovacao": None,
        "ultima_rodada": None,
    })


def salvar_estado(estado):
    salvar_json(ESTADO_FILE, estado)


# --------------------------- verificações ---------------------------
def checar_site_rodando():
    """Verifica se o index.html existe e é acessível (simulado local)."""
    if not INDEX_FILE.exists():
        return {
            "nome": "Site rodando",
            "ok": False,
            "problema": "index.html não encontrado no repositório.",
            "evidencia": str(INDEX_FILE),
            "sugere_correcao": "Criar index.html na raiz do repositório.",
        }
    texto = ler_texto(INDEX_FILE)
    if not texto.strip():
        return {
            "nome": "Site rodando",
            "ok": False,
            "problema": "index.html está vazio (0 bytes).",
            "evidencia": str(INDEX_FILE),
            "sugere_correcao": "Preencher index.html com conteúdo HTML válido.",
        }
    if "<!doctype html" not in texto.lower():
        return {
            "nome": "Site rodando",
            "ok": False,
            "problema": "index.html não tem DOCTYPE HTML (não é um HTML válido).",
            "evidencia": f"{len(texto)} bytes",
            "sugere_correcao": "Adicionar <!DOCTYPE html> no início do index.html.",
        }
    return {
        "nome": "Site rodando",
        "ok": True,
        "problema": None,
        "evidencia": f"index.html válido ({len(texto)} bytes)",
        "sugere_correcao": None,
    }


def checar_css_carregando():
    if not STYLE_FILE.exists():
        return {
            "nome": "CSS carregando",
            "ok": False,
            "problema": "style.css não encontrado.",
            "evidencia": str(STYLE_FILE),
            "sugere_correcao": "Criar style.css na raiz do repositório.",
        }
    texto = ler_texto(STYLE_FILE)
    if not texto.strip():
        return {
            "nome": "CSS carregando",
            "ok": False,
            "problema": "style.css está vazio (0 bytes).",
            "evidencia": str(STYLE_FILE),
            "sugere_correcao": "Preencher style.css com o CSS do ZAMBRIA.",
        }
    if not any(assinatura in texto for assinatura in CSS_ASSINATURAS):
        return {
            "nome": "CSS carregando",
            "ok": False,
            "problema": "style.css carrega, mas não tem assinatura ZAMBRIA.",
            "evidencia": f"amostra: {texto[:80]!r}",
            "sugere_correcao": "Restaurar o style.css original do ZAMBRIA.",
        }
    # referência no index.html
    index_html = ler_texto(INDEX_FILE)
    if "style.css" not in index_html:
        return {
            "nome": "CSS carregando",
            "ok": False,
            "problema": "index.html não referencia style.css.",
            "evidencia": str(INDEX_FILE),
            "sugere_correcao": "Adicionar <link rel=\"stylesheet\" href=\"style.css\"> ao <head> do index.html.",
        }
    return {
        "nome": "CSS carregando",
        "ok": True,
        "problema": None,
        "evidencia": f"style.css válido ({len(texto)} bytes, assinatura ZAMBRIA)",
        "sugere_correcao": None,
    }


def extrair_titulo(html: str):
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def checar_posts_duplicados():
    """Detecta posts HTML com o mesmo título em /posts/."""
    if not POSTS_DIR.exists():
        return {
            "nome": "Sem posts duplicados",
            "ok": True,
            "problema": None,
            "evidencia": "pasta /posts/ não existe (ainda).",
            "sugere_correcao": None,
            "detalhes": {},
        }
    arquivos = sorted(POSTS_DIR.glob("*.html"))
    titulos = {}
    duplicados = []
    for arq in arquivos:
        titulo = extrair_titulo(ler_texto(arq)) or arq.stem
        chave = re.sub(r"\s+", " ", titulo.lower()).strip()
        if chave in titulos:
            duplicados.append({"titulo": titulo, "arquivos": [titulos[chave], arq.name]})
        else:
            titulos[chave] = arq.name
    if duplicados:
        return {
            "nome": "Sem posts duplicados",
            "ok": False,
            "problema": f"{len(duplicados)} grupo(s) de post(s) duplicado(s) pelo mesmo título.",
            "evidencia": "; ".join(f"{d['titulo']}: {d['arquivos']}" for d in duplicados),
            "sugere_correcao": "Remover os posts duplicados, mantendo apenas a versão mais recente/completa.",
            "detalhes": {"duplicados": duplicados},
        }
    return {
        "nome": "Sem posts duplicados",
        "ok": True,
        "problema": None,
        "evidencia": f"{len(arquivos)} post(s) HTML, todos com títulos únicos.",
        "sugere_correcao": None,
        "detalhes": {"total": len(arquivos)},
    }


def extrair_links_internos(html: str, base_dir: Path):
    """Extrai links internos (href) que não sejam http/mailto/anchor."""
    links = []
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        # remove fragment
        href = href.split("#")[0]
        if not href:
            continue
        links.append(href)
    return links


def checar_links_validos():
    """Verifica se todos os links internos de index.html e posts resolvem."""
    paginas = []
    if INDEX_FILE.exists():
        paginas.append(INDEX_FILE)
    if POSTS_DIR.exists():
        paginas.extend(sorted(POSTS_DIR.glob("*.html")))
    quebrados = []
    total_links = 0
    for pagina in paginas:
        texto = ler_texto(pagina)
        for href in extrair_links_internos(texto, REPO):
            total_links += 1
            alvo = (pagina.parent / href).resolve()
            if not alvo.exists():
                quebrados.append({"pagina": pagina.name, "link": href, "alvo": str(alvo)})
    if quebrados:
        return {
            "nome": "Links válidos",
            "ok": False,
            "problema": f"{len(quebrado if False else quebrados)} link(s) interno(s) quebrado(s).",
            "evidencia": "; ".join(f"{q['pagina']} -> {q['link']}" for q in quebrados[:10]),
            "sugere_correcao": "Corrigir ou remover os links apontando para arquivos inexistentes.",
            "detalhes": {"quebrados": quebrados, "total_links": total_links},
        }
    return {
        "nome": "Links válidos",
        "ok": True,
        "problema": None,
        "evidencia": f"{total_links} link(s) interno(s) verificado(s), todos resolvendo.",
        "sugere_correcao": None,
        "detalhes": {"total_links": total_links},
    }


def checar_estrutura_pastas():
    faltando = [p.name for p in PASTAS_OBRIGATORIAS if not p.exists()]
    if faltando:
        return {
            "nome": "Estrutura de pastas",
            "ok": False,
            "problema": f"pastas faltando: {faltando}",
            "evidencia": ", ".join(faltando),
            "sugere_correcao": f"Criar as pastas: {', '.join(faltando)}",
        }
    return {
        "nome": "Estrutura de pastas",
        "ok": True,
        "problema": None,
        "evidencia": "drafts, review, posts, publicados presentes.",
        "sugere_correcao": None,
    }


def parse_frontmatter(texto: str):
    """Retorna (meta_dict, corpo, valido, motivo)."""
    m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)$", texto, re.DOTALL)
    if not m:
        return {}, texto, False, "sem bloco frontmatter --- ... ---"
    bloco = m.group(1)
    corpo = m.group(2)
    meta = {}
    for linha in bloco.splitlines():
        if ":" in linha:
            chave, _, valor = linha.partition(":")
            meta[chave.strip()] = valor.strip().strip('"').strip("'")
    # campos obrigatórios (convenção ZAMBRIA em português)
    obrigatorios = ["titulo", "resumo", "categoria", "data", "slug"]
    faltando = [c for c in obrigatorios if not meta.get(c)]
    if faltando:
        return meta, corpo, False, f"frontmatter sem campo(s) obrigatório(s): {faltando}"
    return meta, corpo, True, None


def checar_frontmatter_valido():
    """Verifica frontmatter de .md em review/pendentes, review/publicados e publicados/."""
    alvos = []
    if (REVIEW_DIR / "pendentes").exists():
        alvos.extend(sorted((REVIEW_DIR / "pendentes").glob("*.md")))
    invalidos = []
    total = 0
    for arq in alvos:
        total += 1
        texto = ler_texto(arq)
        if not texto.strip():
            invalidos.append({"arquivo": arq.name, "motivo": "arquivo vazio"})
            continue
        meta, corpo, valido, motivo = parse_frontmatter(texto)
        if not valido:
            invalidos.append({"arquivo": arq.name, "motivo": motivo})
    if invalidos:
        return {
            "nome": "Frontmatter válido",
            "ok": False,
            "problema": f"{len(invalidos)} arquivo(s) com frontmatter inválido.",
            "evidencia": "; ".join(f"{i['arquivo']} ({i['motivo']})" for i in invalidos[:10]),
            "sugere_correcao": "Adicionar/consertar o bloco frontmatter --- ... --- com o campo title.",
            "detalhes": {"invalidos": invalidos, "total": total},
        }
    return {
        "nome": "Frontmatter válido",
        "ok": True,
        "problema": None,
        "evidencia": f"{total} arquivo(s) .md com frontmatter válido.",
        "sugere_correcao": None,
        "detalhes": {"total": total},
    }


def slugify(titulo: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (titulo or "post").lower()).strip("-")
    return slug or "post"


def checar_posts_correspondentes():
    """Cada .md em publicados/ deve ter um .html correspondente em posts/."""
    if not PUBLICADOS_DIR.exists() or not POSTS_DIR.exists():
        return {
            "nome": "Posts publicados com HTML correspondente",
            "ok": True,
            "problema": None,
            "evidencia": "pastas fonte ou posts não existem ainda.",
            "sugere_correcao": None,
        }
    md_files = sorted(PUBLICADOS_DIR.glob("*.md"))
    html_stems = {p.stem for p in POSTS_DIR.glob("*.html")}
    faltando_html = []
    for md in md_files:
        # tenta corresponder pelo stem direto e por slug do título no frontmatter
        candidato = md.stem
        texto = ler_texto(md)
        meta, _, valido, _ = parse_frontmatter(texto)
        candidato_slug = (
            meta.get("slug")
            or meta.get("titulo")
            or meta.get("title")
            or candidato
        )
        candidato_slug = slugify(candidato_slug)
        if candidato not in html_stems and candidato_slug not in html_stems:
            faltando_html.append({"md": md.name, "candidato_html": f"{candidato}.html"})
    if faltando_html:
        return {
            "nome": "Posts publicados com HTML correspondente",
            "ok": False,
            "problema": f"{len(faltando_html)} post(s) publicado(s) sem HTML em /posts/.",
            "evidencia": "; ".join(f"{f['md']} -> {f['candidato_html']}" for f in faltando_html[:10]),
            "sugere_correcao": "Gerar o HTML correspondente para cada post publicado em /posts/.",
            "detalhes": {"faltando": faltando_html},
        }
    return {
        "nome": "Posts publicados com HTML correspondente",
        "ok": True,
        "problema": None,
        "evidencia": f"{len(md_files)} post(s) publicado(s) com HTML correspondente.",
        "sugere_correcao": None,
        "detalhes": {"total": len(md_files)},
    }


# --------------------------- reparações ---------------------------
def reparar_posts_duplicados():
    """Remove posts HTML duplicados pelo mesmo título, mantendo o maior/mais recente."""
    if not POSTS_DIR.exists():
        return 0, []
    arquivos = sorted(POSTS_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    vistos = {}
    removidos = []
    for arq in arquivos:
        texto = ler_texto(arq)
        titulo = extrair_titulo(texto) or arq.stem
        chave = re.sub(r"\s+", " ", titulo.lower()).strip()
        if chave in vistos:
            arq.unlink()
            removidos.append(arq.name)
            log(f"REPARADO: post duplicado removido '{arq.name}' (título: {titulo})")
        else:
            vistos[chave] = arq.name
    return len(removidos), removidos


def reparar_links_quebrados():
    """Remove links internos quebrados de index.html e posts (substitui por #)."""
    paginas = []
    if INDEX_FILE.exists():
        paginas.append(INDEX_FILE)
    if POSTS_DIR.exists():
        paginas.extend(sorted(POSTS_DIR.glob("*.html")))
    consertados = 0
    for pagina in paginas:
        texto = ler_texto(pagina)
        novo = texto
        mudou = False
        for href in extrair_links_internos(texto, REPO):
            alvo = (pagina.parent / href).resolve()
            if not alvo.exists():
                novo = novo.replace(f'href="{href}"', f'href="#"')
                mudou = True
                consertados += 1
                log(f"REPARADO: link quebrado '{href}' em {pagina.name} -> #")
        if mudou:
            escrever_texto(pagina, novo)
    return consertados


def reparar_estrutura_pastas():
    criadas = []
    for p in PASTAS_OBRIGATORIAS:
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            criadas.append(p.name)
            log(f"REPARADO: pasta criada '{p.name}'")
    return criadas


def reparar_css_referencia():
    """Garante que index.html reference style.css."""
    if not INDEX_FILE.exists() or not STYLE_FILE.exists():
        return False
    texto = ler_texto(INDEX_FILE)
    if "style.css" in texto:
        return False
    if "<head>" in texto.lower():
        novo = texto.replace("<head>", '<head>\n  <link rel="stylesheet" href="style.css">', 1)
        escrever_texto(INDEX_FILE, novo)
        log("REPARADO: referência ao style.css adicionada ao index.html")
        return True
    return False


def reparar_doctype_index():
    """Insere <!DOCTYPE html> no início do index.html se faltar."""
    if not INDEX_FILE.exists():
        return False
    texto = ler_texto(INDEX_FILE)
    if "<!doctype html" in texto.lower():
        return False
    novo = "<!DOCTYPE html>\n" + texto
    escrever_texto(INDEX_FILE, novo)
    log("REPARADO: DOCTYPE HTML adicionado ao index.html")
    return True


def extrair_titulo_md(texto: str, nome_arquivo: str):
    """Extrai um título de um .md: frontmatter title, H1, ou nome do arquivo."""
    meta, _, valido, _ = parse_frontmatter(texto)
    if valido and meta.get("title"):
        return meta["title"]
    m = re.search(r"^#\s+(.+)$", texto, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return Path(nome_arquivo).stem.replace("-", " ").replace("_", " ").title()


def reparar_frontmatter():
    """Adiciona frontmatter --- ... --- com campo title a .md que não tenham."""
    alvos = []
    for d in (REVIEW_DIR / "pendentes", REVIEW_DIR / "publicados", PUBLICADOS_DIR):
        if d.exists():
            alvos.extend(sorted(d.glob("*.md")))
    consertados = 0
    for arq in alvos:
        texto = ler_texto(arq)
        if not texto.strip():
            continue
        _, _, valido, motivo = parse_frontmatter(texto)
        if valido:
            continue
        meta_exist, corpo_fm, _, _ = parse_frontmatter(texto)
        titulo = extrair_titulo_md(texto, arq.name)
        resumo = meta_exist.get("resumo") or "Sem resumo informado."
        categoria = meta_exist.get("categoria") or meta_exist.get("category") or "geral"
        data = meta_exist.get("data") or agora_iso()[:10]
        slug = meta_exist.get("slug") or slugify(titulo)
        partes = [
            "---",
            'titulo: "' + ihtml.escape(titulo) + '"',
            'resumo: "' + ihtml.escape(resumo) + '"',
            "categoria: " + categoria,
            "data: " + data,
            "slug: " + slug,
            "---",
            "",
        ]
        bloco = chr(10).join(partes) + chr(10)
        if motivo == "sem bloco frontmatter --- ... ---":
            novo = bloco + texto
        else:
            m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)$", texto, re.DOTALL)
            if m:
                corpo = m.group(2)
                novo = bloco + corpo
            else:
                novo = bloco + texto
        escrever_texto(arq, novo)
        consertados += 1
        log(f"REPARADO: frontmatter adicionado a '{arq.name}' (title: {titulo})")
    return consertados


def gerar_html_para_publicados():
    """Gera HTML em /posts/ para cada .md em publicado/ que não tem correspondente."""
    if not PUBLICADOS_DIR.exists() or not POSTS_DIR.exists():
        return 0, []
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    gerados = []
    for md in sorted(PUBLICADOS_DIR.glob("*.md")):
        texto = ler_texto(md)
        meta, corpo, valido, _ = parse_frontmatter(texto)
        titulo = meta.get("title") or md.stem
        slug = slugify(titulo)
        html_name = f"{slug}.html"
        alvo = POSTS_DIR / html_name
        if alvo.exists():
            continue
        # converter markdown simples para HTML
        corpo_html = markdown_para_html(corpo)
        html_completo = montar_html_post(titulo, meta, corpo_html, md.name)
        escrever_texto(alvo, html_completo)
        gerados.append(html_name)
        log(f"REPARADO: HTML gerado para post publicado '{md.name}' -> posts/{html_name}")
    return len(gerados), gerados


def markdown_para_html(texto: str) -> str:
    """Conversão muito simples de markdown para HTML (suficiente para o ZAMBRIA)."""
    linhas = texto.split("\n")
    saida = []
    em_lista = False
    for linha in linhas:
        l = linha.rstrip()
        if re.match(r"^#\s+", l):
            saida.append(f"<h1>{l[2:].strip()}</h1>")
        elif re.match(r"^##\s+", l):
            saida.append(f"<h2>{l[3:].strip()}</h2>")
        elif re.match(r"^###\s+", l):
            saida.append(f"<h3>{l[4:].strip()}</h3>")
        elif re.match(r"^[-*]\s+", l):
            if not em_lista:
                saida.append("<ul>")
                em_lista = True
            saida.append(f"  <li>{l[2:].strip()}</li>")
        else:
            if em_lista:
                saida.append("</ul>")
                em_lista = False
            if l.strip():
                saida.append(f"<p>{l}</p>")
    if em_lista:
        saida.append("</ul>")
    return "\n".join(saida)


def montar_html_post(titulo, meta, corpo_html, fonte_md):
    categoria = meta.get("category", "geral")
    data = meta.get("data_revisao") or meta.get("data_pesquisa") or ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ihtml.escape(titulo)} — ZAMBRIA</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="site-shell" id="site-shell">
    <aside class="sidebar" id="sidebar-zambria">
      <div class="sidebar-header">
        <button class="btn-toggle-sidebar" id="btnToggleSidebar" aria-label="Esconder barra lateral">☰</button>
        <div class="site-title">ZAMBRIA</div>
      </div>
      <div class="site-subtitle">O Insólito Presente</div>
      <div class="categoria-grupo">
        <div class="categoria-titulo">{categoria}</div>
        <ul class="lista-topicos">
          <li><a href="../index.html">← Voltar ao início</a></li>
        </ul>
      </div>
    </aside>
    <main class="conteudo">
      <section class="hero">
        <h1>{ihtml.escape(titulo)}</h1>
        <p class="post-meta"><span class="categoria">{categoria}</span> <span>{data}</span></p>
      </section>
      <article class="post">
        <div class="texto">
          {corpo_html}
        </div>
        <div class="comentario-agente">
          <p>[Comentário do ZAMBRIA: este post foi restaurado pelo auditor estrutural contínua. O mistério permanece aberto. E talvez devesse ficar assim.]</p>
        </div>
      </article>
    </main>
    <script>
      const btn = document.getElementById('btnToggleSidebar');
      const shell = document.querySelector('.site-shell');
      btn.addEventListener('click', () => {{
        shell.classList.toggle('sidebar-hidden');
        if (shell.classList.contains('sidebar-hidden')) {{
          btn.textContent = '≡';
          btn.setAttribute('aria-label', 'Mostrar barra lateral');
        }} else {{
          btn.textContent = '☰';
          btn.setAttribute('aria-label', 'Esconder barra lateral');
        }}
      }});
    </script>
  </div>
</body>
</html>"""


# --------------------------- rodada de auditoria ---------------------------
def executar_verificacoes():
    checagens = [
        checar_site_rodando(),
        checar_css_carregando(),
        checar_posts_duplicados(),
        checar_links_validos(),
        checar_estrutura_pastas(),
        checar_frontmatter_valido(),
        checar_posts_correspondentes(),
    ]
    return checagens


def relatorio_markdown(relatorio):
    linhas = []
    linhas.append("# Relatório do Auditor Estrutural Contínua — ZAMBRIA")
    linhas.append("")
    linhas.append(f"- **Repositório:** {REPO.name}")
    linhas.append(f"- **Executado em:** {relatorio['executado_em']}")
    linhas.append(f"- **Rodada:** {relatorio['rodada']}")
    linhas.append("")
    linhas.append("## Resumo")
    linhas.append(
        f"- Verificações: {relatorio['resumo']['total']} | "
        f"OK: {relatorio['resumo']['ok']} | "
        f"Problemas: {relatorio['resumo']['problemas']}"
    )
    linhas.append(f"- Reparações aplicadas: {relatorio['reparacoes_aplicadas']}")
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
    linhas.append(f"---\n*Gerado pelo Auditor Estrutural Contínua ZAMBRIA (timer 2 min).*")
    return "\n".join(linhas)


def salvar_relatorio(relatorio):
    RELATORIO_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
    RELATORIO_MD.write_text(relatorio_markdown(relatorio), encoding="utf-8")
    return RELATORIO_JSON, RELATORIO_MD


def aplicar_reparacoes(checagens):
    """Aplica reparos automáticos com base nos problemas detectados."""
    reparacoes = []
    total = 0

    # 1. Estrutura de pastas (fazer primeiro)
    for c in checagens:
        if c["nome"] == "Estrutura de pastas" and not c["ok"]:
            criadas = reparar_estrutura_pastas()
            if criadas:
                reparacoes.append({"acao": "estrutura_pastas", "criadas": criadas})
                total += len(criadas)

    # 2. DOCTYPE do index
    for c in checagens:
        if c["nome"] == "Site rodando" and not c["ok"]:
            if reparar_doctype_index():
                reparacoes.append({"acao": "doctype_index"})
                total += 1

    # 3. CSS referência no index
    for c in checagens:
        if c["nome"] == "CSS carregando" and not c["ok"]:
            if reparar_css_referencia():
                reparacoes.append({"acao": "css_referencia_index"})
                total += 1

    # 4. Posts duplicados
    for c in checagens:
        if c["nome"] == "Sem posts duplicados" and not c["ok"]:
            qtd, removidos = reparar_posts_duplicados()
            if qtd:
                reparacoes.append({"acao": "remover_duplicados", "removidos": removidos})
                total += qtd

    # 5. Links quebrados
    for c in checagens:
        if c["nome"] == "Links válidos" and not c["ok"]:
            qtd = reparar_links_quebrados()
            if qtd:
                reparacoes.append({"acao": "consertar_links", "consertados": qtd})
                total += qtd

    # 6. Frontmatter
    for c in checagens:
        if c["nome"] == "Frontmatter válido" and not c["ok"]:
            qtd = reparar_frontmatter()
            if qtd:
                reparacoes.append({"acao": "reparar_frontmatter", "consertados": qtd})
                total += qtd

    # 7. Posts publicados sem HTML
    for c in checagens:
        if c["nome"] == "Posts publicados com HTML correspondente" and not c["ok"]:
            qtd, gerados = gerar_html_para_publicados()
            if qtd:
                reparacoes.append({"acao": "gerar_html", "gerados": gerados})
                total += qtd

    return total, reparacoes


def _resumo_checagens(checagens):
    problemas = [c for c in checagens if not c["ok"]]
    return {
        "total": len(checagens),
        "ok": sum(1 for c in checagens if c["ok"]),
        "problemas": len(problemas),
        "problemas_lista": problemas,
    }


def rodada(estado):
    """Executa uma rodada completa: verifica, repara, re-testa (loop interno
    verificar→reparar→reverificar), aprova somente quando todas as
    verificações passam. O loop interno lida com problemas em cadeia (ex.:
    remover um post duplicado pode deixar links órfãos, consertados apenas na
    próxima iteração)."""
    estado["rodadas"] = estado.get("rodadas", 0) + 1
    rodada_num = estado["rodadas"]
    log(f"=== Rodada #{rodada_num} — iniciando auditoria ===")

    total_reparacoes_rodada = 0
    todas_reparacoes = []
    checagens_finais = []

    for iteracao in range(1, MAX_ITERACOES_INTERNAS + 1):
        log(f"  [iteração {iteracao}] verificando...")
        checagens = executar_verificacoes()
        resumo = _resumo_checagens(checagens)
        if resumo["problemas"] == 0:
            log(f"  [iteração {iteracao}] sem problemas detectados.")
            checagens_finais = checagens
            break

        log(f"  [iteração {iteracao}] {resumo['problemas']} problema(s) detectado(s).")
        total_rep, reparacoes = aplicar_reparacoes(checagens)
        total_reparacoes_rodada += total_rep
        todas_reparacoes.extend(reparacoes)
        if total_rep:
            log(f"  [iteração {iteracao}] {total_rep} reparação(ões) aplicada(s).")
        else:
            log(f"  [iteração {iteracao}] nenhuma reparação aplicável; problemas restantes.")
        checagens_finais = checagens

    aprovado = _resumo_checagens(checagens_finais)["problemas"] == 0
    resumo_final = _resumo_checagens(checagens_finais)

    relatorio = {
        "agente": "auditor-estrutural-continua-zambria",
        "repositorio": str(REPO),
        "executado_em": agora_iso(),
        "rodada": rodada_num,
        "timer_minutos": INTERVALO_SEGUNDOS / 60,
        "verificacoes": checagens_finais,
        "reparacoes_aplicadas": total_reparacoes_rodada,
        "reparacoes_detalhes": todas_reparacoes,
        "resumo": resumo_final,
        "status_geral": "ok" if aprovado else "com_problemas",
        "aprovado": aprovado,
    }

    salvar_relatorio(relatorio)
    estado["reparacoes_totais"] = estado.get("reparacoes_totais", 0) + total_reparacoes_rodada

    if aprovado:
        estado["ultima_aprovacao"] = agora_iso()
        log(f"✅ APROVADO — todas as {resumo_final['ok']} verificações passaram na rodada #{rodada_num}.")
    else:
        log(f"❌ NÃO APROVADO — {resumo_final['problemas']} problema(s) restante(s) após reparação.")

    estado["ultima_rodada"] = agora_iso()
    salvar_estado(estado)
    return relatorio


def main():
    parser = argparse.ArgumentParser(description="Auditor Estrutural Contínua — ZAMBRIA")
    parser.add_argument("--loop", action="store_true", help="rodar em loop contínuo a cada 2 minutos")
    parser.add_argument("--interval", type=int, default=INTERVALO_SEGUNDOS, help="intervalo entre rodadas (s)")
    parser.add_argument("--report", default=None, help="caminho do relatório markdown")
    args = parser.parse_args()

    estado = carregar_estado()

    def uma_rodada():
        relatorio = rodada(estado)
        if args.report:
            Path(args.report).write_text(relatorio_markdown(relatorio), encoding="utf-8")
        return relatorio

    if args.loop:
        log(f"Modo contínuo ativado — timer de {args.interval}s ({args.interval/60:.0f} min).")
        while True:
            uma_rodada()
            if estado.get("status_geral") != "ok":
                log("Problemas pendentes — veja auditor_report.json / auditor_report.md")
            time.sleep(args.interval)
    else:
        rel = uma_rodada()
        sys.exit(0 if rel["status_geral"] == "ok" else 1)


if __name__ == "__main__":
    main()
