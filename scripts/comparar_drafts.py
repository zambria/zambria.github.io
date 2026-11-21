import json, re, os

with open('drafted.json', encoding='utf-8') as f:
    data = json.load(f)
reais = [d for d in data['drafted'] if '-fontes:' not in d]

print("=== IDS JA PROCESSADOS (drafted.json) ===")
for d in sorted(reais):
    print("  ", d)

print("\n=== COMPARACAO drafts/ ===")
draft_dir = 'drafts'
nao_processados = []
for fn in sorted(os.listdir(draft_dir)):
    if fn == '.gitkeep':
        continue
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', fn).replace('.md', '')
    match = None
    for d in reais:
        if d == slug or d in slug or slug in d:
            match = d
            break
    if match:
        print(f"[PROCESSADO] {fn}  (match: {match})")
    else:
        print(f"[NAO PROCESSADO] {fn}  -> slug: {slug}")
        nao_processados.append(fn)

print("\n=== TOTAL NAO PROCESSADO: %d ===" % len(nao_processados))
for f in nao_processados:
    print("  ", f)
