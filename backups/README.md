# ZAMBRIA — Backup e Restauração do Site

## Localização dos arquivos de backup

Todos os arquivos de backup ficam nesta pasta: `backups/`

| Arquivo | Descrição |
|---------|-----------|
| `backup_zambria_site_20261121.zip` | Compactação completa do site (456 arquivos, ~2,6 MB) |
| `backup_zambria_site_estrutura.md` | Lista detalhada de todos os arquivos com tamanhos e instruções de restauração |

---

## Como o Hermes localiza o backup

Quando o usuário pedir para restaurar ou verificar o backup do site ZAMBRIA, o agente deve:

1. Acessar a pasta `backups/` no repositório `zambria.github.io`
2. Ler o arquivo `backup_zambria_site_estrutura.md` para conferir a estrutura atual
3. Extrair o arquivo `backup_zambria_site_20261121.zip` para `C:/Users/erico/zambria.github.io/` (sobrescrevendo)
4. Fazer commit e push para o GitHub

---

## Como restaurar em caso de dano

Se o site for danificado ou alterado indevidamente:

1. **Baixe o arquivo ZIP** desta pasta.
2. **Extraia** todo o conteúdo para `C:/Users/erico/zambria.github.io/` (sobrescrevendo os arquivos atuais).
3. **Commit e push** para o GitHub:

```bash
git -C "C:/Users/erico/zambria.github.io" add .
git -C "C:/Users/erico/zambria.github.io" commit -m "restaura backup da estrutura do site"
git -C "C:/Users/erico/zambria.github.io" push origin main
```

4. Aguarde o GitHub Pages reconstruir o site (alguns minutos) e dê um hard refresh (Ctrl+F5).

---

## Dados do backup

- **Data:** 21/11/2026 19:51 (horário local)
- **Repositório:** `C:/Users/erico/zambria.github.io`
- **URL ao vivo:** `https://zambria.github.io/`
- **Arquivos incluídos:** 456
- **Tamanho do ZIP:** ~2,6 MB

---

**Observação:** esta pasta `backups/` não é servida pelo GitHub Pages como conteúdo público do site — é apenas um repositório de segurança para restauração.
