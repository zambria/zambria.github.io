# Erro: Regressão no capitulo-2-continentes-perdidos.html

**Reportado por:** INTEL-WEB-SECURITY
**Data/Hora:** 2026-11-24 03:00

## Erro
O arquivo `posts/capitulo-2-continentes-perdidos.html` apresentava duas regressões em relação ao padrão estabelecido:
1. Markdown `# ` renderizando como texto literal no primeiro parágrafo após o título
2. Seções "Referências e Fontes" e "Anexos de Multimídia" usando estrutura antiga (h2/h3 + divs simples) em vez do padrão `details.bloco-denso` colapsível

## Onde foi encontrado
- `posts/capitulo-2-continentes-perdidos.html` linha 124 (markdown literal)
- `posts/capitulo-2-continentes-perdidos.html` linhas 151-188 (estrutura antiga de referências/anexos)

## Sintoma
- Texto "# Lemúria — O Continente Hipotético..." aparecia literalmente na tela
- Referências e anexos não eram colapsíveis, violando o padrão visual e funcional dos outros 10 posts

## Resolução
**Corrigido por:** INTEL-WEB-SECURITY
**O que foi feito:**
1. Removido o `# ` do início do parágrafo na linha 124
2. Substituída toda a estrutura de Referências e Anexos (linhas 151-188) por dois blocos `details.bloco-denso` colapsíveis, seguindo o padrão dos outros posts (capitulo-1, capitulo-3, e todos os 8 da Operação Prato)
3. Mantidas todas as 40 fontes e 10 anexos de cada categoria, apenas reestruturadas

**Arquivos alterados:** `posts/capitulo-2-continentes-perdidos.html`
**Data/Hora:** 2026-11-24 03:05