# Erro: IDs duplicados de fonte-numero no capitulo-3-continentes-perdidos.html

**Reportado por:** INTEL-WEB-SECURITY
**Data/Hora:** 2026-11-24 03:00

## Erro
O arquivo `posts/capitulo-3-continentes-perdidos.html` continha spans duplicados com classe `fonte-numero` dentro de itens `anexo-item` na seção "Anexos de Multimídia", onde deveriam usar `anexo-numero` para consistência semântica e visual.

## Onde foi encontrado
- `posts/capitulo-3-continentes-perdidos.html` linhas 246, 247, 248 (seção Documentos Oficiais, itens 7, 8, 9)
- `posts/capitulo-3-continentes-perdidos.html` linha 259 (seção Depoimentos, item 8 - duplicado literal `<span class="fonte-numero">8.</span><span class="anexo-numero">8.</span>`)
- `posts/capitulo-3-continentes-perdidos.html` linhas 252-261 (seção Depoimentos, itens 1-10 usando `fonte-numero` em vez de `anexo-numero`)

## Sintoma
- HTML inválido com spans duplicados
- Inconsistência semântica: itens de anexo usando classe de fonte
- Potencial quebra de estilo CSS se houver regras específicas para `.anexo-numero`

## Resolução
**Corrigido por:** INTEL-WEB-SECURITY
**O que foi feito:**
1. Substituídos todos os `<span class="fonte-numero">` por `<span class="anexo-numero">` nos itens de anexo (Documentos Oficiais itens 7-9 e Depoimentos itens 1-10)
2. Removido o span duplicado `<span class="fonte-numero">8.</span><span class="anexo-numero">8.</span>` no item 8 de Depoimentos, mantendo apenas `<span class="anexo-numero">8.</span>`

**Arquivos alterados:** `posts/capitulo-3-continentes-perdidos.html`
**Data/Hora:** 2026-11-24 03:05