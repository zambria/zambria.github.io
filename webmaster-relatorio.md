# Relatório do webmaster ZAMBRIA

Posts em /posts/: 8 (apenas as séries Operação Prato e Sete Além mantidas no site)

Posts em /posts/:
- capitulo-1-operacao-prato.html — Capítulo 1 de 5 — Operação Prato
- capitulo-2-operacao-prato.html — Capítulo 2 de 5 — Operação Prato
- capitulo-3-operacao-prato.html — Capítulo 3 de 5 — Operação Prato
- capitulo-4-operacao-prato.html — Capítulo 4 de 5 — Operação Prato
- capitulo-5-operacao-prato.html — Capítulo 5 de 5 — Operação Prato
- capitulo-1-sete-alem.html — Capítulo 1 de 3 — Sete Além
- capitulo-2-sete-alem.html — Capítulo 2 de 3 — Sete Além
- capitulo-3-sete-alem.html — Capítulo 3 de 3 — Sete Além

## Correções aplicadas nesta execução
- [x] index.html: #posts-lista reconstruída com os 8 posts existentes (removeu ~100 links fantasma para posts excluídos na limpeza automática, commit 0ab066b)
- [x] index.html: removido link fantasma do Caso Varginha da sidebar (categoria UFOs e Aliens) e da seção principal #ufo
- [x] index.html: seções de categoria (#ufo, #arch, #para, #crypto, #conspir, #nature, #contos) mantidas vazias, prontas para novos posts
- [x] publicador.py: loop de publicação publica somente textos aprovados (_aprovado.md) — já no HEAD

## Pendentes
- [ ] review/ foi removido pela limpeza automática (commit 0ab066b); o publicador recria o diretório, mas não há fontes aprovadas em fila para publicar

## Links internos
- nenhum quebrado (todos os 8 hrefs de /posts/ resolvem para arquivos existentes)

## Navegação (regra Zambria absoluta)
- Todas as abas de categoria iniciam contraídas (display: none, aria-expanded="false"); botão toggle visível fora da sidebar.
