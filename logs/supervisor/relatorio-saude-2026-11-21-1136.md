# Relatório de Saúde — Supervisor Fiscal ZAMBRIA

**Execução:** 2026-11-21 11:36 -03 (UTC-03:00)
**Workdir:** C:/Users/erico/zambria.github.io/
**Jobs monitorados:** 11 (jobs.json em C:/Users/erico/AppData/Local/hermes/cron/jobs.json)
**Janela de logs analisada:** 2026-11-20 11:36 -03 até 2026-11-21 11:36 -03

---

## 1. jobs.json — registro de jobs

**Status: OK** — jobs.json lido com sucesso em C:/Users/erico/AppData/Local/hermes/cron/jobs.json.
Todos os 11 jobs estão `enabled: true` e `last_status: ok`. Nenhum job pausado. Nenhum `next_run_at` vencido em relação à hora desta execução (11:36 -03); todos os próximos disparos estão no futuro. **Nenhuma reexecução forçada necessária neste ciclo.**

*Horários de jobs.json (offset -02:00) convertidos para -03:00 (hora local da execução).*

| # | Job (id) | enabled | last_status | next_run_at (-03) | last_run_at (-03) | last_failure | streak |
|---|----------|---------|-------------|-------------------|-------------------|--------------|--------|
| 1 | pesquisador-profundo-zambria (pesq-zambria-001) | true | ok | 2026-11-21 12:06 | 2026-11-21 11:05 | HTTP 429 em 18/11 | 0 |
| 2 | escritor-especializado-zambria (escritor-zambria-001) | true | ok | 2026-11-21 11:43 | 2026-11-21 10:43 | RuntimeStoreError invalid_params em 18/11 | 0 |
| 3 | revisor-editorial-zambria (revisor-zambria-001) | true | ok | 2026-11-21 11:48 | 2026-11-21 10:48 | HTTP 429 em 18/11 | 0 |
| 4 | publicador-zambria-github-io (pub-zambria-001) | true | ok | 2026-11-21 12:04 | 2026-11-21 11:04 | — | 0 |
| 5 | pesq-ativo-zambria-001 (0f8fd715b3cc) | true | ok | 2026-11-21 11:53 | 2026-11-21 11:23 | — | 0 |
| 6 | curador-chefe-zambria (curador-chefe-001) | true | ok | 2026-11-21 11:57 | 2026-11-21 10:57 | — | 0 |
| 7 | verificador-qualidade-zambria (verificador-qualidade-001) | true | ok | 2026-11-21 11:54 | 2026-11-21 10:54 | — | 0 |
| 8 | webmaster-zambria (webmaster-001) | true | ok | 2026-11-21 12:02 | 2026-11-21 11:02 | — | 0 |
| 9 | supervisor-fiscal-zambria (supervisor-fiscal-001) | true | ok | 2026-11-21 12:36 | 2026-11-21 10:36 | — | 0 |
| 10 | sincronizador-onedrive-zambria (sync-onedrive-001) | true | ok | 2026-11-21 12:29 | 2026-11-21 11:29 | — | 0 |
| 11 | ficcao-criador-zambria (ficcao-criador-001) | true | ok | 2026-11-21 11:40 | 2026-11-21 11:29 | "interrupted" em 20/11 23:23 | 0 |

---

## 2. Logs das últimas 24h

**Busca por erros (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError):**

Arquivos consultados: `agent.log`, `errors.log`, `errors.log.1`, `gateway.log`, `gateway-stdio.log`, `managed-worker.log` (C:/Users/erico/AppData/Local/hermes/logs) e `logs/` do workdir.

| Ocorrência | Arquivo / Data | Classificação | Ação do supervisor |
|---|---|---|---|
| HTTP 429 (Too Many Requests) — múltiplos PIDs, 3 tentativas + fallback, esgotado | managed-worker.log, sessão ~20/11 23:2x | Erro temporário (HTTP 429) | Registrado apenas. **Não pausar** (regra: erro temporário não pausa). |
| RuntimeError: "Cron job 'ficcao-criador-zambria' was stopped: cron fire ownership was lost" | errors.log 2026-11-20 23:21:36 (durante drain/desligamento do gateway; 1 job em voo interrompido) | Interrupção transitória de infraestrutura, não erro de sintaxe/arquivo. Job já recuperado (last_status ok, streak 0). | Registrado apenas. **Não pausar**. |
| SyntaxError: unterminated triple-quoted string literal | errors.log 2026-11-20 18:48:48 (execução terminal avulsa via agent.tool_executor) | Isolado, não é job cron / não persiste em job | Registrado apenas. **Não pausar** (não vincula a job agendado). |
| FileNotFoundError | — | Nenhuma ocorrência | Sem ação. |

`logs/qualidade/` (7 arquivos em 21/11) e `logs/curador/` são bloqueios/decisões editoriais do Verificador de Qualidade e Curador — **gatekeeping normal, não erro de sistema**. Não geram pausa de job nem alerta crítico.

---

## 3. Erros conhecidos no jobs.json (last_failure)

Todos com `failure_streak: 0` e `last_status: ok` — já recuperados.

| Job | last_failure | Classificação | Ação do supervisor |
|-----|--------------|---------------|--------------------|
| pesquisador-profundo-zambria | HTTP 429 (Too Many Requests) 2026-11-18T17:27 -02 | Erro temporário (HTTP 429), fora das 24h | Registrado apenas. Não pausar. |
| revisor-editorial-zambria | HTTP 429 (Too Many Requests) 2026-11-18T21:01 -02 | Erro temporário (HTTP 429), fora das 24h | Registrado apenas. Não pausar. |
| escritor-especializado-zambria | RuntimeStoreError: invalid_params 2026-11-18T19:15 -02 | Fora das 24h; já recuperado | Registrado. Sem ação. |
| ficcao-criador-zambria | "interrupted" 2026-11-21T00:23 -02 (20/11 23:23 -03) | Interrupção transitória; já recuperado (streak 0) | Registrado apenas. Não pausar. |
| publicador, pesq-ativo, curador-chefe, verificador, webmaster, supervisor, sincronizador-onedrive | — | Sem falha registrada | Sem ação. |

---

## 4. Jobs com next_run_at vencido

**Nenhum.** O disparo mais próximo é `ficcao-criador-zambria` às 11:40 -03 (em ~4 minutos a partir desta execução). Todas as janelas de execução estão no futuro. **Nenhuma reexecução forçada necessária.**

---

## 5. Conclusão

O pipeline ZAMBRIA está operando sem interrupções neste ciclo:

- 11 jobs cadastrados, todos habilitados (`enabled: true`), todos com `last_status: ok`, `failure_streak: 0`.
- Erros nas últimas 24h: HTTP 429 (temporário, registrado, sem pausa), 1 RuntimeError transitório de `ficcao-criador-zambria` (recuperado), 1 SyntaxError de execução terminal avulsa (não é job cron). Sem `FileNotFoundError`.
- Nenhum erro persistente de sintaxe ou arquivo faltando vinculado a um job cron → **nenhum job pausado**.
- Nenhum alerta crítico gerado. **Curador-Chefe não precisa ser acionado.** Pipeline não travado.
- Nenhum job modificado neste ciclo.

*Observação:* este relatório (11:36 -03) corrige a execução anterior de hoje (08:29 -03), que não havia capturado os eventos HTTP 429 e de interrupção do ficcao-criador visíveis em managed-worker.log e errors.log.

**Ação tomada:** relatório de saúde gravado em logs/supervisor/relatorio-saude-2026-11-21-1136.md. Um ciclo concluído; nenhum job modificado.

*Gerado pelo Agente Supervisor Fiscal ZAMBRIA.*
