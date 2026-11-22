# VARREDURA ESTRUTURAL DE INTEGRIDADE — ZAMBRIA
**Data/Hora:** 2026-11-21 23:05:20  (UTC-02:00)
**Gerado por:** supervisor-fiscal-zambria (Passo 6 + 6B + 7 + 7B)

## 1. Posts
- Arquivos `.html` em `posts/`: **226**
- Links `.html` únicos no `index.html`: **226**
- Links quebrados (href sem arquivo em `posts/`): **0**
- Posts órfãos (arquivo em `posts/` sem link no `index.html`): **0**
- index.html sincronizado com posts/: OK

## 2. Tags `<script>` (6B-a)
- index.html: 2 aberturas, 2 fechamentos -> BALANCEADO
- Posts desbalanceados: **0**
- Resultado: OK (0 desbalanceados)

## 3. Script de animação cascata (6B-b)
- Posts sem `slideFadeIn`/`slideFadeOut`: **174**
  - a-agua-que-o-poco-devolveu.html
  - a-camara-selada-de-pedra.html
  - a-chuva-de-peixes-de-yoro.html
  - a-chuva-que-trouxe-escamas.html
  - a-coisa-que-chama-com-voz-de-mae.html
  - a-coluna-sem-fundo.html
  - a-duna-que-cantava-sozinha.html
  - a-esfera-dourada-da-lapinha.html
  - a-estacao-que-ouviu-de-volta.html
  - a-ferida-que-nao-sangrou.html
  - a-figura-fora-do-abri.html
  - a-fita-que-hollanda-nao-entregou.html
  - a-frequencia-enterrada.html
  - a-frequencia-silenciada.html
  - a-galeria-171.html
  - a-galeria-que-nao-constava-na-planta.html
  - a-grade-do-mar.html
  - a-gravura-que-olha-de-volta.html
  - a-itacoatiara-escreve-de-volta.html
  - a-lista-de-sume.html
  - a-luz-que-caminhava-atras-de-mim.html
  - a-luz-que-chama-pelo-nome.html
  - a-marca-na-pedra-lisa.html
  - a-neblina-que-sobe-em-linha-reta.html
  - a-nevoa-das-tres-e-dezessete.html
  - a-nevoa-que-sussurra-em-dois-idiomas.html
  - a-parede-que-ouviu-de-volta.html
  - a-pele-que-desceu-da-rocha.html
  - a-perseguicao-da-noite-oficial.html
  - a-pintura-que-nao-estava-ontem.html
  - a-pista-que-esperava-a-partida.html
  - a-quarta-parede-da-galeria-sete.html
  - a-quarta-vigia.html
  - a-resonancia-abaixo-do-ouvido.html
  - a-sala-que-guardava-as-vozes.html
  - a-seca-que-trouxe-vozes.html
  - a-segunda-camada.html
  - a-segunda-imagem.html
  - a-segunda-inscricao-de-inga.html
  - a-segunda-sombra.html
- Resultado: ERRO

## 4. Botão toggle fixo (6 + 6B-c)
- `btn-toggle-sidebar` presente no index.html: True
- Botão dentro do `<aside>`: False  -> OK (fora do aside)
- style.css position: fixed presente: True
- style.css z-index alto presente: True
- Resultado toggle: OK

## 5. Classes CSS inconsistentes (6B-d)
- index.html class="topicos-lista": 0 (deveria ser 0)
- index.html class="lista-topicos": 8
- Posts com class="topicos-lista": 0 (deveria ser 0)
- Resultado classes: OK

## 6. onclick toggleCategoria (6B-e)
- Ocorrências: **0** (deveria ser 0)
- Resultado: OK

## 7. Ficções independentes (Passo 7 + regra de segurança)
- Histórias em `review/ficcoes/`: **175**
- Com `publicar: false` (ignorar para publicação): **0**
- `o-laudo-do-turno-da-noite.md`: não encontrado (ignorado corretamente / não existe)

## 8. Textos aprovados parados na revisão (Passo 7B)
- `_aprovado.md` em `review/publicados/` (raiz, excluindo `arquivado/`): **21**
  - a-base-que-nao-existe-2026-11-21_aprovado.md
  - a-datacao-impossivel_aprovado.md
  - a-mancha-do-terceiro-andar_aprovado.md
  - bruxas-feiticos-e-sombras-2026-11-21_aprovado.md
  - ceus-nao-identificados-2026-11-21-2354-01_aprovado.md
  - chupacabra-2026-11-21_aprovado.md
  - contatos-de-outro-mundo-2026-11-21-2354-03_aprovado.md
  - eles-levam-pessoas-2026-11-21-2354-02_aprovado.md
  - entidades-demoniacas-2026-11-21_aprovado.md
  - leviatas-do-mar-2026-11-21_aprovado.md
  - lobisomens-nas-sombras-2026-11-21_aprovado.md
  - maldicao-do-farao-2026-11-21_aprovado.md
  - mensagens-nos-campos-2026-11-21-2354-04_aprovado.md
  - o-batimento-da-hematita_aprovado.md
  - o-fundo-que-nao-acaba_aprovado.md
  - o-globo-que-veio-na-tempestade_aprovado.md
  - o-limpador-de-apartamentos-vazios_aprovado.md
  - o-tumulo-que-arranha-de-dentro_aprovado.md
  - objetos-amaldicoados-2026-11-21_aprovado.md
  - rituais-contra-o-mal-2026-11-21_aprovado.md
  - vozes-do-alem-evp-2026-11-21_aprovado.md
- `_aprovado.md` em `review/pendentes/`: **0**
- `.html` em `posts/`: **226**
- Aprovados > posts publicados? False -> Não há backlog crítico
- Aprovados em pendentes? False -> Sem erro de fluxo