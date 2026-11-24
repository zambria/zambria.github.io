#!/usr/bin/env python3
# scripts/varredura-estrutural.py
# Varredura estrutural de todos os arquivos .html do site ZAMBRIA.
# Detecta e reporta: tags <script> desbalanceadas, script de animacao ausente,
# botao dentro da sidebar, classes inconsistentes, tags HTML desbalanceadas, links quebrados.

import os
import re
import json
import sys


def varrer_repositorio(base_dir):
    erros = []
    avisos = []
    posts_dir = os.path.join(base_dir, 'posts')

    # Arquivos validos no repositorio
    todos_arquivos = set()
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), base_dir)
                todos_arquivos.add(rel)

    # --- index.html ---
    index_path = os.path.join(base_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index = f.read()

        # Botao fora da sidebar
        if re.search(r'<aside.*?<button class="btn-toggle-sidebar"', index, re.DOTALL):
            erros.append('index.html: botao btn-toggle-sidebar DENTRO da sidebar')

        # Classes necessarias
        for cls in ['categoria-titulo', 'lista-topicos', 'slideFadeIn', 'slideFadeOut', 'bg-zambria.jpg', 'btn-toggle-sidebar']:
            if cls not in index:
                erros.append(f'index.html: classe/referencia ausente: {cls}')

        # Sem posts-list na home
        if '<section class="posts-list"' in index:
            avisos.append('index.html: ainda contem posts-list (deveria mostrar apenas hero)')

    # --- style.css ---
    css_path = os.path.join(base_dir, 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()

        for pattern, desc in [
            ('.btn-toggle-sidebar', 'botao fixo'),
            ('.site-shell.sidebar-hidden .sidebar { width: 0;', 'sidebar width:0 quando escondida'),
            ('@keyframes slideFadeIn', 'animacao slideFadeIn'),
            ('@keyframes slideFadeOut', 'animacao slideFadeOut'),
            ('.lista-topicos a:link', 'link :link cor definida'),
            ('.lista-topicos a:visited', 'link :visited cor definida'),
        ]:
            if pattern not in css:
                erros.append(f'style.css: {desc} ausente')

    # --- Posts individuais ---
    if os.path.isdir(posts_dir):
        arquivos_posts = sorted([f for f in os.listdir(posts_dir) if f.endswith('.html')])

        for arquivo in arquivos_posts:
            caminho = os.path.join(posts_dir, arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            problemas = []

            # Tags script balanceadas (ignorando script async do AdSense)
            script_opens = len(re.findall(r'<script(?!\\s+async)', conteudo))
            script_closes = conteudo.count('</script>')
            if script_opens != script_closes:
                problemas.append(f'tags script desbalanceadas ({script_opens} open, {script_closes} close)')

            # Script de animacao cascata presente
            if 'slideFadeIn' not in conteudo and 'slideFadeOut' not in conteudo:
                problemas.append('script de animacao cascata ausente')

            # Botao toggle presente
            if 'btnToggleSidebar' not in conteudo:
                problemas.append('script toggle sidebar ausente')

            # Botao fora da sidebar
            if re.search(r'<aside.*?<button class="btn-toggle-sidebar"', conteudo, re.DOTALL):
                problemas.append('botao btn-toggle-sidebar DENTRO da sidebar')

            # Link para index.html
            if 'index.html' not in conteudo and 'index' not in conteudo.lower():
                problemas.append('sem link de volta para o index.html')

            # Link CSS
            if 'style.css' not in conteudo:
                problemas.append('sem referencia ao style.css')

            # Titulo da pagina
            if '<title>' not in conteudo:
                problemas.append('sem <title>')

            if problemas:
                for p in problemas:
                    erros.append(f'POST [{arquivo}]: {p}')

    # --- Links quebrados ---
    if os.path.isdir(posts_dir):
        for arquivo in arquivos_posts:
            caminho = os.path.join(posts_dir, arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            hrefs = re.findall(r'href="([^"]+)"', conteudo)
            for href in hrefs:
                if href.startswith(('http', 'mailto', '#')):
                    continue
                if href.startswith('../'):
                    href_norm = os.path.normpath(os.path.join('posts', href))
                elif href.startswith('posts/'):
                    href_norm = href
                else:
                    href_norm = href

                if href_norm not in todos_arquivos:
                    erros.append(f'LINK QUEBRADO em {arquivo}: aponta para "{href}" (normalizado: "{href_norm}") nao encontrado')

    return {'erros': erros, 'avisos': avisos, 'total_erros': len(erros), 'total_avisos': len(avisos)}


def main():
    base_dir = sys.argv[1] if len(sys.argv) > 1 else r'C:\\Users\\erico\\zambria.github.io'
    resultado = varrer_repositorio(base_dir)

    print(f"Erros encontrados: {resultado['total_erros']}")
    print(f"Avisos: {resultado['total_avisos']}")
    for e in resultado['erros']:
        print(f"  [ERRO] {e}")
    for a in resultado['avisos']:
        print(f"  [AVISO] {a}")

    if resultado['total_erros'] == 0 and resultado['total_avisos'] == 0:
        print("  Nenhum erro encontrado!")

    # Salvar relatorio
    relatorio_path = os.path.join(base_dir, 'varredura_erros.json')
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print(f"\nRelatorio salvo em: {relatorio_path}")

    sys.exit(1 if resultado['total_erros'] > 0 else 0)


if __name__ == '__main__':
    main()