# 🏗️ ESQUEMA ESTRUTURAL — Index.html (Backup e Regras)

## Arquivo: index.html (Página inicial ZAMBRIA)

### Versão funcional confirmada
Commit `db9fe9f` — Restauração da versão `b565e52` (abas da sidebar funcionando).

### Regras de ouro para edição do index.html

1. **NUNCA** use nomes de variáveis JavaScript com acentos, cedilha, til, espaços ou caracteres especiais
   - ❌ Errado: `serieBtnoperação-prato`, `serieBtnsete-além`
   - ✅ Certo: `serieBtnOperacaoPrato`, `serieBtnSeteAlém`

2. **NUNCA** use arrow functions (`() => {}`) ou template literais (`` `${}` ``) no index.html
   - Use sempre `function() {}` e strings normais com aspas duplas

3. **Sempre teste as abas da sidebar após qualquer alteração no index.html**
   - Abra cada categoria (Operação Prato, Sete Além, etc.) e verifique se expande e recolhe

4. **Nunca remova o evento de clique dos elementos `.categoria-titulo`**
   - Eles precisam do `addEventListener('click', ...)` para funcionar

5. **Mantenha o JavaScript simples e direto**
   - Não use bibliotecas externas no index.html
   - Use apenas JavaScript vanilla padrão

### Como restaurar se quebrar de novo

```bash
cd /c/Users/erico/zambria.github.io
git checkout <commit-funcionando> -- index.html
git add index.html
git commit -m "fix(navegacao): restaura index.html versao funcional"
git push origin main
```

### Commits conhecidos como funcionais para o index.html
- `db9fe9f` — Versão atual restaurada (abas funcionando)
- `b565e52` — Versão anterior funcional
- `52412af` — Versão anterior funcional (antes da quebra)
