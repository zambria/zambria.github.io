import re
import os

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Rule 3: Links internos em posts/ nunca usam prefixo posts/
    if 'posts/capitulo-' in content and 'href="posts/posts/' in content:
        issues.append("REGRA 3 VIOLADA: Link com prefixo duplicado posts/posts/")
    
    # Rule 4: Botão Voltar em TODO post
    if 'btn-voltar' not in content:
        issues.append("REGRA 4 VIOLADA: Botão Voltar ausente")
    elif 'onclick=' not in content or 'window.location.href=' not in content:
        issues.append("REGRA 4 VIOLADA: Botão Voltar sem onclick direto")
    
    # Rule 5: aria-expanded deve bater com style=display
    # Check for aria-expanded="false" with style="display: block" or vice versa
    aria_false_display_block = re.search(r'aria-expanded="false"[^>]*style="[^"]*display:\s*block', content)
    aria_true_display_none = re.search(r'aria-expanded="true"[^>]*style="[^"]*display:\s*none', content)
    if aria_false_display_block:
        issues.append("REGRA 5 VIOLADA: aria-expanded=false mas style=display:block")
    if aria_true_display_none:
        issues.append("REGRA 5 VIOLADA: aria-expanded=true mas style=display:none")
    
    # Rule 6: Categorias da sidebar fechadas por padrão
    # All lista-topicos should have style="display: none" and aria-expanded="false"
    lista_topicos = re.findall(r'<ul class="lista-topicos"[^>]*>', content)
    for lt in lista_topicos:
        if 'style="display: none"' not in lt:
            issues.append("REGRA 6 VIOLADA: lista-topicos sem display:none")
    
    categoria_titulos = re.findall(r'<div class="categoria-titulo"[^>]*>', content)
    for ct in categoria_titulos:
        if 'aria-expanded="false"' not in ct:
            issues.append("REGRA 6 VIOLADA: categoria-titulo sem aria-expanded=false")
    
    # Rule 7: Conteúdo principal apenas a hero - no posts-lista
    if 'posts-lista' in content:
        issues.append("REGRA 7 VIOLADA: Seção posts-lista presente")
    
    # Rule 8: Loop .categoria-titulo pular IDs de série
    if 'if (titulo.id' in content:
        if "startsWith('serie-')" not in content and "=== 'serie-" not in content:
            issues.append("REGRA 8 VIOLADA: Loop genérico não exclui IDs de série")
    
    # Rule 9: animationDelay sempre com template literal (crase)
    # Check for single quotes in animationDelay
    single_quote_animation = re.search(r"animationDelay\s*=\s*['\"][^`]*\$\{i", content)
    if single_quote_animation:
        issues.append("REGRA 9 VIOLADA: animationDelay com aspas simples em vez de template literal")
    
    # Rule 11: Nada avulso na raiz ou em posts/ - this is a filesystem check, not content
    
    # Rule 14: ID duplicados
    ids = re.findall(r'id="([^"]+)"', content)
    id_counts = {}
    for id_val in ids:
        id_counts[id_val] = id_counts.get(id_val, 0) + 1
    for id_val, count in id_counts.items():
        if count > 1:
            issues.append(f"REGRA 14 VIOLADA: ID duplicado '{id_val}' ({count} vezes)")
    
    # Check for nested scripts
    script_count = len(re.findall(r'<script>', content))
    if script_count > 1:
        issues.append(f"REGRA: Múltiplos blocos <script> ({script_count}) - verificar aninhamento")
    
    # Check AdSense script is properly closed
    adsense_scripts = re.findall(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"]*" crossorigin="anonymous"></script>', content)
    if not adsense_scripts and 'adsbygoogle.js' in content:
        issues.append("REGRA: Script AdSense malformado ou não fechado corretamente")
    
    # Check nav-capitulos exists for series chapters
    if 'nav-capitulos' not in content and 'capitulo-' in filepath:
        issues.append("REGRA: nav-capitulos ausente em capítulo de série")
    
    # Check btn-voltar has z-index: 10000
    if 'btn-voltar' in content and 'z-index: 10000' not in content:
        issues.append("REGRA: btn-voltar sem z-index: 10000")
    
    # Check background-image bg-zambria.jpg preserved
    if 'bg-zambria.jpg' not in content and 'index.html' in filepath:
        issues.append("REGRA: background-image bg-zambria.jpg ausente no index.html")
    
    return issues

# Audit all files
files = [
    'index.html',
    'posts/capitulo-1-operacao-prato.html',
    'posts/capitulo-2-operacao-prato.html',
    'posts/capitulo-3-operacao-prato.html',
    'posts/capitulo-4-operacao-prato.html',
    'posts/capitulo-5-operacao-prato.html',
    'posts/capitulo-6-operacao-prato.html',
    'posts/capitulo-7-operacao-prato.html',
    'posts/capitulo-8-operacao-prato.html',
    'posts/capitulo-1-continentes-perdidos.html',
    'posts/capitulo-2-continentes-perdidos.html',
    'posts/capitulo-3-continentes-perdidos.html',
]

all_issues = {}
for filepath in files:
    full_path = f'C:/Users/erico/zambria.github.io/{filepath}'
    issues = audit_file(full_path)
    if issues:
        all_issues[filepath] = issues
        print(f"\n❌ {filepath}:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"✅ {filepath}: OK")

print(f"\n{'='*60}")
print(f"RESUMO: {len(files) - len(all_issues)}/{len(files)} arquivos sem violações")
if all_issues:
    print(f"ARQUIVOS COM PROBLEMAS: {len(all_issues)}")
else:
    print("TODOS OS ARQUIVOS EM CONFORMIDADE COM AS 15 REGRAS DE OURO")