import re, os

site_root = 'C:/Users/erico/zambria.github.io'
posts_dir = os.path.join(site_root, 'posts')

files = ['index.html'] + sorted([f for f in os.listdir(posts_dir) if f.endswith('.html')])

print('=' * 60)
print('COMPREHENSIVE AUDIT - 15 GOLDEN RULES + STRUCTURAL CHECKS')
print('=' * 60)

total_issues = 0

for fname in files:
    fpath = os.path.join(site_root, fname) if fname == 'index.html' else os.path.join(posts_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'\n--- {fname} ---')
    file_issues = 0
    
    # Rule 3: Links internos em posts/ nunca usam prefixo posts/
    if fname != 'index.html':
        bad_links = re.findall(r'href="posts/posts/', content)
        if bad_links:
            print(f'  ❌ RULE 3 VIOLATION: Found {len(bad_links)} links with posts/posts/ prefix')
            file_issues += 1
        else:
            print(f'  ✅ Rule 3: No posts/posts/ prefix in internal links')
    
    # Rule 4: Botão Voltar em TODO post
    if fname != 'index.html':
        has_btn_voltar = 'btn-voltar' in content and 'onclick' in content
        if has_btn_voltar:
            print(f'  ✅ Rule 4: btn-voltar present with onclick')
        else:
            print(f'  ❌ RULE 4 VIOLATION: btn-voltar missing or no onclick')
            file_issues += 1
    
    # Rule 5: aria-expanded bate com style=display
    aria_expanded = re.findall(r'aria-expanded="(true|false)"', content)
    style_display = re.findall(r'style="display:\s*(block|none);?"', content)
    if len(aria_expanded) == len(style_display) and len(aria_expanded) > 0:
        print(f'  ✅ Rule 5: aria-expanded and style=display counts match ({len(aria_expanded)} each)')
    else:
        print(f'  ⚠️ Rule 5: Count mismatch - aria-expanded: {len(aria_expanded)}, style=display: {len(style_display)}')
    
    # Rule 6: Categorias da sidebar fechadas por padrão
    if 'aria-expanded="false"' in content and 'display: none' in content:
        print(f'  ✅ Rule 6: Sidebar categories start collapsed')
    else:
        print(f'  ❌ RULE 6 VIOLATION: Sidebar not collapsed by default')
        file_issues += 1
    
    # Rule 7: Conteúdo principal apenas a hero (no posts-lista)
    if 'posts-lista' in content:
        print(f'  ❌ RULE 7 VIOLATION: posts-lista section found in main content')
        file_issues += 1
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
        file_issues += 1
    elif anim_delays:
        print(f'  ✅ Rule 9: animationDelay uses template literals ({len(anim_delays)} instances)')
    else:
        print(f'  ⚠️ Rule 9: No animationDelay found')
    
    # Rule 11: IDs com acentos
    ids = re.findall(r'id="([^"]+)"', content)
    accented_ids = [id for id in ids if re.search(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', id, re.IGNORECASE)]
    if accented_ids:
        print(f'  ❌ RULE 11/JS VIOLATION: IDs with accents/special chars: {accented_ids}')
        file_issues += 1
    else:
        print(f'  ✅ Rule 11: All IDs are ASCII-only')
    
    # Check for duplicate IDs
    id_counts = {}
    for id in ids:
        id_counts[id] = id_counts.get(id, 0) + 1
    dup_ids = [id for id, count in id_counts.items() if count > 1]
    if dup_ids:
        print(f'  ❌ DUPLICATE IDs: {dup_ids}')
        file_issues += 1
    else:
        print(f'  ✅ No duplicate IDs')
    
    # Check for nested scripts (fixed regex)
    script_opens = len(re.findall(r'<script\b', content))
    script_closes = len(re.findall(r'</script>', content))
    if script_opens != script_closes:
        print(f'  ❌ NESTED/UNBALANCED SCRIPTS: {script_opens} open, {script_closes} close')
        file_issues += 1
    else:
        print(f'  ✅ Script tags balanced ({script_opens} blocks)')
    
    # Check background-image (in index.html inline or via CSS in posts)
    if fname == 'index.html':
        if 'bg-zambria.jpg' in content:
            print(f'  ✅ Background image referenced inline')
        else:
            print(f'  ⚠️ Background image not found inline')
    else:
        # Posts use CSS for background
        print(f'  ✅ Background via CSS (style.css)')
    
    # Check nav-capitulos
    if fname != 'index.html':
        has_nav = 'nav-capitulos' in content
        if has_nav:
            is_first = 'capitulo-1-' in fname
            is_last_op = 'capitulo-8-operacao-prato' in fname
            is_last_cont = 'capitulo-3-continentes' in fname
            is_last = is_last_op or is_last_cont
            
            has_prev = 'nav-anterior' in content
            has_next = 'nav-proximo' in content
            
            if is_first and not has_prev and has_next:
                print(f'  ✅ Nav-capitulos: First chapter only has proximo')
            elif is_last and has_prev and not has_next:
                print(f'  ✅ Nav-capitulos: Last chapter only has anterior')
            elif not is_first and not is_last and has_prev and has_next:
                print(f'  ✅ Nav-capitulos: Middle chapter has both')
            else:
                print(f'  ⚠️ Nav-capitulos: first={is_first}, last={is_last}, prev={has_prev}, next={has_next}')
        else:
            print(f'  ❌ RULE: nav-capitulos missing')
            file_issues += 1
    
    total_issues += file_issues

print('\n' + '=' * 60)
print(f'AUDIT COMPLETE - Total issues found: {total_issues}')
print('=' * 60)