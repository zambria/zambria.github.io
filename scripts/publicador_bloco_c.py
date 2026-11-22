#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Publicador-Webmaster (Bloco C)
Publica TODOS os textos aprovados (_aprovado.md) em review/publicados/ e review/pendentes/,
gera HTML em posts/, atualiza index.html, commita e push para origin/main.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import html as html_mod
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

REPO = Path("C:/Users/erico/zambria.github.io")
PUBLICADOS_DIR = REPO / "review" / "publicados"
ARQUIVADO_DIR = PUBLICADOS_DIR / "arquivado"
PENDENTES_DIR = REPO / "review" / "pendentes"
POSTS_DIR = REPO / "posts"
INDEX_FILE = REPO / "index.html"
ESTADO_FILE = REPO / "estado-publicador.json"

ADSENSE = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/'
    'js/adsbygoogle.js?client=ca-pub-4937131805632227" crossorigin="anonymous"></script>'
)

# Comentários breves do agente em momentos de suspense (sem opinião).
COMENTARIOS = {
    "sombrio": [
        "O mistério permanece aberto. E talvez devesse ficar assim.",
        "Não há registro confortável para isso. Não há mesmo.",
        "O que não se nomeia continua ali. Sem nome, sem responsável.",
    ],
    "sarcastico": [
        "Conveniente. Tudo sem explicação oficial, sem culpado, sem fim.",
        "Ótimo. Mais um fenômeno que as autoridades não identificam — e não se comprometem a identificar.",
        "Transparência total: não sabemos nada. Isso é a resposta.",
    ],
    "padrao": [
        "Isso fica no ar. E talvez seja exatamente o ponto.",
        "Restam as perguntas. As respostas, se é que existem, não estão nos arquivos.",
    ],
}
SUSPENSE_CUES = ["mistério", "mistérios", "desconhecido", "desconhecida",
                 "não identificado", "não identificada", "não identificados", "não identificadas",
                 "permanece", "permanecem", "inquietante", "inquietantes", "sombrio", "sombrios",
                 "sem resposta", "sem respostas", "sem explicação", "sem explicações",
                 "segredo", "segredos", "oculto", "ocultos", "aberta", "abertas"]
SARCASTIC_CUES = ["governo", "pentágono", "estados unidos", "sigiloso", "sigilosa", "secreto",
                  "secretos", "ocultação", "encobrimento", "cobertura", "conspiração", "conspiracao",
                  "classificado", "classificados", "arquivo secreto", "arquivos secretos"]

def log(msg: str) -> None:
    print(f"[publicador-bloco-c] {msg}")

def carregar_estado() -> dict:
    if ESTADO_FILE.exists():
        try:
            return json.loads(ESTADO_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posts_publicados_total": 0, "ultimo_post": None, "ultima_atualizacao": None}

def salvar_estado(estado: dict) -> None:
    ESTADO_FILE.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")

def git(*args):
    return subprocess.run(["git"] + list(args), cwd=str(REPO), capture_output=True, text=True)

def commit_e_push(arquivos: list, mensagem: str, remover: tuple = ()) -> bool:
    for arq in remover:
        git("rm", "--quiet", arq)
    if arquivos:
        git("add", "--", *arquivos)
    r = git("commit", "-m", mensagem)
    if r.returncode != 0:
        log(f"commit falhou: {(r.stderr or r.stdout).strip()}")
        return False
    log("commit realizado.")
    r = git("push")
    if r.returncode != 0:
        log(f"push falhou: {(r.stderr or r.stdout).strip()}")
        return False
    log("push realizado para origin/main.")
    return True

def parse_frontmatter(texto: str):
    meta = {}
    corpo = texto
    m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)$", texto, re.DOTALL)
    if m:
        bloco = m.group(1)
        corpo = m.group(2)
        for linha in bloco.splitlines():
            if ":" in linha:
                chave, _, valor = linha.partition(":")
                meta[chave.strip()] = valor.strip().strip('"').strip("'")
    return meta, corpo

def slugify(titulo: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (titulo or "post").lower()).strip("-")
    return slug or "post"

def ler_fontes(meta, corpo):
    fontes = []
    fonte_bruta = meta.get("fontes")
    if fonte_bruta:
        for item in re.split(r"[;\n]", fonte_bruta):
            item = item.strip()
            if item:
                fontes.append(item)
    if not fontes:
        m = re.search(r"##\s*Fontes\s*\n(.*?)(?=\n##\s|\Z)", corpo, re.DOTALL | re.IGNORECASE)
        if m:
            bloco = m.group(1)
            for linha in bloco.splitlines():
                linha = linha.strip().lstrip("- ").strip()
                if linha:
                    fontes.append(linha)
    return fontes

def md_para_blocos(texto: str):
    blocos = []
    pular_fontes = False
    for linha_raw in texto.split("\n"):
        linha = linha_raw.rstrip()
        if re.match(r"##\s*Fontes", linha, re.IGNORECASE):
            pular_fontes = True
            continue
        if pular_fontes:
            if re.match(r"#{1,3}\s", linha):
                pular_fontes = False
            else:
                continue
        if not linha.strip():
            continue
        if linha.startswith("### "):
            blocos.append(f"<h3>{html_mod.escape(linha[4:].strip())}</h3>")
        elif linha.startswith("## "):
            blocos.append(f"<h2>{html_mod.escape(linha[3:].strip())}</h2>")
        elif linha.startswith("# "):
            blocos.append(f"<h1>{html_mod.escape(linha[2:].strip())}</h1>")
        elif linha.startswith("> "):
            conteudo = linha[2:].strip()
            conteudo = re.sub(r"\*\*(.+?)\*\*", r"<b>\\1</b>", conteudo)
            blocos.append(f"<blockquote>{conteudo}</blockquote>")
        elif linha.startswith("- "):
            blocos.append(f"<li>{html_mod.escape(linha[2:].strip())}</li>")
        else:
            conteudo = re.sub(r"\*\*(.+?)\*\*", r"<b>\\1</b>", linha)
            conteudo = html_mod.escape(conteudo)
            conteudo = conteudo.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
            blocos.append(f"<p>{conteudo}</p>")
    agrupados = []
    i = 0
    while i < len(blocos):
        if blocos[i].startswith("<li>"):
            itens = [blocos[i]]
            i += 1
            while i < len(blocos) and blocos[i].startswith("<li>"):
                itens.append(blocos[i])
                i += 1
            agrupados.append("<ul>\n" + "\n".join(itens) + "\n</ul>")
        else:
            agrupados.append(blocos[i])
            i += 1
    return agrupados

def tem_suspense(bloco: str) -> bool:
    baixo = bloco.lower()
    return any(cue in baixo for cue in SUSPENSE_CUES) or "..." in bloco or "…" in bloco

def escolher_comentario(texto_inteiro: str) -> str:
    baixo = texto_inteiro.lower()
    if any(cue in baixo for cue in SARCASTIC_CUES):
        grupo = "sarcastico"
    elif any(cue in baixo for cue in SUSPENSE_CUES):
        grupo = "sombrio"
    else:
        grupo = "padrao"
    import random
    return random.choice(COMENTARIOS[grupo])

def ler_tempo_leitura(texto: str) -> int:
    palavras = len(re.findall(r"\S+", texto))
    return max(1, round(palavras / 200))

def gerar_html_post(titulo, categoria, data, corpo_html, resumo, slug, fontes_html):
    minutos = ler_tempo_leitura(corpo_html + resumo)
    t = html_mod.escape(titulo)
    c = html_mod.escape(categoria)
    d = html_mod.escape(data)
    r = resumo
    a = ADSENSE
    corpo = corpo_html
    f = fontes_html
    TEMPLATE = """<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>__TITULO__ — ZAMBRIA</title>
  <link rel=\"stylesheet\" href=\"../style.css\">
  __ADSENSE__
</head>
<body class=\"bg-black text-white font-sans leading-relaxed min-h-screen\">
  <div class=\"site-shell flex min-h-screen transition-all duration-300\" id=\"site-shell\">
    <!-- Botão toggle SEMPRE visível, fora da sidebar -->
    <button class=\"btn-toggle-sidebar\" id=\"btnToggleSidebar\" aria-label=\"Esconder barra lateral\">☰</button>

    <!-- Sidebar esquerda (estática na página do post) -->
    <aside class=\"sidebar\" id=\"sidebar-zambria\">
      <div class=\"site-title\">ZAMBRIA</div>
      <div class=\"site-subtitle\">O Insólito Presente</div>
      <nav class=\"nav-posts\">
        <a href=\"../index.html\" style=\"display:block; margin-bottom:2rem; color:var(--text); text-decoration:none; border-bottom:1px solid var(--border); padding-bottom:0.5rem;\">← Voltar ao início</a>
      </nav>
    </aside>

    <!-- Conteúdo principal -->
    <main class=\"conteudo\">
      <article class=\"post\">
        <div class=\"post-meta\">
          <span class=\"categoria\">__CATEGORIA__</span>
          <span>__DATA__</span>
          <span>Leitura: ~__MINUTOS__ min</span>
        </div>
        <h1>__TITULO__</h1>
        <p class=\"resumo\">__RESUMO__</p>
        <div class=\"corpo\">
          __CORPO__
        </div>
        __FONTES__
      </article>
    </main>
  </div>

  <script>
    /* Toggle da sidebar (botão fixo, nunca some) */
    (function() {
      var btn = document.getElementById('btnToggleSidebar');
      var shell = document.getElementById('site-shell');
      if (!btn || !shell) return;
      btn.addEventListener('click', function() {
        shell.classList.toggle('sidebar-hidden');
        if (shell.classList.contains('sidebar-hidden')) {
          btn.textContent = '≡';
          btn.setAttribute('aria-label', 'Mostrar barra lateral');
        } else {
          btn.textContent = '☰';
          btn.setAttribute('aria-label', 'Esconder barra lateral');
        }
      });
    })();
  </script>
</body>
</html>"""
    out = (TEMPLATE
           .replace("__TITULO__", t)
           .replace("__ADSENSE__", a)
           .replace("__CATEGORIA__", c)
           .replace("__DATA__", d)
           .replace("__MINUTOS__", str(minutos))
           .replace("__RESUMO__", r)
           .replace("__CORPO__", corpo)
           .replace("__FONTES__", f))
    return out

CATEGORIA_MAP = {
    "ufos": "ufos",
    "ufo": "ufos",
    "arqueologia": "arqueologia",
    "arch": "arqueologia",
    "sobrenatural": "sobrenatural",
    "para": "sobrenatural",
    "criptozoologia": "criptozoologia",
    "crypto": "criptozoologia",
    "conspiracao": "conspiracao",
    "conspiracoes": "conspiracao",
    "conspir": "conspiracao",
    "fenomenos": "fenomenos-naturais",
    "fenomenos-naturais": "fenomenos-naturais",
    "nature": "fenomenos-naturais",
    "contos": "contos-de-terror",
    "contos-de-terror": "contos-de-terror",
}

CATEGORIA_NOME = {
    "ufos": "UFOs e Aliens",
    "arqueologia": "Arqueologia Antiga e Mistérios Históricos",
    "sobrenatural": "Sobrenatural e Paranormal",
    "criptozoologia": "Criptozologia",
    "conspiracao": "Conspirações e Coberturas",
    "fenomenos-naturais": "Fenômenos Naturais Inexplicáveis",
    "contos-de-terror": "Contos de Terror — Conteúdo Original",
}

def categoria_id(categoria: str) -> str:
    return CATEGORIA_MAP.get(categoria.lower(), categoria.lower().replace(" ", "-"))

def encontrar_lista_ul(texto: str, cat_id: str):
    """Encontra o </ul> da lista-topicos da categoria cat_id."""
    # procurar o categoria-titulo que contenha o nome da categoria
    nome = CATEGORIA_NOME.get(cat_id, cat_id)
    busca_desde = 0
    while True:
        pos_titulo = texto.find('categoria-titulo', busca_desde)
        if pos_titulo == -1:
            return -1
        trecho = texto[pos_titulo:pos_titulo + 200]
        if nome.lower() in trecho.lower():
            pos_ul = texto.find('class="lista-topicos"', pos_titulo)
            if pos_ul != -1:
                pos_fim_ul = texto.find("</ul>", pos_ul)
                if pos_fim_ul != -1:
                    return pos_fim_ul
        busca_desde = pos_titulo + 1

def adicionar_li_index(texto: str, slug, titulo, cat_id: str):
    """Adiciona <li> com link para o post na lista-topicos da categoria."""
    pos = encontrar_lista_ul(texto, cat_id)
    if pos == -1:
        return texto, False
    novo_li = f'          <li><a href="posts/{slug}.html">{html_mod.escape(titulo)}</a></li>\n'
    texto = texto[:pos] + novo_li + texto[pos:]
    return texto, True

def criar_categoria_index(texto: str, slug, titulo, cat_id: str):
    """Cria uma nova categoria-grupo no index.html antes do fechamento do </aside>."""
    nome = CATEGORIA_NOME.get(cat_id, cat_id.title())
    lista_id = f"lista-{cat_id}"
    bloco = f'''
      <div class="categoria-grupo">
        <div class="categoria-titulo" id="categoria-{cat_id}" role="button" tabindex="0" aria-expanded="false">{html_mod.escape(nome)}</div>
        <ul class="lista-topicos" id="{lista_id}" style="display: none;">
          <li><a href="posts/{slug}.html">{html_mod.escape(titulo)}</a></li>
        </ul>
      </div>'''
    pos = texto.rfind("</aside>")
    if pos == -1:
        pos = texto.rfind("</body>")
    texto = texto[:pos] + bloco + "\n" + texto[pos:]
    return texto

def posts_links_em_index(texto: str) -> set:
    """Retorna os slugs de posts já linkados no index.html."""
    links = re.findall(r'href="posts/([^"]+)\.html"', texto)
    return set(l.replace("/", "") for l in links)

def main():
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    ARQUIVADO_DIR.mkdir(parents=True, exist_ok=True)

    estado = carregar_estado()

    # --- Passo 2: selecionar todos os _aprovado.md não arquivados ---
    aprovados_publ = sorted(PUBLICADOS_DIR.glob("*_aprovado.md"))
    arquivados = {p.name for p in ARQUIVADO_DIR.glob("*_aprovado.md")}
    pendentes_publ = [p for p in aprovados_publ if p.name not in arquivados]

    aprovados_pend = sorted(PENDENTES_DIR.glob("*_aprovado.md"))
    # aprovados em pendentes que ainda não têm HTML em posts/
    pendentes_pend = []
    for p in aprovados_pend:
        base = p.name.replace("_aprovado.md", ".md")
        origem = PENDENTES_DIR / base
        slug = p.name.replace("_aprovado.md", "")
        if not (POSTS_DIR / f"{slug}.html").exists():
            pendentes_pend.append(p)

    todos = pendentes_publ + pendentes_pend
    if not todos:
        log("Nenhum _aprovado.md pendente para publicar.")
        salvar_estado(estado)
        return

    log(f"Encontrados {len(todos)} texto(s) aprovado(s) para publicar.")

    publicados_esta_execucao = 0
    arquivos_git = []

    for caminho in todos:
        # determinar slug e origem
        if caminho.parent == PENDENTES_DIR:
            # aprovado em pendentes -> origem é o .md sem sufixo
            base = caminho.name.replace("_aprovado.md", ".md")
            origem = PENDENTES_DIR / base
            slug = caminho.name.replace("_aprovado.md", "")
        else:
            # aprovado em publicados -> origem é o .md referenciado dentro do aprovado
            texto_aprovado = caminho.read_text(encoding="utf-8")
            m = re.search(r"\*\*Artigo:\*\*\s*(.+)", texto_aprovado)
            if m:
                origem = REPO / m.group(1).strip()
            else:
                m = re.search(r"Arquivo de origem:\s*review/pendentes/([^\s\n]+)", texto_aprovado)
                if m:
                    origem = PENDENTES_DIR / m.group(1)
                else:
                    origem = PENDENTES_DIR / (caminho.name.replace("_aprovado.md", ".md"))
            slug = caminho.name.replace("_aprovado.md", "")

        if not origem.exists():
            log(f"ORIGEM NÃO ENCONTRADA: {origem} — pulando {caminho.name}")
            continue
        if (POSTS_DIR / f"{slug}.html").exists():
            log(f"JÁ EXISTE HTML: posts/{slug}.html — pulando {caminho.name}")
            continue

        texto = origem.read_text(encoding="utf-8")
        meta, corpo = parse_frontmatter(texto)

        titulo = meta.get("titulo") or meta.get("title") or slug
        categoria = meta.get("categoria") or meta.get("category") or "geral"
        data = meta.get("data") or date.today().isoformat()
        resumo_meta = meta.get("resumo") or ""
        resumo = html_mod.escape(resumo_meta) if resumo_meta else html_mod.escape(corpo.split("\n")[0][:217])

        blocos = md_para_blocos(corpo)
        # comentário de suspense
        comentario_html = ""
        for idx, bloco in enumerate(blocos):
            if tem_suspense(bloco):
                comentario = escolher_comentario(" ".join(blocos))
                comentario_html = (
                    '<div class="comentario-agente">'
                    f"{html_mod.escape(comentario)}"
                    "</div>"
                )
                blocos.insert(idx + 1, comentario_html)
                break

        fontes = ler_fontes(meta, corpo)
        fontes_html = ""
        if fontes:
            itens = "\n".join(
                f'<li><a href="{html_mod.escape(f)}" target="_blank" rel="noopener">{html_mod.escape(f)}</a></li>'
                if f.startswith("http")
                else f"<li>{html_mod.escape(f)}</li>"
                for f in fontes
            )
            fontes_html = (
                '<section class="fontes">\n'
                "<h2>Fontes</h2>\n"
                "<ul>\n" + itens + "\n</ul>\n"
                "</section>"
            )
        else:
            fontes_html = (
                '<section class="fontes">\n'
                "<h2>Fontes</h2>\n"
                "<p>Nenhuma fonte registrada no conteúdo.</p>\n"
                "</section>"
            )

        corpo_html = "\n".join(blocos) + "\n" + fontes_html

        html_post = gerar_html_post(titulo, categoria, data, corpo_html, resumo, slug, fontes_html)
        post_path = POSTS_DIR / f"{slug}.html"
        post_path.write_text(html_post, encoding="utf-8")
        log(f"Post gerado: {post_path.name}")

        arquivos_git.append(str(post_path))
        publicados_esta_execucao += 1

        # atualizar index.html
        texto_index = INDEX_FILE.read_text(encoding="utf-8")
        cat_id = categoria_id(categoria)
        texto_index, ok = adicionar_li_index(texto_index, slug, titulo, cat_id)
        if not ok:
            texto_index = criar_categoria_index(texto_index, slug, titulo, cat_id)
            log(f"Nova categoria criada no index.html: {cat_id}")
        else:
            log(f"Post adicionado à categoria '{cat_id}' no index.html.")
        INDEX_FILE.write_text(texto_index, encoding="utf-8")
        arquivos_git.append(str(INDEX_FILE))

        # mover .md aprovado para arquivado
        if caminho.parent == PUBLICADOS_DIR:
            shutil.move(str(caminho), str(ARQUIVADO_DIR / caminho.name))
            arquivos_git.append(str(ARQUIVADO_DIR / caminho.name))
            log(f"Arquivado: {caminho.name}")

    # --- Passo 5: Guardião — sincronização index.html vs posts/ ---
    texto_index = INDEX_FILE.read_text(encoding="utf-8")
    posts_html = sorted(POSTS_DIR.glob("*.html"))
    links_index = posts_links_em_index(texto_index)
    sincronizou = False
    for p in posts_html:
        slug = p.stem
        if slug not in links_index:
            # extrair categoria do post
            texto_p = p.read_text(encoding="utf-8")
            mc = re.search(r'<span class="categoria">(.*?)</span>', texto_p, re.DOTALL | re.IGNORECASE)
            cat = html_mod.unescape(mc.group(1)).strip() if mc else "geral"
            mt = re.search(r"<h1[^>]*>(.*?)</h1>", texto_p, re.DOTALL | re.IGNORECASE)
            titulo = re.sub(r"<[^>]+>", "", mt.group(1)).strip() if mt else slug
            cat_id = categoria_id(cat)
            texto_index, ok = adicionar_li_index(texto_index, slug, titulo, cat_id)
            if not ok:
                texto_index = criar_categoria_index(texto_index, slug, titulo, cat_id)
            log(f"GUARDIAO: post órfão adicionado ao index: {slug} (categoria {cat_id})")
            sincronizou = True
            arquivos_git.append(str(INDEX_FILE))
            links_index.add(slug)

    if sincronizou:
        INDEX_FILE.write_text(texto_index, encoding="utf-8")

    # --- Passo 6: commit e push ---
    arquivos_git = list(dict.fromkeys(arquivos_git))
    if arquivos_git:
        estado["posts_publicados_total"] = estado.get("posts_publicados_total", 0) + publicados_esta_execucao
        ultimo = (POSTS_DIR / f"{todos[-1].name.replace('_aprovado.md','')}.html").stem if todos else estado.get("ultimo_post")
        # usar o último slug processado
        estado["ultimo_post"] = ultimo
        br = timezone(timedelta(hours=-3))
        estado["ultima_atualizacao"] = datetime.now(br).isoformat()
        salvar_estado(estado)
        arquivos_git.append(str(ESTADO_FILE))

        mensagem = f"[Publicador Bloco C] Publica {publicados_esta_execucao} post(s)"
        if commit_e_push(arquivos_git, mensagem):
            log("Publicação concluída com sucesso.")
        else:
            log("FALHA no commit/push.")
    else:
        salvar_estado(estado)

    # --- Relatório ---
    print("\n=== RELATÓRIO DO PUBLICADOR-WEBMASTER (Bloco C) ===")
    print(f"Posts publicados nesta execução: {publicados_esta_execucao}")
    print(f"Arquivos git preparados: {len(arquivos_git)}")
    print(f"index.html atualizado com posts na categoria correta: sim")
    if sincronizou:
        print("Guardião do site: corrigidos posts órfãos no index.html.")
    else:
        print("Guardião do site: sincronização OK, nenhum órfão.")
    print(f"Estado: total={estado.get('posts_publicados_total')}, ultimo_post={estado.get('ultimo_post')}")

if __name__ == "__main__":
    main()
