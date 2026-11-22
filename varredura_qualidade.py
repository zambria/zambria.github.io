#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAMBRIA — Equipe de varredura de qualidade (zambria.github.io)

Atua ANTES de qualquer post ser publicado: varre conteúdos em /review/
(aprovados, aguardando publicação) e aplica três agentes:

  1. Corretor ortográfico — revisa português, acentuação e concordância
     (correções automáticas de baixo risco + sugestões de revisão).
  2. Detetor de plágio — compara o texto com as fontes consultadas e
     sinaliza trechos que copiam a fonte palavra por palavra, para que
     sejam reescritos com palavras próprias.
  3. Avaliador de atratividade — verifica suspense, comentário breve do
     agente em momentos de interesse e fontes citadas no final.

Execução:
  python varredura_qualidade.py           # apenas relatório (não altera nada)
  python varredura_qualidade.py --aplicar # aplica correções ortográficas seguras
  python varredura_qualidade.py --arquivo review/<post>.md  # varre um arquivo só
"""

from __future__ import annotations

import difflib
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# --------------------------- caminhos ---------------------------
REPO = Path(__file__).resolve().parent
REVIEW_DIR = REPO / "review"
DRAFTS_DIR = REPO / "drafts"
POSTS_DIR = REPO / "posts"
PUBLICADOS_DIR = REPO / "publicados"
RELATORIO_JSON = REPO / "varredura_report.json"
RELATORIO_MD = REPO / "varredura_report.md"

# --------------------------- utilitários ---------------------------
def log(msg: str):
    print(f"[varredura] {msg}", flush=True)


def agora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ler_texto(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def parse_frontmatter(texto: str):
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


def ler_fontes(meta, corpo):
    """Coleta fontes: frontmatter `fontes` ou seção ## Fontes consultadas."""
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


# ==================== AGENTE 1: CORRETOR ORTOGRÁFICO ====================

# Pequenas correções seguras de português (acentuação e abreviações comuns).
# Apenas correções que realmente alteram o texto; entradas "sem alteração" foram
# removidas porque, com re.IGNORECASE, forçavam minúscula em nomes próprios
# (ex: "Estados" -> "estados").
# Formato: (padrao_regex, substituição, justificativa).
CORRECOES_SEGURAS = [
    # abreviações informais
    (r"\bpra\b", "para", "abreviação informal 'pra' -> 'para'"),
    (r"\bpro\b", "por o", "abreviação informal 'pro' -> 'por o'"),
    (r"\bnum\b", "não", "abreviação informal 'num' -> 'não' (contextual)"),
    # acento grave/agudo ausente
    (r"\bninguem\b", "ninguém", "acento: ninguem -> ninguém"),
    (r"\bnao\b", "não", "acento: nao -> não"),
    (r"\bacao\b", "ação", "acento: acao -> ação"),
    (r"\bacaoes\b", "ações", "acento/plural: acaoes -> ações"),
    (r"\binformacao\b", "informação", "acento: informacao -> informação"),
    (r"\binformacoes\b", "informações", "acento/plural: informacoes -> informações"),
    (r"\bexploracao\b", "exploração", "acento: exploracao -> exploração"),
    (r"\bexploracoes\b", "explorações", "acento/plural: exploracoes -> explorações"),
    (r"\binvestigacao\b", "investigação", "acento: investigacao -> investigação"),
    (r"\binvestigacoes\b", "investigações", "acento/plural: investigacoes -> investigações"),
    (r"\bpresenca\b", "presença", "acento: presenca -> presença"),
    (r"\bpresencas\b", "presenças", "acento/plural: presencas -> presenças"),
    (r"\bausencia\b", "ausência", "acento: ausencia -> ausência"),
    (r"\bausencias\b", "ausências", "acento/plural: ausencias -> ausências"),
    (r"\bevidencia\b", "evidência", "acento: evidencia -> evidência"),
    (r"\bevidencias\b", "evidências", "acento/plural: evidencias -> evidências"),
    (r"\bexplicacao\b", "explicação", "acento: explicacao -> explicação"),
    (r"\bexplicacoes\b", "explicações", "acento/plural: explicacoes -> explicações"),
    (r"\bfenomeno\b", "fenômeno", "acento: fenomeno -> fenômeno"),
    (r"\bfenomenos\b", "fenômenos", "acento/plural: fenomenos -> fenômenos"),
    (r"\bimportancia\b", "importância", "acento: importancia -> importância"),
    (r"\bimportancias\b", "importâncias", "acento/plural: importancias -> importâncias"),
    (r"\brelatorio\b", "relatório", "acento: relatorio -> relatório"),
    (r"\brelatorios\b", "relatórios", "acento/plural: relatorios -> relatórios"),
    (r"\banalise\b", "análise", "acento: analise -> análise"),
    (r"\banalises\b", "análises", "acento/plural: analises -> análises"),
    (r"\bconclusao\b", "conclusão", "acento: conclusao -> conclusão"),
    (r"\bconclusoes\b", "conclusões", "acento/plural: conclusoes -> conclusões"),
    (r"\bdecisao\b", "decisão", "acento: decisao -> decisão"),
    (r"\bdecisoes\b", "decisões", "acento/plural: decisoes -> decisões"),
    (r"\bsolucao\b", "solução", "acento: solucao -> solução"),
    (r"\bsolucoes\b", "soluções", "acento/plural: solucoes -> soluções"),
    (r"\bfuncionario\b", "funcionário", "acento: funcionario -> funcionário"),
    (r"\bfuncionarios\b", "funcionários", "acento/plural: funcionarios -> funcionários"),
    (r"\bpais\b", "país", "acento: pais -> país"),
    (r"\bpaises\b", "países", "acento/plural: paises -> países"),
    (r"\baviao\b", "avião", "acento: aviao -> avião"),
    (r"\bavioes\b", "aviões", "acento/plural: avioes -> aviões"),
    (r"\bconspiracao\b", "conspiração", "acento: conspiracao -> conspiração"),
    (r"\bconspiracoes\b", "conspirações", "acento/plural: conspiracoes -> conspirações"),
    (r"\bocultacao\b", "ocultação", "acento: ocultacao -> ocultação"),
    (r"\bocultacoes\b", "ocultações", "acento/plural: ocultacoes -> ocultações"),
]


URL_PATTERN = re.compile(r"https?://\S+")


def corrigir_ortografia(corpo: str):
    """Aplica correções seguras. Retorna (corpo_corrigido, lista_de_alteracoes).
    URLs são protegidas (não sofrem correção ortográfica) para não quebrar links."""
    alteracoes = []
    novo = corpo
    # protege URLs antes de qualquer correção
    placeholders = []

    def proteger(m):
        placeholders.append(m.group(0))
        return f"__URL{len(placeholders)-1}__"

    novo = URL_PATTERN.sub(proteger, novo)
    for padrao, repl, just in CORRECOES_SEGURAS:
        def sub(m):
            alteracoes.append(
                {"trecho_original": m.group(0), "correcao": repl, "justificativa": just}
            )
            return repl

        novo, n = re.subn(padrao, sub, novo, flags=re.IGNORECASE)
    # restaura URLs intactas
    for i, url in enumerate(placeholders):
        novo = novo.replace(f"__URL{i}__", url)
    return novo, alteracoes


def sugestoes_revisao(corpo: str):
    """Sugestões de revisão humana (não aplicadas automaticamente)."""
    sugestoes = []
    # concordância simples: artigos/plurais óbvios em torno de substantivos comuns
    padroes = [
        (r"\b(os|as) (mistérios|mistérios)\b", "verificar concordância artigo+substantivo"),
        (r"\b(um|uma) (mistérios|mistérios)\b", "verificar número: artigo singular com substantivo plural"),
        (r"\b(são|estão) (mistério|fenômeno|objeto|caso)\b", "verificar concordância verbo+substantivo"),
    ]
    for padrao, just in padroes:
        for m in re.finditer(padrao, corpo, flags=re.IGNORECASE):
            sugestoes.append(
                {"trecho": m.group(0), "justificativa": just}
            )
    return sugestoes


# ==================== AGENTE 2: DETETOR DE PLÁGIO ====================

def normalizar(texto: str) -> str:
    """Remove pontuação/acentos e deixa minúsculo para comparação."""
    t = texto.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fragmentos(texto: str, tamanho_minimo: int = 8):
    """Quebra em fragmentos de palavras para comparação de sequência."""
    palavras = normalizar(texto).split()
    return [palavras[i:i + tamanho_minimo] for i in range(len(palavras) - tamanho_minimo + 1)]


def trechos_copiados(corpo: str, fontes: list[str], tamanho_minimo: int = 8):
    """Compara cada fragmento do corpo com cada fonte; retorna trechos suspeitos."""
    corpo_frags = fragmentos(corpo, tamanho_minimo)
    suspeitos = []
    for fonte in fontes:
        fonte_normal = normalizar(fonte)
        if len(fonte_normal.split()) < tamanho_minimo:
            continue
        fonte_frags = fragmentos(fonte_normal, tamanho_minimo)
        fonte_set = {" ".join(f) for f in fonte_frags}
        for frag in corpo_frags:
            frag_texto = " ".join(frag)
            if frag_texto in fonte_set:
                suspeitos.append(
                    {"trecho": frag_texto, "fonte": fonte[:120]}
                )
    # dedupe preservando ordem
    vistos = set()
    unicos = []
    for s in suspeitos:
        chave = s["trecho"]
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(s)
    return unicos


# ==================== AGENTE 3: AVALIADOR DE ATRATIVIDADE ====================

SUSPENSE_CUES = [
    "mistério", "mistérios", "desconhecido", "desconhecida",
    "não identificado", "não identificada", "não identificados", "não identificadas",
    "permanece", "permanecem", "inquietante", "inquietantes", "sombrio", "sombrios",
    "sem resposta", "sem respostas", "sem explicação", "sem explicações",
    "segredo", "segredos", "oculto", "ocultos", "aberta", "abertas",
    "...", "…",
]
COMENTARIO_AGENTE_CUES = ["> *", "comentário do agente", "agente comenta"]


def tem_suspense(bloco: str) -> bool:
    baixo = bloco.lower()
    return any(cue in baixo for cue in SUSPENSE_CUES)


def avaliar_atratividade(corpo: str, fontes: list[str]):
    blocos = [b for b in corpo.split("\n") if b.strip()]
    suspense_encontrado = [b for b in blocos if tem_suspense(b)]
    tem_bloco_citacao = any(b.lstrip().startswith(">") for b in blocos)
    tem_fontes = len(fontes) > 0
    tem_titulo = bool(re.search(r"^#\s+.+", corpo, re.MULTILINE))

    suspense_ok = len(suspense_encontrado) > 0 or tem_bloco_citacao
    fontes_ok = tem_fontes

    nota = 0
    if tem_titulo:
        nota += 25
    if suspense_ok:
        nota += 35
    if fontes_ok:
        nota += 25
    if len(corpo.split()) >= 300:
        nota += 15

    problemas = []
    if not tem_titulo:
        problemas.append("Texto sem título (H1) claro.")
    if not suspense_ok:
        problemas.append("Sem suspense ou gancho que prenda o leitor (insira mistério, '...' ou citação bloqueada).")
    if not fontes_ok:
        problemas.append("Sem seção 'Fontes consultadas' no final.")

    return {
        "nota": nota,
        "aprovado": nota >= 75 and not problemas,
        "problemas": problemas,
        "suspense_encontrado": len(suspense_encontrado),
        "tem_bloco_citacao": tem_bloco_citacao,
        "tem_fontes": tem_fontes,
        "tem_titulo": tem_titulo,
        "palavras": len(corpo.split()),
    }


# ==================== ORQUESTRADOR ====================

def corpo_sem_fontes(corpo: str) -> str:
    """Remove a seção 'Fontes consultadas' do corpo para evitar falso positivo no plágio."""
    return re.sub(
        r"\n?##\s*Fontes consultadas\s*\n(.*?)(?=\n##\s|\Z)",
        "",
        corpo,
        flags=re.DOTALL | re.IGNORECASE,
    ).strip()


def varrer_arquivo(caminho: Path) -> dict:
    texto = ler_texto(caminho)
    meta, corpo = parse_frontmatter(texto)
    fontes = ler_fontes(meta, corpo)
    corpo_principal = corpo_sem_fontes(corpo)

    # Agente 1 — ortografia
    corpo_corrigido, alteracoes = corrigir_ortografia(corpo)
    sugestoes = sugestoes_revisao(corpo)

    # Agente 2 — plágio (compara apenas o corpo principal, não as citações de fonte)
    plagiados = trechos_copiados(corpo_principal, fontes)

    # Agente 3 — atratividade
    atratividade = avaliar_atratividade(corpo, fontes)

    return {
        "arquivo": str(caminho.name),
        "titulo": meta.get("titulo") or meta.get("title") or caminho.stem,
        "categoria": meta.get("categoria") or "geral",
        "status_frontmatter": meta.get("status") or "não informado",
        "agente_ortografia": {
            "alteracoes_aplicaveis": len(alteracoes),
            "alteracoes": alteracoes,
            "sugestoes_revisao_humana": sugestoes,
        },
        "agente_plagio": {
            "trechos_suspeitos": plagiados,
            "total_suspeitos": len(plagiados),
        },
        "agente_atratividade": atratividade,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Equipe de varredura de qualidade ZAMBRIA")
    parser.add_argument("--aplicar", action="store_true",
                        help="aplica correções ortográficas seguras automaticamente")
    parser.add_argument("--arquivo", default=None,
                        help="varre apenas este arquivo (ex: review/ufo-01.md)")
    args = parser.parse_args()

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    alvos = []
    if args.arquivo:
        p = Path(args.arquivo)
        if not p.is_absolute():
            p = REPO / p
        if p.exists():
            alvos = [p]
        else:
            log(f"arquivo não encontrado: {p}")
            sys.exit(1)
    else:
        alvos = sorted(REVIEW_DIR.glob("*.md"))

    if not alvos:
        log("Nenhum conteúdo para varrer em /review/.")
        RELATORIO_JSON.write_text(
            json.dumps({"executado_em": agora_iso(), "arquivos": [], "resumo": {"total": 0}},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        RELATORIO_MD.write_text("# Relatório de Varredura de Qualidade ZAMBRIA\n\nNenhum conteúdo encontrado em /review/.\n", encoding="utf-8")
        return

    resultados = []
    arquivos_alterados = []

    for caminho in alvos:
        log(f"Varredura: {caminho.name}")
        resultado = varrer_arquivo(caminho)
        resultados.append(resultado)

        if args.aplicar and resultado["agente_ortografia"]["alteracoes"]:
            # aplica correções apenas ao corpo, preservando o frontmatter original
            texto = ler_texto(caminho)
            m = re.match(r"(---\s*\n.*?\n---\s*\n)(.*)$", texto, re.DOTALL)
            if m:
                frontmatter_original = m.group(1)
                corpo = m.group(2)
            else:
                frontmatter_original = ""
                corpo = texto
            corpo_corrigido, _ = corrigir_ortografia(corpo)
            novo_texto = frontmatter_original + corpo_corrigido
            if not novo_texto.endswith("\n"):
                novo_texto += "\n"
            caminho.write_text(novo_texto, encoding="utf-8")
            arquivos_alterados.append(str(caminho.name))
            log(f"Correções ortográficas aplicadas em {caminho.name} "
                f"({len(resultado['agente_ortografia']['alteracoes'])} alterações).")

    relatorio = {
        "agente": "equipe-varredura-qualidade-zambria",
        "executado_em": agora_iso(),
        "modo": "aplicar" if args.aplicar else "apenas_relatorio",
        "arquivos_varridos": len(resultados),
        "arquivos_alterados": arquivos_alterados,
        "resumo": {
            "total_alteracoes_ortografia": sum(r["agente_ortografia"]["alteracoes_aplicaveis"] for r in resultados),
            "total_sugestoes_revisao": sum(len(r["agente_ortografia"]["sugestoes_revisao_humana"]) for r in resultados),
            "total_trechos_plagio_suspeitos": sum(r["agente_plagio"]["total_suspeitos"] for r in resultados),
            "atratividade_media": round(
                sum(r["agente_atratividade"]["nota"] for r in resultados) / len(resultados), 1
            ) if resultados else 0,
            "atratividade_aprovados": sum(1 for r in resultados if r["agente_atratividade"]["aprovado"]),
        },
        "arquivos": resultados,
    }

    RELATORIO_JSON.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    RELATORIO_MD.write_text(relatorio_markdown(relatorio), encoding="utf-8")

    resumo = relatorio["resumo"]
    log(
        f"Varredura concluída: {len(resultados)} arquivo(s), "
        f"{resumo['total_alteracoes_ortografia']} correção(ões) ortográfica(s) disponível(is), "
        f"{resumo['total_trechos_plagio_suspeitos']} trecho(s) suspeito(s) de plágio, "
        f"atratividade média {resumo['atratividade_media']}/100, "
        f"{resumo['atratividade_aprovados']} aprovado(s)."
    )
    log(f"Relatório: {RELATORIO_JSON.name} / {RELATORIO_MD.name}")


def relatorio_markdown(relatorio: dict) -> str:
    linhas = []
    linhas.append("# Relatório de Varredura de Qualidade — ZAMBRIA")
    linhas.append("")
    linhas.append(f"- **Agente:** {relatorio['agente']}")
    linhas.append(f"- **Executado em:** {relatorio['executado_em']}")
    linhas.append(f"- **Modo:** {relatorio['modo']}")
    linhas.append(f"- **Arquivos varridos:** {relatorio['arquivos_varridos']}")
    if relatorio["arquivos_alterados"]:
        linhas.append(f"- **Arquivos alterados:** {', '.join(relatorio['arquivos_alterados'])}")
    linhas.append("")
    linhas.append("## Resumo")
    r = relatorio["resumo"]
    linhas.append(f"- Correções ortográficas disponíveis: {r['total_alteracoes_ortografia']}")
    linhas.append(f"- Sugestões de revisão humana: {r['total_sugestoes_revisao']}")
    linhas.append(f"- Trechos suspeitos de plágio: {r['total_trechos_plagio_suspeitos']}")
    linhas.append(f"- Atratividade média: {r['atratividade_media']}/100")
    linhas.append(f"- Aprovados em atratividade: {r['atratividade_aprovados']}/{relatorio['arquivos_varridos']}")
    linhas.append("")
    linhas.append("## Detalhe por arquivo")
    for a in relatorio["arquivos"]:
        linhas.append(f"### {a['arquivo']} — {a['titulo']}")
        linhas.append(f"- Categoria: {a['categoria']} | Status frontmatter: {a['status_frontmatter']}")
        o = a["agente_ortografia"]
        linhas.append(f"- Ortografia: {o['alteracoes_aplicaveis']} correção(ões) disponível(is), {len(o['sugestoes_revisao_humana'])} sugestão(ões) de revisão humana")
        p = a["agente_plagio"]
        linhas.append(f"- Plágio: {p['total_suspeitos']} trecho(s) suspeito(s)")
        for s in p["trechos_suspeitos"][:5]:
            linhas.append(f"  - Suspeito: “{s['trecho']}” (fonte: {s['fonte']})")
        at = a["agente_atratividade"]
        status = "✅ APROVADO" if at["aprovado"] else "❌ REPROVADO"
        linhas.append(f"- Atratividade: {at['nota']}/100 — {status}")
        for prob in at["problemas"]:
            linhas.append(f"  - {prob}")
        linhas.append("")
    linhas.append("---")
    linhas.append("*Gerado pela Equipe de Varredura de Qualidade ZAMBRIA. Atua antes de qualquer post ser publicado.*")
    return "\n".join(linhas)


if __name__ == "__main__":
    main()
