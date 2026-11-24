# Backups — ZAMBRIA

| Arquivo | Data | Tamanho | Conteúdo |
|---|---|---|---|
| backup_zambria_site_20261123_0615.tar.gz | 2026-11-23 06:15 -03 | ~2 MB | Site completo (exceto .git e pasta backups/) |

Procedimento (webmaster skill):

```bash
cd "C:/Users/erico/zambria.github.io"
tar -czf "backups/backup_zambria_site_$(date +%Y%m%d_%H%M%S).tar.gz" --exclude='.git' --exclude='backups' .
```

Restauração: extraia o arquivo sobre `C:/Users/erico/zambria.github.io/`, depois `git add . && git commit && git push origin main`.

Gerado pelo ciclo de vigilância do AXXA Web Sovereign (rodada #6 — varredura estrutural aprovada: 7/7 verificações passaram, nenhum erro estrutural em index.html nem nos 10 capítulos de posts/).
