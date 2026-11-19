#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Agente publicador (zambria.github.io)

Lê conteúdos aprovados em /review/, aplica o tom editorial ZAMBRIA
(sério, sombrio, adulto formal, sarcástico às vezes), insere um
comentário breve do agente em momentos de suspense, garante fontes no
final, gera o post em /posts/, atualiza index.html com a lista de posts,
move o fonte para /publicados/ e respeita o limite de 2 posts por dia.

Execução: python publicador.py
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import html
from datetime import date
from pathlib import Path

# --------------------------- caminhos ---------------------------
REPO = Path(__file__).resolve().parent
REVIEW_DIR = REPO / "review"
PENDENTES_DIR = REVIEW_DIR / "pendentes"
POSTS_DIR = REPO / "posts"
PUBLICADOS_DIR = REPO / "publicados"
INDEX_FILE = REPO / "index.html"
ESTADO_FILE = REPO / "estado-publicador.json"
TOPICS_FILE = REPO / "topics.json"

POSTS_POR_DIA = 2

# --------------------------- tom editorial ZAMBRIA ---------------------------
# Comentários breves do agente em momentos de suspense (sem opinião, apenas reação).
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

SUSPENSE_CUES = [
    "mistério", "mistérios", "desconhecido", "desconhecida",
    "não identificado", "não identificada", "não identificados", "não identificadas",
    "permanece", "permanecem", "inquietante", "inquietantes", "sombrio", "sombrios",
    "sem resposta", "sem respostas", "sem explicação", "sem explicações",
    "segredo", "segredos", "oculto", "ocultos", "aberta", "abertas",
]
SARCASTIC_CUES = [
    "governo", "pentágono", "estados unidos", "sigiloso", "sigilosa", "secreto",
    "secretos", "ocultação", "encobrimento", "cobertura", "conspiração", "conspiracao",
    "classificado", "classificados", "arquivo secreto", "arquivos secretos",
]


def log(msg):
    print(f"[publicador] {msg}")


# --------------------------- estado / limite diário ---------------------------
def carregar_estado():
    if ESTADO_FILE.exists():
        try:
            return json.loads(ESTADO_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"ultima_publicacao": None, "posts_hoje": 0, "total_publicados": 0}


def salvar_estado(estado):
    ESTADO_FILE.write_text(
        json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def resetar_contador_diario(estado):
    hoje = date.today().isoformat()
    if estado.get("ultima_publicacao") != hoje:
        estado["ultima_publicacao"] = hoje
        estado["posts_hoje"] = 0
    return estado


def limite_atingido(estado):
    return estado.get("posts_hoje", 0) >= POSTS_POR_DIA


# --------------------------- frontmatter / slug ---------------------------
def parse_frontmatter(texto):
    """Retorna (metadados_dict, corpo_markdown)."""
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


def slugify(titulo):
    slug = re.sub(r"[^a-z0-9]+", "-", (titulo or "post").lower()).strip("-")
    return slug or "post"


def ler_fontes(meta, corpo):
    """Coleta fontes consultadas: frontmatter `fontes` ou seção ## Fontes consultadas no corpo."""
    fontes = []
    fonte_bruta = meta.get("fontes")
    if fonte_bruta:
        for item in re.split(r"[;\n]", fonte_bruta):
            item = item.strip()
            if item:
                fontes.append(item)
    if not fontes:
        m = re.search(
            r"##\s*Fontes consultadas\s*\n(.*?)(?=\n##\s|\Z)",
            corpo,
            re.DOTALL | re.IGNORECASE,
        )
        if m:
            bloco = m.group(1)
            for linha in bloco.splitlines():
                linha = linha.strip().lstrip("- ").strip()
                if linha:
                    fontes.append(linha)
    return fontes


# --------------------------- markdown -> blocos HTML ---------------------------
def md_para_blocos(texto):
    """Converte markdown simples para uma lista de blocos HTML (strings)."""
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
            blocos.append(f"<h3>{html.escape(linha[4:].strip())}</h3>")
        elif linha.startswith("## "):
            blocos.append(f"<h2>{html.escape(linha[3:].strip())}</h2>")
        elif linha.startswith("# "):
            blocos.append(f"<h1>{html.escape(linha[2:].strip())}</h1>")
        elif linha.startswith("> "):
            conteudo = linha[2:].strip()
            conteudo = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", conteudo)
            blocos.append(f"<blockquote>{conteudo}</blockquote>")
        elif linha.startswith("- "):
            blocos.append(f"<li>{html.escape(linha[2:].strip())}</li>")
        else:
            conteudo = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", linha)
            conteudo = html.escape(conteudo)
            # html.escape escapa os <b> que acabamos de criar; reabri-los:
            conteudo = conteudo.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
            blocos.append(f"<p>{conteudo}</p>")
    # agrupa li consecutivos em ul
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


def tem_suspense(bloco):
    baixo = bloco.lower()
    return any(cue in baixo for cue in SUSPENSE_CUES) or "..." in bloco or "…" in bloco


def escolher_comentario(texto_inteiro):
    baixo = texto_inteiro.lower()
    if any(cue in baixo for cue in SARCASTIC_CUES):
        grupo = "sarcastico"
    elif any(cue in baixo for cue in SUSPENSE_CUES):
        grupo = "sombrio"
    else:
        grupo = "padrao"
    import random

    return random.choice(COMENTARIOS[grupo])


# --------------------------- geração do post HTML ---------------------------
def ler_resumo(corpo_md):
    """Primeiro parágrafo do corpo como resumo simples."""
    primeiro = ""
    for linha in corpo_md.split("\n"):
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            primeiro = linha
            break
    primeiro = re.sub(r"\*\*(.+?)\*\*", r"\1", primeiro)
    if len(primeiro) > 220:
        primeiro = primeiro[:217].rstrip() + "..."
    return html.escape(primeiro)


def ler_tempo_leitura(texto):
    palavras = len(re.findall(r"\S+", texto))
    minutos = max(1, round(palavras / 200))
    return minutos


def gerar_html_post(titulo, categoria, data, corpo_html, resumo, slug):
    minutos = ler_tempo_leitura(corpo_html)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(titulo)} — ZAMBRIA</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <div class="site-shell">

    <aside class="sidebar">
      <div class="site-title">ZAMBRIA</div>
      <div class="site-subtitle">O Insólito Presente</div>
      <nav class="nav-posts">
        <a href="../index.html" style="display:block; margin-bottom:2rem; color:var(--text); text-decoration:none; border-bottom:1px solid var(--border); padding-bottom:0.5rem;">← Voltar ao início</a>
      </nav>
    </aside>

    <main class="conteudo">
      <article class="post">
        <div class="post-meta">
          <span class="categoria">{html.escape(categoria)}</span>
          <span>{html.escape(data)}</span>
          <span>Leitura: ~{minutos} min</span>
        </div>
        <h2>{html.escape(titulo)}</h2>
        <div class="texto">
          {corpo_html}
        </div>
        <p class="resumo">{resumo}</p>
      </article>
    </main>

  </div>

</body>
</html>"""


# --------------------------- index.html ---------------------------
def artigo_index(slug, titulo, categoria, data, resumo):
    return (
        "<article class=\"post\">\n"
        "        <div class=\"post-meta\">\n"
        f"          <span class=\"categoria\">{html.escape(categoria)}</span>\n"
        f"          <span>{html.escape(data)}</span>\n"
        "        </div>\n"
        f"        <h2><a href=\"posts/{slug}.html\">{html.escape(titulo)}</a></h2>\n"
        f"        <p>{resumo}</p>\n"
        "      </article>"
    )


def atualizar_index(slug, titulo, categoria, data, resumo):
    texto = INDEX_FILE.read_text(encoding="utf-8")
    novo = artigo_index(slug, titulo, categoria, data, resumo)

    artigos_existentes = re.findall(
        r"<article class=\"post\">.*?</article>", texto, re.DOTALL
    )
    artigos_existentes = [a for a in artigos_existentes if "Nenhum post publicado" not in a]

    lista_partes = [novo] + artigos_existentes
    lista = "\n".join(lista_partes)

    # remove o bloco vazio quando já há pelo menos um post real
    texto_sem_vazio = re.sub(
        r"<div class=\"vazio\">.*?</div>\s*", "", texto, flags=re.DOTALL
    )

    marcador = "<section id=\"posts-lista\">"
    pos = texto_sem_vazio.find(marcador)
    if pos == -1:
        log("AVISO: seção #posts-lista não encontrada no index.html.")
        return False
    depois = texto_sem_vazio[pos + len(marcador):]
    # retira comentário de placeholder e artigos antigos (já estão em lista)
    depois = depois.replace(
        "<!-- Posts serão injetados aqui pelo agente publicador -->", ""
    )
    depois = re.sub(r"<article class=\"post\">.*?</article>\s*", "", depois, flags=re.DOTALL)
    depois = depois.strip()
    texto_final = (
        texto_sem_vazio[: pos + len(marcador)]
        + "\n              "
        + lista
        + "\n            "
        + depois
    )
    INDEX_FILE.write_text(texto_final, encoding="utf-8")
    return True


# --------------------------- git ---------------------------
def git(*args):
    return subprocess.run(
        ["git"] + list(args), cwd=str(REPO), capture_output=True, text=True
    )


def commit_e_push(arquivos, mensagem, remover=()):
    for arq in remover:
        git("rm", "--quiet", arq)
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


# --------------------------- fluxo principal ---------------------------
def publicar():
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    PUBLICADOS_DIR.mkdir(parents=True, exist_ok=True)

    estado = carregar_estado()
    estado = resetar_contador_diario(estado)

    if limite_atingido(estado):
        log(
            f"Limite diário atingido ({estado['posts_hoje']}/{POSTS_POR_DIA}). "
            "Nenhum post publicado hoje."
        )
        salvar_estado(estado)
        return

    pendentes = sorted(PENDENTES_DIR.glob("*.md"))
    if not pendentes:
        log("Nenhum conteúdo aprovado pendente em /review/.")
        salvar_estado(estado)
        return

    publicados_hoje = 0
    arquivos_git = []

    for caminho in pendentes:
        if publicados_hoje >= POSTS_POR_DIA:
            break

        texto = caminho.read_text(encoding="utf-8")
        meta, corpo = parse_frontmatter(texto)

        titulo = meta.get("titulo") or meta.get("title") or caminho.stem
        categoria = meta.get("categoria") or meta.get("category") or "geral"
        slug = meta.get("slug") or slugify(titulo)
        data = meta.get("data", date.today().isoformat())

        blocos = md_para_blocos(corpo)

        # comentário breve do agente no primeiro momento de suspense
        comentario_html = ""
        for idx, bloco in enumerate(blocos):
            if tem_suspense(bloco):
                comentario = escolher_comentario(" ".join(blocos))
                comentario_html = (
                    '<div class="comentario-agente">'
                    f"{html.escape(comentario)}"
                    "</div>"
                )
                blocos.insert(idx + 1, comentario_html)
                break

        # fontes no final
        fontes = ler_fontes(meta, corpo)
        fontes_html = ""
        if fontes:
            itens = "\n".join(
                f'<li><a href="{html.escape(f)}" target="_blank" rel="noopener">{html.escape(f)}</a></li>'
                if f.startswith("http")
                else f"<li>{html.escape(f)}</li>"
                for f in fontes
            )
            fontes_html = (
                '<div class="fontes">\n'
                "<h4>Fontes consultadas</h4>\n"
                "<ul>\n" + itens + "\n</ul>\n"
                "</div>"
            )
        else:
            fontes_html = (
                '<div class="fontes">\n'
                "<h4>Fontes consultadas</h4>\n"
                "<p>Nenhuma fonte registrada no conteúdo.</p>\n"
                "</div>"
            )

        corpo_html = "\n".join(blocos) + "\n" + fontes_html
        resumo = ler_resumo(corpo)

        html_post = gerar_html_post(titulo, categoria, data, corpo_html, resumo, slug)

        post_path = POSTS_DIR / f"{slug}.html"
        post_path.write_text(html_post, encoding="utf-8")

        if not atualizar_index(slug, titulo, categoria, data, resumo):
            salvar_estado(estado)
            return

        # arquiva o fonte em /publicados/ e remove de /review/
        destino = PUBLICADOS_DIR / caminho.name
        shutil.move(str(caminho), str(destino))

        arquivos_git.extend([str(post_path), str(INDEX_FILE), str(destino), str(ESTADO_FILE)])
        publicados_hoje += 1
        log(f"Post gerado: {post_path.name}")

    if not arquivos_git:
        salvar_estado(estado)
        return

    estado["posts_hoje"] = estado.get("posts_hoje", 0) + publicados_hoje
    estado["total_publicados"] = estado.get("total_publicados", 0) + publicados_hoje
    salvar_estado(estado)

    arquivos_git.append(str(ESTADO_FILE))
    arquivos_git = list(dict.fromkeys(arquivos_git))  # dedupe, ordem preservada

    remover = [str(p) for p in pendentes[:publicados_hoje]]
    mensagem = f"[Publicador] Publica {publicados_hoje} post(s): {', '.join(Path(a).stem for a in arquivos_git if a.endswith('.html'))}"
    if commit_e_push(arquivos_git, mensagem, remover=remover):
        log("Publicação concluída com sucesso.")
    else:
        log("Falha na publicação (commit/push).")


if __name__ == "__main__":
    publicar()
