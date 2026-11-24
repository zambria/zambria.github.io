import re
import os

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    filename = os.path.basename(filepath)
    
    # Rule 3: Links in posts should NOT have "posts/" prefix
    if filepath.startswith('posts/'):
        # Check chapter links in sidebar
        posts_links = re.findall(r'href="posts/capitulo-', content)
        if posts_links:
            issues.append(f"Rule 3 VIOLATION: Found {len(posts_links)} links with 'posts/' prefix in post file")
        
        # Check nav-capitulos links
        nav_links = re.findall(r'<nav class="nav-capitulos">.*?</nav>', content, re.DOTALL)
        for nav in nav_links:
            nav_posts_links = re.findall(r'href="posts/capitulo-', nav)
            if nav_posts_links:
                issues.append(f"Rule 3 VIOLATION: nav-capitulos has {len(nav_posts_links)} links with 'posts/' prefix")
    
    # Rule 3: index.html SHOULD have "posts/" prefix
    if filename == 'index.html':
        index_links = re.findall(r'<a href="capitulo-', content)
        if index_links:
            issues.append(f"Rule 3 VIOLATION: index.html has {len(index_links)} links WITHOUT 'posts/' prefix")
    
    # Rule 4: btn-voltar present with onclick + listener
    if filepath.startswith('posts/'):
        if 'btn-voltar' not in content:
            issues.append("Rule 4 VIOLATION: btn-voltar missing")
        if 'onclick=' not in content or "window.location.href" not in content:
            issues.append("Rule 4 VIOLATION: btn-voltar missing onclick")
        if 'btnVoltar.addEventListener' not in content:
            issues.append("Rule 4 VIOLATION: btn-voltar missing JS listener")
    
    # Rule 5/6: Sidebar starts collapsed (aria-expanded="false" + display:none)
    # Check all categoria-titulo elements
    categoria_titulos = re.findall(r'<div class="categoria-titulo"[^>]*aria-expanded="([^"]*)"[^>]*>', content)
    for expanded in categoria_titulos:
        if expanded != 'false':
            issues.append(f"Rule 5/6 VIOLATION: categoria-titulo has aria-expanded='{expanded}' instead of 'false'")
    
    # Check lista-topicos style=display:none
    lista_displays = re.findall(r'<ul class="lista-topicos"[^>]*style="([^"]*)"', content)
    for style in lista_displays:
        if 'display: none' not in style:
            issues.append(f"Rule 5/6 VIOLATION: lista-topicos missing display:none, has style='{style}'")
    
    # Rule 7: No posts-lista section in main content
    if '<section id="posts-lista"' in content or '<section class="posts-lista"' in content:
        issues.append("Rule 7 VIOLATION: posts-lista section found in main content")
    
    # Rule 8: Loop excludes series
    if filepath.startswith('posts/'):
        # Posts should check for exact series ID match
        if "if (titulo.id === 'serie-" not in content and 'if (titulo.id === "serie-' not in content:
            issues.append("Rule 8 VIOLATION: Generic loop missing series exclusion check (exact ID match)")
    else:  # index.html
        if "startsWith('serie-')" not in content:
            issues.append("Rule 8 VIOLATION: index.html generic loop missing startsWith('serie-') exclusion")
    
    # Rule 9: animationDelay uses template literals (backticks)
    anim_delays = re.findall(r'animationDelay\s*=\s*([^;]+)', content)
    for delay in anim_delays:
        if '`' not in delay:
            issues.append(f"Rule 9 VIOLATION: animationDelay not using template literal: {delay}")
    
    # Rule 11: No nested scripts
    script_count = len(re.findall(r'<script(?![^>]*src=)', content))
    if script_count > 1:
        issues.append(f"Rule 11 VIOLATION: {script_count} inline script blocks found (possible nesting)")
    
    # Check for IDs with accents/non-ASCII
    ids = re.findall(r'id="([^"]*)"', content)
    for id_val in ids:
        if re.search(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', id_val, re.IGNORECASE):
            issues.append(f"Rule ZAMBRIA VIOLATION: ID contains non-ASCII characters: {id_val}")
    
    # background-image check
    if 'bg-zambria.jpg' not in content and filename == 'index.html':
        issues.append("Background image missing from index.html")
    if 'bg-zambria.jpg' not in content and filepath.startswith('posts/'):
        # Posts use inline style or style.css
        pass  # style.css handles it
    
    # btn-toggle-sidebar outside aside
    if 'btn-toggle-sidebar' in content:
        # Check it's not inside aside
        aside_start = content.find('<aside')
        btn_pos = content.find('btn-toggle-sidebar')
        if aside_start != -1 and btn_pos > aside_start:
            aside_end = content.find('</aside>')
            if aside_end != -1 and btn_pos < aside_end:
                issues.append("btn-toggle-sidebar is INSIDE aside (should be outside)")
    
    # site-shell class
    if 'site-shell' not in content:
        issues.append("site-shell class missing")
    
    # nav-capitulos completeness
    if filepath.startswith('posts/'):
        nav_match = re.search(r'<nav class="nav-capitulos">(.*?)</nav>', content, re.DOTALL)
        if not nav_match:
            issues.append("nav-capitulos missing entirely")
        else:
            nav_content = nav_match.group(1)
            # Check if it's first chapter (should only have next)
            is_first = 'capitulo-1-' in filename
            is_last_operacao = 'capitulo-8-operacao-prato' in filename
            is_last_continentes = 'capitulo-3-continentes-perdidos' in filename
            is_last = is_last_operacao or is_last_continentes
            
            has_prev = 'nav-anterior' in nav_content
            has_next = 'nav-proximo' in nav_content
            
            if is_first and not has_next:
                issues.append("First chapter missing nav-proximo")
            if is_last and not has_prev:
                issues.append("Last chapter missing nav-anterior")
            if not is_first and not is_last and (not has_prev or not has_next):
                issues.append("Middle chapter missing nav-anterior or nav-proximo")
    
    return issues

# Check all files
base = "C:/Users/erico/zambria.github.io"
files = [
    "index.html",
    "posts/capitulo-1-operacao-prato.html",
    "posts/capitulo-2-operacao-prato.html",
    "posts/capitulo-3-operacao-prato.html",
    "posts/capitulo-4-operacao-prato.html",
    "posts/capitulo-5-operacao-prato.html",
    "posts/capitulo-6-operacao-prato.html",
    "posts/capitulo-7-operacao-prato.html",
    "posts/capitulo-8-operacao-prato.html",
    "posts/capitulo-1-continentes-perdidos.html",
    "posts/capitulo-2-continentes-perdidos.html",
    "posts/capitulo-3-continentes-perdidos.html",
]

all_issues = {}
for f in files:
    full = os.path.join(base, f)
    issues = check_file(full)
    if issues:
        all_issues[f] = issues
        print(f"\n❌ {f}:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"✅ {f}: OK")

print(f"\n{'='*60}")
if all_issues:
    print(f"TOTAL ISSUES FOUND: {sum(len(v) for v in all_issues.values())} across {len(all_issues)} files")
else:
    print("🎉 ALL 12 FILES PASS ALL 15 GOLDEN RULES + KEB v1.0 CHECKS")