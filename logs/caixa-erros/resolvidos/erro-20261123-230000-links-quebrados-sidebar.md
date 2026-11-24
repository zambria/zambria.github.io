# Erro: Links Quebrados nas Sidebars dos Posts

## Erro
Links com `href="#"` nas sidebars dos arquivos de posts, tornando a navegação entre capítulos inoperante.

## Onde foi encontrado
44 arquivos em `posts/` contêm links `href="#"` na sidebar lateral.

## Sintoma
Ao clicar nos títulos dos capítulos na sidebar lateral de qualquer post, o link não navega para lugar nenhum (âncora vazia). O usuário fica preso na página atual sem poder navegar para outros capítulos da mesma série.

## Reportado por
INTEL-WEB-SECURITY

## Data/Hora
2026-11-23 23:00

## Arquivos afetados (exemplos)
- `posts/capitulo-1-conspiracaoes-a-ultima-leitura-da-estacao-de-numeros.html`
- `posts/capitulo-1-criptozoologia-o-animal-de-carajas.html`
- `posts/capitulo-1-sobrenatural-o-po-co-sem-eco.html`
- `posts/capitulo-2-conspiracaoes-o-arquivista-do-segundo-andar.html`
- `posts/capitulo-2-criptozoologia-o-minhocao-de-barro-preto.html`
- `posts/capitulo-2-sobrenatural-o-revisor-de-negativos.html`
- `posts/capitulo-3-arqueologia-a-figura-que-nao-estava-na-rocha.html`
- `posts/capitulo-3-contos-de-terror-a-decima-setima-campainha.html`
- `posts/capitulo-3-criptozoologia-o-que-respira-no-lodo.html`
- `posts/capitulo-3-fenomenos-naturais-as-luzes-de-antes-do-tremor.html`
- `posts/capitulo-3-ufos-o-alvo-sem-plano-de-voo.html`
- E mais 34 arquivos...

## Severidade
🔴 Crítica - Navegação principal quebrada em 44 páginas

## Resolução
- **Corrigido por:** INTEL-WEB-SECURITY
- **O que foi feito:** Substituídos todos os links `href="#"` nas sidebars por links corretos apontando para os arquivos de capítulo correspondentes. Cada arquivo de post agora tem uma sidebar completa com todos os capítulos da sua série, com links funcionais.
- **Arquivos alterados:** 71 arquivos em `posts/` (todas as sidebars reconstruídas com links corretos)
- **Data/Hora:** 2026-11-23 23:15