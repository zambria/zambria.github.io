# Relatório de Saúde — Supervisor Fiscal ZAMBRIA

**Execução:** 2026-11-21 17:30 -03 (UTC-03:00)  
**Workdir:** C:/Users/erico/zambria.github.io/  
**Arquivo de jobs:** C:/Users/erico/AppData/Local/hermes/cron/jobs.json  
**Jobs monitorados:** 13

---

## 1. jobs.json — registro de jobs

Horários de jobs.json (offset -02:00) convertidos para hora local (-03:00). Execução às 17:30 -03 = 18:30 -02.

| # | Job | enabled | last_status | next_run_at (-02) | next_run_at (-03 local) | last_failure | streak | Pausado por |
|---|-----|---------|-------------|-------------------|-------------------------|--------------|--------|-------------|
| 1 | pesquisador-profundo-zambria (pesq-zambria-001) | true | ok | 2026-11-21 19:57 | 2026-11-21 18:57 | HTTP 429 em 18/11 | 0 | — |
| 2 | escritor-especializado-zambria (escritor-zambria-001) | true | ok | 2026-11-21 19:02 | 2026-11-21 18:02 | RuntimeStoreError invalid_params em 18/11 | 0 | — |
| 3 | revisor-editorial-zambria (revisor-zambria-001) | true | ok | 2026-11-21 19:09 | 2026-11-21 18:09 | HTTP 429 em 18/11 | 0 | — |
| 4 | publicador-zambria-github-io (pub-zambria-001) | true | ok | 2026-11-21 19:22 | 2026-11-21 18:22 | — | 0 | — |
| 5 | pesq-ativo-zambria-001 (0f8fd715b3cc) | false | ok | 2026-11-21 17:57 | 2026-11-21 16:57 (VENCIDO) | — | 0 | Usuário — correção necessária |
| 6 | curador-chefe-zambria (curador-chefe-001) | true | ok | 2026-11-21 19:25 | 2026-11-21 18:25 | — | 0 | — |
| 7 | verificador-qualidade-zambria (verificador-qualidade-001) | true | ok | 2026-11-21 19:13 | 2026-11-21 18:13 | — | 0 | — |
| 8 | webmaster-zambria (webmaster-001) | false | ok | 2026-11-21 17:25 | 2026-11-21 16:25 (VENCIDO) | — | 0 | Usuário — correção necessária |
| 9 | supervisor-fiscal-zambria (supervisor-fiscal-001) | true | ok | 2026-11-21 19:30 | 2026-11-21 18:30 | — | 0 | — |
| 10 | sincronizador-onedrive-zambria (sync-onedrive-001) | false | ok | 2026-11-21 17:37 | 2026-11-21 16:37 (VENCIDO) | — | 0 | Usuário — não essencial |
| 11 | ficcao-criador-zambria (ficcao-criador-001) | false | ok | 2026-11-21 17:23 | 2026-11-21 16:23 (VENCIDO) | "interrupted" em 21/11 00:23 -02 | 0 | Usuário — correção necessária |
| 12 | auditor-estrutura-zambria (auditor-estrutura-001) | false | ok | 2026-11-21 17:25 | 2026-11-21 16:25 (VENCIDO) | — | 0 | Usuário — correção necessária |
| 13 | guardiao-visual-zambria (guardiao-visual-001) | true | ok | 2026-11-21 19:56 | 2026-11-21 18:56 | — | 0 | — |

Novos jobs cadastrados desde o relatório anterior: auditor-estrutura-zambria e guardiao-visual-zambria.

---

## 2. Logs das últimas 24h

Busca por padrões de erro (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError) nos logs do workdir (logs/) e do Hermes:

- **HTTP 429 (Too Many Requests):** pesquisador-profundo-zambria (18/11 17:27 -02) e revisor-editorial-zambria (18/11 21:01 -02). Erros temporários, já recuperados (`last_status: ok`, `failure_streak: 0`). Fora da janela de 24h desta execução, mas mantidos no registro. **Não pausar** (regra: erro temporário não pausa).
- **RuntimeError:** ficcao-criador-zambria — "interrupted" (cron fire ownership lost durante drain do gateway) em 21/11 00:23 -02 (20/11 23:23 -03). Interrupção transitória de infraestrutura, já recuperada. **Não pausar**.
- **SyntaxError:** 20/11 18:48:48 — execução terminal avulsa via agent.tool_executor, não vinculada a job cron, isolado. **Não pausar**.
- **FileNotFoundError:** nenhuma ocorrência.
- Nenhum erro novo registrado neste ciclo (17:30 -03).

`logs/qualidade/` contém bloqueios editoriais do Verificador de Qualidade (plágio, texto não corrigido, ortografia) — **gatekeeping normal, não erro de sistema**. Não geram pausa de job nem alerta crítico. Inclui o bloqueio de `o-laudo-do-turno-da-noite` por `publicar: false` — regra de segurança respeitada (primeira história do Criador de Ficção mantida fora do fluxo de publicação).

---

## 3. Erros conhecidos no jobs.json (last_failure)

Todos com `failure_streak: 0` e `last_status: ok` — já recuperados, sem ação do supervisor.

| Job | last_failure | Classificação | Ação do supervisor |
|-----|--------------|---------------|--------------------|
| pesquisador-profundo-zambria | HTTP 429 em 18/11 | Temporário, recuperado | Registrado apenas. Não pausar. |
| revisor-editorial-zambria | HTTP 429 em 18/11 | Temporário, recuperado | Registrado apenas. Não pausar. |
| escritor-especializado-zambria | RuntimeStoreError invalid_params em 18/11 | Recuperado | Sem ação. |
| ficcao-criador-zambria | "interrupted" em 21/11 00:23 -02 | Transitória, recuperada | Registrada apenas. Não pausar. |
| Demais 9 jobs | — | Sem falha | Sem ação. |

---

## 4. Jobs com next_run_at vencido

Cinco jobs têm `next_run_at` já passado em relação a 17:30 -03 (18:30 -02):

| Job | next_run_at (-03) | Estado | Motivo |
|-----|-------------------|--------|--------|
| pesq-ativo-zambria-001 | 2026-11-21 16:57 | Pausado | Usuário — correção necessária |
| webmaster-zambria | 2026-11-21 16:25 | Pausado | Usuário — correção necessária |
| sincronizador-onedrive-zambria | 2026-11-21 16:37 | Desativado | Usuário — não essencial |
| ficcao-criador-zambria | 2026-11-21 16:23 | Pausado | Usuário — correção necessária |
| auditor-estrutura-zambria | 2026-11-21 16:25 | Pausado | Usuário — correção necessária |

**Ação:** nenhuma reexecução forçada. Todos estão `enabled: false` por decisão explícita do usuário; o supervisor não sobrepõe pausas do usuário. Nenhum job `enabled: true` tem janela vencida.

---

## 5. Estrutura do site (monitoramento obrigatório)

1. **index.html → posts/:** 16 links para `.html` em `posts/`. Todos resolvem para arquivos existentes. **Sem links quebrados.**
2. **Arquivos órfãos em posts/:** nenhum — todos os 16 arquivos `.html` estão referenciados em index.html.
3. **Botão toggle fixo:** existe em index.html (`id="btnToggleSidebar"`) e `style.css` define `position: fixed; top: 1rem; left: 1rem; z-index: 1000;` — sempre visível no canto superior esquerdo. **OK.**
4. **review/ficcoes/:** pasta ativa com histórias do Criador de Ficção. Primeira história ("O Laudo do Turno da Noite") com `publicar: false` — mantida fora do fluxo de publicação (regra de segurança respeitada).

**Nenhuma inconsistência estrutural encontrada.** Sem necessidade de acionar Curador-Chefe ou Publicador para correção.

---

## 6. Ações tomadas neste ciclo

- Nenhum job pausado (não houve erro persistente: sem SyntaxError nem FileNotFoundError vinculados a jobs cron).
- Nenhum job reexecutado forçadamente (todos os vencidos estão pausados pelo usuário).
- `jobs.json`: sem alterações.
- Relatório de saúde gravado em `logs/supervisor/relatorio-saude-2026-11-21-1730.md`.

---

## 7. Alertas enviados ao Curador-Chefe

**Nenhum alerta crítico neste ciclo.** Pipeline não travado: todos os 8 jobs habilitados têm próxima execução no futuro.

---

## 8. Conclusão

O pipeline ZAMBRIA está operando sem interrupções neste ciclo:

- 13 jobs cadastrados; 8 habilitados com `last_status: ok` e próximo disparo no futuro.
- 5 jobs pausados/desativados por decisão do usuário (não por erro do sistema).
- Erros recentes apenas transitórios (HTTP 429 recuperados, interrupção de infraestrutura do ficcao-criador recuperada). `failure_streak: 0` em todos.
- Sem `FileNotFoundError` nem `SyntaxError` em jobs cron. Estrutura do site OK.
- Pipeline não travado. Curador-Chefe não precisa ser acionado.

*Gerado pelo Agente Supervisor Fiscal ZAMBRIA. Um ciclo concluído.*
