import re, os

site_root = 'C:/Users/erico/zambria.github.io'
posts_dir = os.path.join(site_root, 'posts')

files = ['index.html'] + sorted([f for f in os.listdir(posts_dir) if f.endswith('.html')])

print('=' * 60)
print('COMPREHENSIVE AUDIT - 15 GOLDEN RULES + STRUCTURAL CHECKS')
print('=' * 60)

for fname in files:
    fpath = os.path.join(site_root, fname) if fname == 'index.html' else os.path.join(posts_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'\n--- {fname} ---')
    
    # Rule 3: Links internos em posts/ nunca usam prefixo posts/
    if fname != 'index.html':
        bad_links = re.findall(r'href="posts/posts/', content)
        if bad_links:
            print(f'  ❌ RULE 3 VIOLATION: Found {len(bad_links)} links with posts/posts/ prefix')
        else:
            print(f'  ✅ Rule 3: No posts/posts/ prefix in internal links')
    
    # Rule 4: Botão Voltar em TODO post
    if fname != 'index.html':
        has_btn_voltar = 'btn-voltar' in content and 'onclick' in content
        if has_btn_voltar:
            print(f'  ✅ Rule 4: btn-voltar present with onclick')
        else:
            print(f'  ❌ RULE 4 VIOLATION: btn-voltar missing or no onclick')
    
    # Rule 5: aria-expanded bate com style=display
    aria_expanded = re.findall(r'aria-expanded="(true|false)"', content)
    style_display = re.findall(r'style="display: (block|none)"', content)
    if len(aria_expanded) == len(style_display) and len(aria_expanded) > 0:
        print(f'  ✅ Rule 5: aria-expanded and style=display counts match ({len(aria_expanded)} each)')
    else:
        print(f'  ⚠️ Rule 5: Count mismatch - aria-expanded: {len(aria_expanded)}, style=display: {len(style_display)}')
    
    # Rule 6: Categorias da sidebar fechadas por padrão
    if 'aria-expanded="false"' in content and 'style="display: none"' in content:
        print(f'  ✅ Rule 6: Sidebar categories start collapsed')
    else:
        print(f'  ❌ RULE 6 VIOLATION: Sidebar not collapsed by default')
    
    # Rule 7: Conteúdo principal apenas a hero (no posts-lista)
    if 'posts-lista' in content:
        print(f'  ❌ RULE 7 VIOLATION: posts-lista section found in main content')
    else:
        print(f'  ✅ Rule 7: No posts-lista in main content')
    
    # Rule 8: Loop .categoria-titulo pula IDs de série
    if 'if (titulo.id' in content and ('startsWith' in content or '===' in content):
        print(f'  ✅ Rule 8: Series handler excluded from generic loop')
    else:
        print(f'  ⚠️ Rule 8: Series exclusion check needed')
    
    # Rule 9: animationDelay com template literal (crase)
    anim_delays = re.findall(r'animationDelay\s*=\s*[`\']([^`\']*)[`\']', content)
    bad_delays = [d for d in anim_delays if '${' not in d and 'i *' in d]
    if bad_delays:
        print(f'  ❌ RULE 9 VIOLATION: animationDelay without template literal: {bad_delays}')
    elif anim_delays:
        print(f'  ✅ Rule 9: animationDelay uses template literals ({len(anim_delays)} instances)')
    else:
        print(f'  ⚠️ Rule 9: No animationDelay found')
    
    # Rule 11: IDs com acentos
    ids = re.findall(r'id="([^"]+)"', content)
    accented_ids = [id for id in ids if re.search(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', id, re.IGNORECASE)]
    if accented_ids:
        print(f'  ❌ RULE 11/JS VIOLATION: IDs with accents/special chars: {accented_ids}')
    else:
        print(f'  ✅ Rule 11: All IDs are ASCII-only')
    
    # Check for duplicate IDs
    id_counts = {}
    for id in ids:
        id_counts[id] = id_counts.get(id, 0) + 1
    dup_ids = [id for id, count in id_counts.items() if count > 1]
    if dup_ids:
        print(f'  ❌ DUPLICATE IDs: {dup_ids}')
    else:
        print(f'  ✅ No duplicate IDs')
    
    # Check for nested scripts
    script_count = len(re.findall(r'<script>', content))
    script_close_count = len(re.findall(r'</script>', content))
    if script_count != script_close_count:
        print(f'  ❌ NESTED/UNBALANCED SCRIPTS: {script_count} open, {script_close_count} close')
    else:
        print(f'  ✅ Script tags balanced ({script_count} blocks)')
    
    # Check background-image
    if 'bg-zambria.jpg' in content:
        print(f'  ✅ Background image referenced')
    else:
        print(f'  ⚠️ Background image not found in this file')
    
    # Check nav-capitulos
    if fname != 'index.html':
        has_nav = 'nav-capitulos' in content
        if has_nav:
            if 'capitulo-1' in fname and 'operacao-prato' in fname:
                has_prev = 'nav-anterior' in content
                has_next = 'nav-proximo' in content
                if not has_prev and has_next:
                    print(f'  ✅ Nav-capitulos: First chapter only has proximo')
                else:
                    print(f'  ⚠️ Nav-capitulos: First chapter has prev={has_prev}, next={has_next}')
            elif 'capitulo-8' in fname or 'capitulo-3-continentes' in fname:
                has_prev = 'nav-anterior' in content
                has_next = 'nav-proximo' in content
                if has_prev and not has_next:
                    print(f'  ✅ Nav-capitulos: Last chapter only has anterior')
                else:
                    print(f'  ⚠️ Nav-capitulos: Last chapter has prev={has_prev}, next={has_next}')
            else:
                has_prev = 'nav-anterior' in content
                has_next = 'nav-proximo' in content
                if has_prev and has_next:
                    print(f'  ✅ Nav-capitulos: Middle chapter has both')
                else:
                    print(f'  ⚠️ Nav-capitulos: Middle chapter has prev={has_prev}, next={has_next}')
        else:
            print(f'  ❌ RULE: nav-capitulos missing')

print('\n' + '=' * 60)
print('AUDIT COMPLETE')
print('=' * 60)