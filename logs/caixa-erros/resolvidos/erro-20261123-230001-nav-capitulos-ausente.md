# Erro: Navegação Entre Capítulos Ausente (nav-capitulos)

## Erro
57 arquivos de posts não possuem o componente `<nav class="nav-capitulos">` para navegação entre capítulos (anterior/próximo).

## Onde foi encontrado
Arquivos em `posts/` que fazem parte de séries multi-capítulo mas não têm botões de navegação.

## Sintoma
Usuários não conseguem navegar sequencialmente entre capítulos de uma mesma série usando botões "Anterior/Próximo" no final do artigo. Precisam voltar ao index e clicar na sidebar.

## Reportado por
INTEL-WEB-SECURITY

## Data/Hora
2026-11-23 23:00

## Severidade
🟡 Alta - Degradação significativa de UX em séries longas

## Observação
Alguns arquivos são artigos únicos (standalone) e não precisam de nav-capitulos. A correção deve ser aplicada apenas às séries multi-capítulo.

## Resolução
- **Corrigido por:** INTEL-WEB-SECURITY
- **O que foi feito:** Adicionado componente `<nav class="nav-capitulos">` com links "Anterior/Próximo" em todos os 61 arquivos de capítulos que fazem parte de séries multi-capítulo. Artigos standalone não receberam nav-capitulos.
- **Arquivos alterados:** 61 arquivos em `posts/` (todos os capítulos de séries)
- **Data/Hora:** 2026-11-23 23:15