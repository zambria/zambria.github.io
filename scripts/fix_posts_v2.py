#!/usr/bin/env python3
import os
import re

posts_dir = "C:/Users/erico/zambria.github.io/posts/"

# Define series structure with ACTUAL file names
series = {
    "operacao-prato": {
        "category": "Operação Prato",
        "cat_id": "categoria-operacao-prato",
        "list_id": "lista-operacao-prato",
        "serie_id": "serie-operacao-prato",
        "capitulos_id": "capitulos-operacao-prato",
        "chapters": [
            ("capitulo-1-operacao-prato.html", "Capítulo 1"),
            ("capitulo-2-operacao-prato.html", "Capítulo 2"),
            ("capitulo-3-operacao-prato.html", "Capítulo 3"),
            ("capitulo-4-operacao-prato.html", "Capítulo 4"),
            ("capitulo-5-operacao-prato.html", "Capítulo 5"),
        ]
    },
    "sete-alem": {
        "category": "Sete Além",
        "cat_id": "categoria-sete-alem",
        "list_id": "lista-sete-alem",
        "serie_id": "serie-sete-alem",
        "capitulos_id": "capitulos-sete-alem",
        "chapters": [
            ("capitulo-1-sete-alem.html", "Capítulo 1"),
            ("capitulo-2-sete-alem.html", "Capítulo 2"),
            ("capitulo-3-sete-alem.html", "Capítulo 3"),
        ]
    },
    "continentes-perdidos": {
        "category": "Continentes Perdidos",
        "cat_id": "categoria-continentes-perdidos",
        "list_id": "lista-continentes-perdidos",
        "serie_id": "serie-continentes-perdidos",
        "capitulos_id": "capitulos-continentes-perdidos",
        "chapters": [
            ("capitulo-1-continentes-perdidos.html", "Continentes Perdidos — Capítulo 1"),
            ("capitulo-2-continentes-perdidos.html", "Lemúria — Origem, Localização, Evidências e Teorias do Continente Hipotético do Índico"),
            ("capitulo-3-continentes-perdidos.html", "Conexões, Comparações e Legado — Atlântida e Lemúria, o que Une e Separa os Dois Mitos"),
        ]
    },
    "arqueologia": {
        "category": "Arqueologia",
        "cat_id": "categoria-arqueologia",
        "list_id": "lista-arqueologia",
        "serie_id": "serie-arqueologia",
        "capitulos_id": "capitulos-arqueologia",
        "chapters": [
            ("capitulo-1-arqueologia-o-geoglifo-que-nao-estava-no-mapa.html", "O Geoglifo que Não Estava no Mapa"),
            ("capitulo-2-arqueologia-a-camada-abaixo-do-ocre.html", "A Camada Abaixo do Ocre"),
            ("capitulo-3-arqueologia-a-figura-que-nao-estava-na-rocha.html", "A Figura que Não Estava na Rocha"),
            ("capitulo-4-arqueologia-a-pintura-que-esperava-no-escuro.html", "A Pintura que Esperava no Escuro"),
            ("capitulo-5-arqueologia-a-segunda-escrita-do-inga.html", "A Segunda Escrita do Ingá"),
            ("capitulo-6-arqueologia-o-que-esta-abaixo-das-conchas.html", "O Que Está Abaixo das Conchas"),
        ],
        "standalone": [
            ("o-glifo-que-nao-esta-no-catalogo.html", "O Glifo que Não Está no Catálogo"),
            ("o-nome-na-pedra-de-esquina.html", "O Nome na Pedra de Esquina"),
        ]
    },
    "sobrenatural": {
        "category": "Sobrenatural",
        "cat_id": "categoria-sobrenatural",
        "list_id": "lista-sobrenatural",
        "serie_id": "serie-sobrenatural",
        "capitulos_id": "capitulos-sobrenatural",
        "chapters": [
            ("capitulo-1-sobrenatural-o-po-co-sem-eco.html", "O Poço Sem Eco"),
            ("capitulo-2-sobrenatural-o-revisor-de-negativos.html", "O Revisor de Negativos"),
        ]
    },
    "contos-de-terror": {
        "category": "Contos de Terror",
        "cat_id": "categoria-contos-de-terror",
        "list_id": "lista-contos-de-terror",
        "serie_id": "serie-contos-de-terror",
        "capitulos_id": "capitulos-contos-de-terror",
        "chapters": [
            ("capitulo-1-contos-de-terror.html", "O Gravador do Abismo"),
            ("capitulo-2-contos-de-terror-a-boca-da-mina.html", "A Boca da Mina"),
            ("capitulo-3-contos-de-terror-a-decima-setima-campainha.html", "A Décima Sétima Campainha"),
            ("capitulo-4-contos-de-terror-a-dolina-invertida.html", "A Dolina Invertida"),
            ("capitulo-5-contos-de-terror-a-ultima-ronda-da-torre-de-vigia.html", "A Última Ronda da Torre de Vigia"),
            ("capitulo-6-contos-de-terror-buraco-do-inferno.html", "O Eco que Vinha de Baixo"),
            ("capitulo-7-contos-de-terror-o-andar-que-nao-esta-na-planta.html", "O Andar que Não Está na Planta"),
            ("capitulo-8-contos-de-terror-o-bilhete-da-plataforma-3.html", "O Bilhete da Plataforma 3"),
            ("capitulo-9-contos-de-terror-o-canto-da-areia-nao-tem-volta.html", "O Canto da Areia Não Tem Volta"),
            ("capitulo-10-contos-de-terror-o-deposito-de-achados-e-perdidos.html", "O Depósito de Achados e Perdidos"),
            ("capitulo-11-contos-de-terror-o-faroleiro-da-nevoa.html", "O Faroleiro da Névoa"),
            ("capitulo-12-contos-de-terror-o-guardiao-do-silencio.html", "O Guardião do Silêncio"),
            ("capitulo-13-contos-de-terror-o-laudo-da-sala-fria.html", "O Laudo da Sala Fria"),
            ("capitulo-14-contos-de-terror-o-livro-de-ponto-de-fordlandia.html", "O Livro de Ponto de Fordlândia"),
            ("capitulo-15-contos-de-terror-o-recebedor-de-cartas-nao-enderecadas.html", "O Recebedor de Cartas Não Endereçadas"),
            ("capitulo-16-contos-de-terror-o-ultimo-sermao-da-igreja-submersa.html", "O Último Sermão da Igreja Submersa"),
            ("capitulo-17-contos-de-terror-o-ultimo-telegrafo-da-estacao-monte-santo.html", "O Último Telégrafo da Estação Monte Santo"),
        ],
        "standalone": [
            ("a-boca-da-mina.html", "A Boca da Mina"),
            ("a-camada-abaixo-do-ocre.html", "A Camada Abaixo do Ocre"),
            ("a-corrida-da-madrugada.html", "A Corrida da Madrugada"),
            ("a-linha-morta.html", "A Linha Morta"),
            ("a-voz-no-poco-de-ventilacao.html", "A Voz no Poço de Ventilação"),
            ("o-quarto-de-fundo.html", "O Quarto de Fundo"),
            ("o-zumbido-de-taos.html", "O Zumbido de Taos"),
            ("o-zumbido-que-escuta-de-volta.html", "O Zumbido que Escuta de Volta"),
        ]
    },
    "arte-antiga-e-ovnis": {
        "category": "Arte Antiga e OVNIs",
        "cat_id": "categoria-arte-antiga",
        "list_id": "lista-arte-antiga",
        "serie_id": "serie-arte-antiga",
        "capitulos_id": "capitulos-arte-antiga",
        "chapters": [
            ("capitulo-1-arte-antiga-discos.html", "Discos na Arte Antiga: OVNIs nas Obras-Primas da História da Arte"),
        ]
    },
    "ufos-e-aliens": {
        "category": "UFOs e Aliens",
        "cat_id": "categoria-ufos",
        "list_id": "lista-ufos",
        "serie_id": "serie-ufos",
        "capitulos_id": "capitulos-ufos",
        "chapters": [
            ("capitulo-1-ufos-o-registro-151.html", "O Registro 151"),
            ("capitulo-2-ufos-a-sexta-exposicao.html", "A Sexta Exposição"),
            ("capitulo-3-ufos-o-alvo-sem-plano-de-voo.html", "O Alvo Sem Plano de Voo"),
            ("capitulo-4-ufos-o-controle-que-respondeu-de-volta.html", "O Controle Que Respondeu de Volta"),
            ("capitulo-5-ufos-o-eco-secundario.html", "O Eco Secundário"),
            ("capitulo-6-ufos-o-escrevente-de-colares.html", "O Escrevente de Colares"),
            ("capitulo-7-ufos-o-operador-da-hora-vazia.html", "O Operador da Hora Vazia"),
        ]
    },
    "fenomenos-naturais": {
        "category": "Fenômenos Naturais",
        "cat_id": "categoria-fenomenos-naturais",
        "list_id": "lista-fenomenos-naturais",
        "serie_id": "serie-fenomenos-naturais",
        "capitulos_id": "capitulos-fenomenos-naturais",
        "chapters": [
            ("capitulo-1-fenomenos-naturais-a-chuva-que-traya-ossos.html", "A Chuva que Trazia Ossos"),
            ("capitulo-2-fenomenos-naturais-a-nuvem-que-nao-passava.html", "A Nuvem que Não Passava"),
            ("capitulo-3-fenomenos-naturais-as-luzes-de-antes-do-tremor.html", "As Luzes de Antes do Tremor"),
            ("capitulo-4-fenomenos-naturais-as-luzes-do-brejo.html", "As Luzes do Brejo"),
            ("capitulo-5-fenomenos-naturais-o-estampido-sem-fonte.html", "O Estampido sem Fonte"),
            ("capitulo-6-fenomenos-naturais-o-fogo-do-catatumbo.html", "O Fogo do Catatumbo"),
            ("capitulo-7-fenomenos-naturais-o-gemido-das-pedras-de-espinhaco.html", "O Gemido das Pedras de Espinhaço"),
            ("capitulo-8-fenomenos-naturais-o-hum-de-cana-brava.html", "O Hum de Cana Brava"),
            ("capitulo-9-fenomenos-naturais-o-sopro-abaixo-de-20-hertz.html", "O Sopro Abaixo de 20 Hertz"),
            ("capitulo-10-fenomenos-naturais-o-tremor-da-estacao-santa-helena.html", "O Tremor da Estação Santa Helena"),
            ("capitulo-11-fenomenos-naturais-o-zumbido-de-pedra-branca.html", "O Zumbido de Pedra Branca"),
        ]
    },
    "criptozoologia": {
        "category": "Criptozoologia",
        "cat_id": "categoria-criptozoologia",
        "list_id": "lista-criptozoologia",
        "serie_id": "serie-criptozoologia",
        "capitulos_id": "capitulos-criptozoologia",
        "chapters": [
            ("capitulo-1-criptozoologia-o-animal-de-carajas.html", "O Animal de Carajás"),
            ("capitulo-2-criptozoologia-o-minhocao-de-barro-preto.html", "O Minhocão de Barro Preto"),
            ("capitulo-3-criptozoologia-o-que-respira-no-lodo.html", "O Que Respira no Lodo"),
            ("capitulo-4-criptozoologia-o-que-restou-abaixo-da-agua.html", "O Que Restou Abaixo da Água"),
        ]
    },
    "conspiracoes": {
        "category": "Conspirações",
        "cat_id": "categoria-conspiracoes",
        "list_id": "lista-conspiracoes",
        "serie_id": "serie-conspiracoes",
        "capitulos_id": "capitulos-conspiracoes",
        "chapters": [
            ("capitulo-1-conspiracaoes-a-ultima-leitura-da-estacao-de-numeros.html", "A Última Leitura da Estação de Números"),
            ("capitulo-2-conspiracaoes-o-arquivista-do-segundo-andar.html", "O Arquivista do Segundo Andar"),
        ]
    }
}

def generate_sidebar_html(series_key, current_file):
    """Generate the sidebar HTML for a given series and current file."""
    s = series[series_key]
    cat_id = s["cat_id"]
    list_id = s["list_id"]
    serie_id = s["serie_id"]
    capitulos_id = s["capitulos_id"]
    category = s["category"]
    chapters = s["chapters"]
    standalone = s.get("standalone", [])
    
    # Build chapter links
    chapter_links = ""
    for fname, title in chapters:
        active = ' class="ativo"' if fname == current_file else ''
        chapter_links += f'              <li><a href="{fname}"{active}>{title}</a></li>\n'
    
    # Add standalone if current file is standalone
    standalone_links = ""
    if current_file in [f for f, _ in standalone]:
        for fname, title in standalone:
            active = ' class="ativo"' if fname == current_file else ''
            standalone_links += f'              <li><a href="{fname}"{active}>{title}</a></li>\n'
    elif standalone:
        # If current file is a chapter, include standalone in the list
        for fname, title in standalone:
            standalone_links += f'              <li><a href="{fname}">{title}</a></li>\n'
    
    all_links = chapter_links + standalone_links
    
    sidebar = f'''      <!-- Categoria: {category} -->
      <div class="categoria-grupo">
        <div class="categoria-titulo" id="{cat_id}" role="button" tabindex="0" aria-expanded="false">{category}</div>
        <ul class="lista-topicos" id="{list_id}" style="display: none;">
          <li>
            <div class="categoria-titulo nivel-2" id="{serie_id}" role="button" tabindex="0" aria-expanded="false">Série {category}</div>
            <ul class="lista-topicos nivel-2" id="{capitulos_id}" style="display: none;">
{all_links}            </ul>
          </li>
        </ul>
      </div>'''
    return sidebar

def generate_nav_capitulos(series_key, current_file):
    """Generate nav-capitulos HTML for a given series and current file."""
    s = series[series_key]
    chapters = s["chapters"]
    
    # Find current index
    current_idx = None
    for i, (fname, _) in enumerate(chapters):
        if fname == current_file:
            current_idx = i
            break
    
    if current_idx is None:
        return ""
    
    prev_link = ""
    next_link = ""
    
    if current_idx > 0:
        prev_fname, prev_title = chapters[current_idx - 1]
        prev_link = f'        <a href="{prev_fname}" class="nav-anterior">← {prev_title}</a>\n'
    
    if current_idx < len(chapters) - 1:
        next_fname, next_title = chapters[current_idx + 1]
        next_link = f'        <a href="{next_fname}" class="nav-proximo">{next_title} →</a>\n'
    
    if not prev_link and not next_link:
        return ""
    
    nav = f'''      <nav class="nav-capitulos">
{prev_link}{next_link}      </nav>'''
    return nav

def generate_js_serie_handler(series_key):
    """Generate the JavaScript serie handler for a given series."""
    s = series[series_key]
    serie_id = s["serie_id"]
    capitulos_id = s["capitulos_id"]
    
    js = f'''        /* Animação cascata da série {s["category"]} */
        const serieBtn = document.getElementById('{serie_id}');
        const serieLista = document.getElementById('{capitulos_id}');
        if (serieBtn && serieLista) {{
          const serieItens = Array.from(serieLista.querySelectorAll('li'));

          function abrirSerie() {{
            serieLista.style.display = 'block';
            serieLista.style.visibility = 'visible';
            void serieLista.offsetHeight;
            serieItens.forEach((li, i) => {{
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeIn 0.3s ease forwards';
              li.style.animationDelay = `${{i * 60}}ms`;
            }});
            serieBtn.setAttribute('aria-expanded', 'true');
          }}

          function fecharSerie() {{
            const ultimo = serieItens.length - 1;
            serieItens.forEach((li, i) => {{
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeOut 0.2s ease forwards';
              li.style.animationDelay = `${{i * 50}}ms`;
            }});
            setTimeout(() => {{
              serieLista.style.display = 'none';
              serieLista.style.visibility = 'hidden';
              serieItens.forEach(li => {{ li.style.animation = 'none'; }});
            }}, ultimo * 50 + 200);
            serieBtn.setAttribute('aria-expanded', 'false');
          }}

          serieBtn.addEventListener('click', () => {{
            const aberto = serieLista.style.display === 'block';
            if (aberto) {{ fecharSerie(); }} else {{ abrirSerie(); }}
          }});

          serieBtn.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' || e.key === ' ') {{
              e.preventDefault();
              serieBtn.click();
            }}
          }});
        }}'''
    return js

def find_series_for_file(filename):
    """Find which series a file belongs to."""
    for key, s in series.items():
        for fname, _ in s["chapters"]:
            if fname == filename:
                return key
        for fname, _ in s.get("standalone", []):
            if fname == filename:
                return key
    return None

def fix_file(filepath, filename):
    """Fix a single post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    series_key = find_series_for_file(filename)
    if not series_key:
        print(f"  WARNING: No series found for {filename}")
        return False
    
    s = series[series_key]
    is_chapter = any(fname == filename for fname, _ in s["chapters"])
    is_standalone = any(fname == filename for fname, _ in s.get("standalone", []))
    
    # Fix sidebar - replace the entire sidebar section
    sidebar_pattern = r'(<aside class="sidebar" id="sidebar-zambria">.*?</aside>)'
    match = re.search(sidebar_pattern, content, re.DOTALL)
    if match:
        old_sidebar = match.group(1)
        new_sidebar = f'''<aside class="sidebar" id="sidebar-zambria">
      <div class="sidebar-header">
        <div class="site-title">ZAMBRIA</div>
        <div class="site-subtitle">O Insólito Presente</div>
      </div>
{generate_sidebar_html(series_key, filename)}
    </aside>'''
        content = content.replace(old_sidebar, new_sidebar)
    else:
        print(f"  WARNING: Could not find sidebar in {filename}")
    
    # Fix nav-capitulos if it's a chapter (not standalone)
    if is_chapter:
        nav_html = generate_nav_capitulos(series_key, filename)
        if nav_html:
            # Check if nav-capitulos exists
            if '<nav class="nav-capitulos">' in content:
                # Replace existing
                nav_pattern = r'(<nav class="nav-capitulos">.*?</nav>)'
                content = re.sub(nav_pattern, nav_html, content, flags=re.DOTALL)
            else:
                # Insert before btn-voltar
                btn_voltar_pattern = r'(<!-- Botão Voltar -->\s*<button class="btn-voltar")'
                match = re.search(btn_voltar_pattern, content)
                if match:
                    insert_pos = match.start()
                    content = content[:insert_pos] + nav_html + '\n\n' + content[insert_pos:]
                else:
                    # Try to insert before </article>
                    article_end = content.find('</article>')
                    if article_end != -1:
                        content = content[:article_end] + '\n\n' + nav_html + '\n' + content[article_end:]
    
    # Fix JavaScript - replace the entire script section
    script_pattern = r'(<script>\s*//.*?</script>\s*</main>)'
    match = re.search(script_pattern, content, re.DOTALL)
    if match:
        old_script = match.group(1)
        
        # Build new script
        js_serie = generate_js_serie_handler(series_key)
        
        # Build the generic categoria-titulo handler
        all_serie_ids = [s["serie_id"] for s in series.values()]
        skip_ids = "', '".join(all_serie_ids)
        
        new_script = f'''<script>
        /* Botão de esconder/mostrar sidebar inteira */
        const btn = document.getElementById('btnToggleSidebar');
        const shell = document.querySelector('.site-shell');
        btn.addEventListener('click', () => {{
          shell.classList.toggle('sidebar-hidden');
          if (shell.classList.contains('sidebar-hidden')) {{
            btn.textContent = '≡';
            btn.setAttribute('aria-label', 'Mostrar barra lateral');
          }} else {{
            btn.textContent = '☰';
            btn.setAttribute('aria-label', 'Esconder barra lateral');
          }}
        }});

        /* Animação cascata das abas de categoria (genérico) */
        const titulos = document.querySelectorAll('.categoria-titulo');
        titulos.forEach((titulo) => {{
          const lista = titulo.nextElementSibling;
          if (!lista || !lista.classList.contains('lista-topicos')) return;
          if (['{skip_ids}'].includes(titulo.id)) return;
          const itens = Array.from(lista.querySelectorAll('li'));

          function abrir() {{
            lista.style.display = 'block';
            lista.style.visibility = 'visible';
            void lista.offsetHeight;
            itens.forEach((li, i) => {{
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = `slideFadeIn 0.3s ease forwards`;
              li.style.animationDelay = `${{i * 70}}ms`;
            }});
            titulo.setAttribute('aria-expanded', 'true');
          }}

          function fechar() {{
            const ultimo = itens.length - 1;
            itens.forEach((li, i) => {{
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = `slideFadeOut 0.2s ease forwards`;
              li.style.animationDelay = `${{i * 60}}ms`;
            }});
            setTimeout(() => {{
              lista.style.display = 'none';
              lista.style.visibility = 'hidden';
              itens.forEach(li => {{ li.style.animation = 'none'; }});
            }}, ultimo * 60 + 250);
            titulo.setAttribute('aria-expanded', 'false');
          }}

          titulo.addEventListener('click', () => {{
            const aberto = lista.style.display === 'block';
            if (aberto) {{ fechar(); }} else {{ abrir(); }}
          }});

          titulo.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' || e.key === ' ') {{
              e.preventDefault();
              titulo.click();
            }}
          }});
        }});

{js_serie}

        /* Botão Voltar */
        const btnVoltar = document.getElementById('btnVoltar');
        if (btnVoltar) {{
          btnVoltar.addEventListener('click', (e) => {{
            window.location.href = '../index.html';
          }});
        }}
      </script>
    </main>'''
        content = content.replace(old_script, new_script)
    else:
        print(f"  WARNING: Could not find script section in {filename}")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Process all files
fixed_count = 0
for filename in sorted(os.listdir(posts_dir)):
    if filename.endswith('.html'):
        filepath = os.path.join(posts_dir, filename)
        print(f"Fixing {filename}...")
        if fix_file(filepath, filename):
            fixed_count += 1

print(f"\nFixed {fixed_count} files.")