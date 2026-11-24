# Erro: Artigos Standalone Incompletos (10 arquivos)

## Erro
10 artigos standalone (a-*.html, o-*.html) na pasta posts/ têm estrutura incompleta comparada aos capítulos de séries.

## Onde foi encontrado
- `posts/a-boca-da-mina.html`
- `posts/a-camada-abaixo-do-ocre.html`
- `posts/a-corrida-da-madrugada.html`
- `posts/a-linha-morta.html`
- `posts/a-voz-no-poco-de-ventilacao.html`
- `posts/o-glifo-que-nao-esta-no-catalogo.html`
- `posts/o-nome-na-pedra-de-esquina.html`
- `posts/o-quarto-de-fundo.html`
- `posts/o-zumbido-de-taos.html`
- `posts/o-zumbido-que-escuta-de-volta.html`

## Sintoma
Estes artigos não possuem:
1. Bloco `<style>` com CSS customizado (btn-voltar, bloco-denso, cite, cap-paragrafo, etc.)
2. Script de animação específico da série `serie-contos-de-terror` (exceto a-voz-no-poco-de-ventilacao.html que tem)
3. Seção de fontes em `<details class="bloco-denso">` (usam `<div class="fontes">` simples)
4. `a-boca-da-mina.html` tem conteúdo corrompido com códigos de escape de terminal
5. `a-camada-abaixo-do-ocre.html` tem exclusão errada no script genérico (`serie-arqueologia` em vez de `serie-contos-de-terror`)

## Reportado por
INTEL-WEB-SECURITY

## Data/Hora
2026-11-24 00:15

## Severidade
🟡 Alta - Degradação de UX e inconsistência estrutural em 10 páginas

## Resolução
**Corrigido por:** INTEL-WEB-SECURITY
**Data/Hora:** 2026-11-24 01:12
**O que foi feito:** Os 10 artigos standalone mencionados não existem mais no site. O site foi reconstruído em 2026-11-23 (conforme memoria-compartilhada.json) mantendo apenas 2 séries: Operação Prato (5 capítulos) e Continentes Perdidos (3 capítulos). Os arquivos standalone (Contos de Terror) foram removidos durante a limpeza total. O erro relatado referia-se a um estado anterior do site que não existe mais.
**Arquivos alterados:** Nenhum (arquivos já não existem)
**Status:** Resolvido por obsolescência - erro referia-se a versão anterior do site