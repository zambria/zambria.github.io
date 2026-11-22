#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Curador-Chefe do ZAMBRIA — O Insólito Presente.
Cerebro estratégico: decide o que entra, quando sai, desempata Escritor/Revisor,
direciona pesquisas e controla o fluxo de publicacao (sem limite diario).
"""

import json
import os
from datetime import datetime, timezone, timedelta

WORKDIR = r"C:\Users\erico\zambria.github.io"
TOPICS_PATH = os.path.join(WORKDIR, "topics.json")
DRAFTED_PATH = os.path.join(WORKDIR, "drafted.json")
ESTADO_PESQ_PATH = os.path.join(WORKDIR, "estado-pesquisador.json")
ESTADO_PUB_PATH = os.path.join(WORKDIR, "estado-publicador.json")
DECISOES_LOG = os.path.join(WORKDIR, "logs", "curador", "decisoes.jsonl")
PESQUISAS_DIR = os.path.join(WORKDIR, "pesquisas")
DRAFTS_DIR = os.path.join(WORKDIR, "drafts")
REVIEW_PENDENTES = os.path.join(WORKDIR, "review", "pendentes")
REVIEW_PUBLICADOS = os.path.join(WORKDIR, "review", "publicados")

LIMITE_POSTS_DIA = 999


def agora_iso():
    return datetime.now(timezone(timedelta(hours=-3))).isoformat()


def ler_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def escrever_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def registrar_decisao(registro):
    os.makedirs(os.path.dirname(DECISOES_LOG), exist_ok=True)
    with open(DECISOES_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def topicos_nao_pesquisados(topics, drafted):
    """Retorna topicos que ainda nao foram pesquisados."""
    nao_pesquisados = []
    for t in topics.get("topicos", []):
        if t.get("id") not in drafted.get("drafted", []):
            nao_pesquisados.append(t)
    return nao_pesquisados


def categorias_abandonadas(estado_pesq, topicos, horas=24):
    """Retorna IDs de categorias sem busca recente."""
    agora = datetime.now(timezone(timedelta(hours=-3)))
    abandonadas = set()
    for t in topicos.get("topicos", []):
        cat_id = t.get("categoria")
        ultimo = estado_pesq.get("ultima_busca", {}).get(cat_id)
        if not ultimo:
            abandonadas.add(cat_id)
        else:
            try:
                dt = datetime.fromisoformat(ultimo)
                if (agora - dt).total_seconds() > horas * 3600:
                    abandonadas.add(cat_id)
            except Exception:
                abandonadas.add(cat_id)
    return abandonadas


def main():
    registro = {
        "timestamp": agora_iso(),
        "acao": "curador-chefe",
        "topico_selecionado": None,
        "categoria": None,
        "motivo": None,
        "agente_direcionado": None,
        "bloqueio": None,
    }

    # 1. Leitura dos arquivos de entrada
    topics = ler_json(TOPICS_PATH)
    drafted = ler_json(DRAFTED_PATH) or {"drafted": [], "processados": []}
    estado_pesq = ler_json(ESTADO_PESQ_PATH) or {}
    estado_pub = ler_json(ESTADO_PUB_PATH) or {"posts_hoje": 0, "ultima_publicacao": None}

    if not topics:
        registro["bloqueio"] = "topics.json nao encontrado"
        registrar_decisao(registro)
        print("[ERRO] topics.json nao encontrado.")
        return

    # 2. Verificar posts hoje
    hoje = datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d")
    posts_hoje = estado_pub.get("posts_hoje", 0)
    ultima_pub = estado_pub.get("ultima_publicacao")

    if ultima_pub != hoje:
        posts_hoje = 0

    # 3. Escolha do próximo topico para pesquisa
    nao_pesquisados = topicos_nao_pesquisados(topics, drafted)
    abandonadas = categorias_abandonadas(estado_pesq, topics)

    topico_escolhido = None

    # Prioridade 1: nunca pesquisados
    if nao_pesquisados:
        # Prefere categorias abandonadas
        for t in nao_pesquisados:
            if t.get("categoria") in abandonadas:
                topico_escolhido = t
                break
        if not topico_escolhido:
            topico_escolhido = nao_pesquisados[0]
        registro["motivo"] = "topico nunca pesquisado (prioridade categoria abandonada)" if topico_escolhido.get("categoria") in abandonadas else "topico nunca pesquisado"
    else:
        # Todos pesquisados: verificar se Pesquisador Ativo trouxe novidades
        registro["motivo"] = "todos os topicos ja foram pesquisados"
        registro["agente_direcionado"] = "pesquisador-ativo (buscar novidades externas)"
        registrar_decisao(registro)
        print("[INFO] Todos os topicos ja pesquisados. Aguardando Pesquisador Ativo trazer novidades.")
        return

    registro["topico_selecionado"] = topico_escolhido.get("titulo")
    registro["topico_id"] = topico_escolhido.get("id")
    registro["categoria"] = topico_escolhido.get("categoria")

    # 4. Verificar gargalo de revisao
    pendentes = []
    if os.path.isdir(REVIEW_PENDENTES):
        pendentes = [f for f in os.listdir(REVIEW_PENDENTES) if f.endswith(".md") and not f.endswith("_revisao.md")]

    if pendentes:
        registro["agente_direcionado"] = "revisor-editorial"
        registro["motivo"] += f"; {len(pendentes)} texto(s) aguardando revisao"
    elif posts_hoje < LIMITE_POSTS_DIA:
        registro["agente_direcionado"] = "publicador-github"
        registro["motivo"] += f"; espaco para {LIMITE_POSTS_DIA - posts_hoje} post(s) hoje"
    else:
        registro["agente_direcionado"] = "pesquisador-profundo"
        registro["motivo"] += "; limite diario atingido, aguardando proximo dia"

    # 5. Direcionar Pesquisador Profundo para o topico escolhido
    registro["agente_direcionado"] = "pesquisador-profundo"
    registro["detalhes"] = {
        "topico_id": topico_escolhido.get("id"),
        "topico": topico_escolhido.get("titulo"),
        "categoria": topico_escolhido.get("categoria"),
    }

    registrar_decisao(registro)
    print(f"[Curador-Chefe] Topico selecionado: {topico_escolhido['titulo']} ({topico_escolhido['categoria']})")
    print(f"[Curador-Chefe] Motivo: {registro['motivo']}")
    print(f"[Curador-Chefe] Agente direcionado: {registro['agente_direcionado']}")
    print(f"[Curador-Chefe] Posts hoje: {posts_hoje}/{LIMITE_POSTS_DIA}")


if __name__ == "__main__":
    main()
