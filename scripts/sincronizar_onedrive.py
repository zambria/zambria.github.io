#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronizador ZAMBRIA — espelha o trabalho da equipe do workdir para o OneDrive.
Permite que o usuário acompanhe o progresso em tempo real.
"""

import shutil
import os
from datetime import datetime, timezone, timedelta

WORKDIR = r"C:\Users\erico\zambria.github.io"
ONEDRIVE = r"C:\Users\erico\OneDrive\Documentos\PROJETO-Z4W3R14\ZAMBRIA - INSÓLITO"

MAPEAMENTO = {
    "pesquisas": "pesquisas",           # Pesquisador Ativo -> pesquisas
    "drafts": "rascunhos",              # Pesquisador Profundo -> rascunhos
    "review/pendentes": "revisados",    # Escritor/Revisor -> revisados
    "posts": "publicados",              # Publicador -> publicados
    "topics.json": "temas/topics.json", # Curador-Chefe -> temas
}

def agora_iso():
    return datetime.now(timezone(timedelta(hours=-3))).isoformat()

def sincronizar():
    print(f"[{agora_iso()}] Iniciando sincronização ZAMBRIA -> OneDrive")
    
    for origem_rel, destino_rel in MAPEAMENTO.items():
        origem = os.path.join(WORKDIR, origem_rel)
        destino = os.path.join(ONEDRIVE, destino_rel)
        
        if os.path.isdir(origem):
            # Sincronizar diretório
            os.makedirs(destino, exist_ok=True)
            for arquivo in os.listdir(origem):
                src = os.path.join(origem, arquivo)
                dst = os.path.join(destino, arquivo)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"  [OK] {origem_rel}/{arquivo} -> {destino_rel}/")
        elif os.path.isfile(origem):
            # Sincronizar arquivo único
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origem, destino)
            print(f"  [OK] {origem_rel} -> {destino_rel}")
        else:
            print(f"  [SKIP] {origem_rel} não encontrado (ainda não foi criado)")
    
    print(f"[{agora_iso()}] Sincronização concluída.")

if __name__ == "__main__":
    sincronizar()
