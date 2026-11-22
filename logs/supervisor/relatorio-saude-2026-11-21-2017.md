# Relatório de Saúde — Supervisor Fiscal ZAMBRIA

**Execução:** 2026-11-21 20:17 -02 (UTC-02:00)  
**Workdir:** C:/Users/erico/zambria.github.io/  
**Arquivo de jobs:** C:/Users/erico/AppData/Local/hermes/cron/jobs.json  
**Jobs monitorados:** 5

---

## 1. jobs.json — registro de jobs

| # | Job | enabled | last_status | state | next_run_at (-02) | last_run_at (-02) | last_failure | streak |
|---|-----|---------|-------------|-------|-------------------|-------------------|--------------|--------|
| 1 | ficcao-criador-zambria (ficcao-criador-001) | true | ok | scheduled | 2026-11-21 20:20 | 2026-11-21 20:09 | "interrupted" em 21/11 00:23 | 0 |
| 2 | pesquisador-escritor-zambria (pesquisador-escritor-zambria-001) | true | ok | running | 2026-11-21 21:17 | 2026-11-21 19:25 | — | 0 |
| 3 | curador-revisor-verificador-zambria (curador-revisor-verificador-zambria-001) | true | ok | scheduled | 2026-11-21 20:23 | 2026-11-21 20:17 | — | 0 |
| 4 | publicador-webmaster-zambria (publicador-webmaster-zambria-001) | true | ok | scheduled | 2026-11-21 20:26 | 2026-11-21 19:35 | — | 0 |
| 5 | supervisor-fiscal-zambria (supervisor-fiscal-zambria-001) | true | ok | scheduled | 2026-11-21 20:36 | 2026-11-21 19:36 | — | 0 |

Todos os 5 jobs estão `enabled: true`. Todos têm `next_run_at` no futuro (não há janela vencida neste ciclo).

---

## 2. Logs das últimas 24h

Busca por padrões de erro (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError):

- **HTTP 429:** ocorrências em `managed-worker.log` pertencem a janelas anteriores (18/11, fora da janela de 24h desta execução). Erros temporários, já recuperados. **Não pausar** (regra: erro temporário não pausa).
- **RuntimeError / SyntaxError / FileNotFoundError:** nenhuma ocorrência vinculada a jobs cron nesta janela de 24h.
- **ficcao-criador-zambria:** `last_failure` "interrupted" em 21/11 00:23 -02 — interrupção transitória de infraestrutura (cron fire ownership perdido durante drain do gateway), já recuperada (`last_status: ok`, `failure_streak: 0`). **Não pausar.**
- Nenhum erro novo registrado neste ciclo (20:17 -02). Todos os jobs reportam `last_status: ok`.

---

## 3. Erros conhecidos no jobs.json (last_failure)

Todos com `failure_streak: 0` e `last_status: ok` — já recuperados, sem ação do supervisor.

| Job | last_failure | Classificação | Ação do supervisor |
|-----|--------------|---------------|--------------------|
| ficcao-criador-zambria | "interrupted" em 21/11 00:23 -02 | Transitória, recuperada | Registrada apenas. Não pausar. |
| Demais 4 jobs | — | Sem falha | Sem ação. |

---

## 4. Jobs com next_run_at vencido

Nenhum. Todos os 5 jobs têm `next_run_at` futuro em relação a 20:17 -02. Não há reexecução forçada necessária.

---

## 5. Estrutura do site (monitoramento obrigatório)

### 5.1 index.html → posts/

index.html contém **11 links** para arquivos `.html` em `posts/`:

| Link em index.html | Existe em posts/ | Status |
|--------------------|------------------|--------|
| posts/ceus-vigiados-ovnis-brasil.html | sim | OK |
| posts/triangulo-negro-uap.html | sim | OK |
| posts/a-sombra-no-planalto.html | sim | OK |
| posts/o-di-rio-do-vigia.html | sim | OK |
| posts/a-l-mpada-que-viu-demais.html | **não** | ❌ LINK QUEBRADO |
| posts/o-olhar-de-pedra.html | sim | OK |
| posts/2026-11-20-17-de-novembro-apagao-mundial.html | sim | OK |
| posts/2026-11-20-ceu-verde-paraiba-bolido.html | sim | OK |
| posts/a-ltima-noite-de-marte.html | sim | OK |
| posts/contos-criativos-001.html | sim | OK |
| posts/o-tom-das-3h14.html | sim | OK |

### 5.2 Arquivos órfãos em posts/ (não referenciados em index.html)

5 arquivos `.html` existem em `posts/` mas não são linkados em index.html:
- `posts/ufo-01-longo.html`
- `posts/revis-o-editorial-contos-criativos-001-md.html`
- `posts/ovnis-e-uaps-quando-o-c-u-deixa-de-ser-identificado.html`
- `posts/abdu-es-alien-genas-quando-eles-levam-voc.html`
- `posts/743-registros-zero-explicacoes-arquivo-nacional.html`

### 5.3 Botão toggle fixo

Existe em index.html (`id="btnToggleSidebar"`, canto superior esquerdo) e `style.css` define `position: fixed; top: 1rem; left: 1rem; z-index: 1000;` — sempre visível. **OK.**

### 5.4 review/ficcoes/

Pasta ativa com 51+ histórias do Super Agent Criador de Ficção em `.md`.

**Inconsistências encontradas:**
1. Link quebrado: `posts/a-l-mpada-que-viu-demais.html` referenciado em index.html não existe (arquivo real: `posts/a-l-mpada-que-viu-demais-revisao.html`).
2. 5 arquivos órfãos em `posts/` não vinculados na sidebar.

Informar o Curador-Chefe ou o Publicador-Webmaster para correção.

---

## 6. Verificação de ficções independentes (review/ficcoes/)

- `o-laudo-do-turno-da-noite.md` contém `publicar: false` no frontmatter (linha 9). **Ignorado para fins de publicação**, conforme regra de segurança — primeira história do Super Agent Criador, serve apenas como exemplo de funcionamento.
- As demais histórias na pasta podem entrar no fluxo de curadoria normal (Curador-Chefe → Revisor → Verificador → Publicador) quando requisitadas.

---

## 7. Ações tomantes neste ciclo

- Nenhum job pausado (não houve erro persistente: sem SyntaxError nem FileNotFoundError vinculados a jobs cron).
- Nenhum job reexecutado forçadamente (todos os `next_run_at` estão no futuro).
- `jobs.json`: sem alterações.
- Relatório de saúde gravado em `logs/supervisor/relatorio-saude-2026-11-21-2017.md`.

---

## 8. Alertas enviados ao Curador-Chefe

**Nenhum alerta crítico de pipeline travado.** Pipeline operando: todos os 5 jobs habilitados têm `last_status: ok` e próxima execução no futuro.

**Alerta de estrutura (não crítico):** inconsistência no site (1 link quebrado + 5 arquivos órfãos em `posts/`). Encaminhar ao Curador-Chefe ou Publicador-Webmaster para correção.

---

## 9. Conclusão

O pipeline ZAMBRIA está operando sem interrupções neste ciclo:

- 5 jobs cadastrados; 5 habilitados com `last_status: ok` e próximo disparo no futuro.
- 0 jobs pausados/desativados.
- Erros recentes apenas transitórios (HTTP 429 de 18/11 já recuperados; interrupção do ficcao-criador em 21/11 00:23 já recuperada). `failure_streak: 0` em todos.
- Sem `FileNotFoundError` nem `SyntaxError` em jobs cron.
- Estrutura do site com inconsistências: 1 link quebrado e 5 arquivos órfãos em `posts/`.
- Pipeline não travado. Curador-Chefe não precisa ser acionado por parada de job, mas deve ser informado sobre a inconsistência estrutural.

*Gerado pelo Agente Supervisor Fiscal ZAMBRIA. Um ciclo concluído.*
