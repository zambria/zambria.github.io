import os, json, re

base = 'review/pendentes/'
items = [
    ('ufo-01','Céus Não Identificados','ufos','ceus-nao-identificados-2026-11-22-1102.md',5),
    ('ufo-02','Eles Levam Pessoas','ufos','eles-levam-pessoas-2026-11-22-1102.md',7),
    ('ufo-03','Contatos de Outro Mundo','ufos','contatos-de-outro-mundo-2026-11-22-1102.md',7),
    ('ufo-04','Mensagens nos Campos','ufos','mensagens-nos-campos-2026-11-22-1102.md',7),
    ('ufo-05','Discos na Arte Antiga','ufos','discos-na-arte-antiga-2026-11-22-1102.md',6),
    ('ufo-06','Arquivos Secretos do Governo','ufos','arquivos-secretos-do-governo-2026-11-22-1102.md',8),
    ('ufo-07','A Base que Não Existe','ufos','a-base-que-nao-existe-2026-11-22-1102.md',7),
    ('ufo-08','O Sinal do Espaço','ufos','o-sinal-do-espaco-2026-11-22-1102.md',7),
    ('ufo-09','Eles Vieram das Estrelas','ufos','eles-vieram-das-estrelas-2026-11-22-1102.md',7),
    ('ufo-10','Vida Fora da Terra','ufos','vida-fora-da-terra-2026-11-22-1102.md',8),
]

print('=== VERIFICACAO DE ARQUIVOS (review/pendentes/) ===')
results = []
for topico, titulo, categoria, fname, fontes in items:
    path = os.path.join(base, fname)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    chars_no_frontmatter = None
    if exists:
        with open(path, encoding='utf-8') as f:
            content = f.read()
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.S)
        body = content[m.end():] if m else content
        chars_no_frontmatter = len(body)
    results.append((topico, titulo, categoria, fname, exists, size, chars_no_frontmatter, fontes))
    flag = 'OK' if (exists and chars_no_frontmatter and chars_no_frontmatter >= 3500) else 'FALHA'
    print(f"[{flag}] {topico}: existe={exists} bytes={size} chars_sem_frontmatter={chars_no_frontmatter} fontes={fontes}")

with open('drafted.json', encoding='utf-8') as f:
    d = json.load(f)
print('\ndrafted.json valido. entradas atuais:', len(d.get('drafted', [])), '| processados:', d.get('processados'))

total_chars = sum(r[6] for r in results if r[6])
print('\n=== RESUMO ===')
print('Artigos:', len(results), '| Todos >= 3500 chars sem frontmatter:', all(r[6] and r[6] >= 3500 for r in results))
print('Total caracteres sem frontmatter:', total_chars)
for r in results:
    print(f"  - {r[0]} | {r[3]} | {r[6]} chars | {r[7]} fontes")

EOF
