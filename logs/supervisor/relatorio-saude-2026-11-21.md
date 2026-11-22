# Relatório de Saúde — Supervisor Fiscal ZAMBRIA

**Execução:** 2026-11-21 08:29 -03 (UTC-03:00)
**Workdir:** C:/Users/erico/zambria.github.io/
**Jobs monitorados:** 11 (todos listados em jobs.json)

---

## 1. jobs.json — registro de jobs

**Status: OK** — jobs.json lido com sucesso em C:/Users/erico/AppData/Local/hermes/cron/jobs.json.
Todos os 11 jobs estão `enabled: true` e `last_status: ok`. Nenhum job pausado. Nenhum `next_run_at` vencido em relação à hora da execução (08:29 -03); todos os próximos disparos estão no futuro, portanto nenhuma reexecução forçada é necessária neste ciclo.

| # | Job (id) | enabled | last_status | next_run_at (-03) | last_run_at (-03) | last_failure | streak |
|---|----------|---------|-------------|-------------------|-------------------|--------------|--------|
| 1 | pesquisador-profundo-zambria (pesq-zambria-001) | true | ok | 2026-11-21 08:53 | 2026-11-21 08:23 | HTTP 429 em 18/11 | 0 |
| 2 | escritor-especializado-zambria (escritor-zambria-001) | true | ok | 2026-11-21 08:32 | 2026-11-21 08:32 | RuntimeStoreError invalid_params em 18/11 | 0 |
| 3 | revisor-editorial-zambria (revisor-zambria-001) | true | ok | 2026-11-21 08:39 | 2026-11-21 08:39 | HTTP 429 em 18/11 | 0 |
| 4 | publicador-zambria-github-io (pub-zambria-001) | true | ok | 2026-11-21 09:00 | 2026-11-20 09:07 | — | 0 |
| 5 | pesq-ativo-zambria-001 (0f8fd715b3cc) | true | ok | 2026-11-21 08:32 | 2026-11-21 09:02 | — | 0 |
| 6 | curador-chefe-zambria (curador-chefe-001) | true | ok | 2026-11-21 08:46 | 2026-11-21 08:46 | — | 0 |
| 7 | verificador-qualidade-zambria (verificador-qualidade-001) | true | ok | 2026-11-21 08:45 | 2026-11-21 08:45 | — | 0 |
| 8 | webmaster-zambria (webmaster-001) | true | ok | 2026-11-21 08:54 | 2026-11-21 08:54 | — | 0 |
| 9 | supervisor-fiscal-zambria (supervisor-fiscal-001) | true | ok | 2026-11-21 09:29 | 2026-11-20 23:07 | — | 0 |
| 10 | sincronizador-onedrive-zambria (sync-onedrive-001) | true | ok | 2026-11-21 09:21 | 2026-11-21 09:21 | — | 0 |
| 11 | ficcao-criador-zambria (ficcao-criador-001) | true | ok | 2026-11-21 08:32 | 2026-11-21 09:27 | "interrupted" em 20/11 23:23 | 0 |

*Horários de jobs.json (offset -02:00) convertidos para -03:00 (hora local da execução).*

---

## 2. Logs das últimas 24h

**Busca por erros (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError):** nenhuma ocorrência encontrada nos arquivos de logs.

Arquivos de log presentes em logs/ (últimas 24h):
- logs/qualidade/2026-11-21-17-de-novembro-apagao-mundial-bloqueio-plagio.md
- logs/qualidade/2026-11-21-743-registros-bloqueio-plagio.md
- logs/qualidade/2026-11-21-aine-o-pantano-bloqueio-plagio.md
- logs/qualidade/2026-11-21-curupira-pes-virados-floresta-vinga-bloqueio-texto-nao-corrigido.md
- logs/qualidade/2026-11-21-o-laudo-do-turno-da-noite-bloqueio-publicar-falso.md

Os 5 arquivos em logs/qualidade/ são bloqueios editoriais do Verificador de Qualidade (plágio / texto não corrigido / publicar falso) — **ação de gatekeeping normal, não erro de sistema**. Não geram pausa de job nem alerta crítico.

---

## 3. Erros conhecidos no jobs.json (last_failure)

Todos com `failure_streak: 0` e `last_status: ok` — já recuperados.

| Job | last_failure | Classificação | Ação do supervisor |
|-----|--------------|---------------|--------------------|
| pesquisador-profundo-zambria | HTTP 429 (Too Many Requests) em 2026-11-18T17:27 -02 | Erro temporário (HTTP 429) | Registrado apenas. Não pausar (regra: erro temporário não pausa). |
| revisor-editorial-zambria | HTTP 429 (Too Many Requests) em 2026-11-18T21:01 -02 | Erro temporário (HTTP 429) | Registrado apenas. Não pausar. |
| escritor-especializado-zambria | RuntimeStoreError: invalid_params em 2026-11-18T19:15 -02 | Fora das últimas 24h; já recuperado | Registrado. Sem ação. |
| ficcao-criador-zambria | "interrupted" em 2026-11-21T00:23 -02 (20/11 23:23 -03) | Interrupção transitória — não é HTTP 429 / RuntimeError / SyntaxError / FileNotFoundError | Registrado apenas. last_status ok, streak 0. Não pausar. |

---

## 4. Jobs com next_run_at vencido

Nenhum. O disparo mais próximo é o publicador às 09:00 -03 (em ~31 minutos). Todas as janelas de execução estão no futuro. **Nenhuma reexecução forçada necessária.**

---

## 5. Conclusão

O pipeline ZAMBRIA está operando sem interrupções neste ciclo:

- 11 jobs cadastrados, todos habilitados (`enabled: true`), todos com `last_status: ok`.
- Zero erros de execução (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError) nos logs das últimas 24h.
- Bloqueios em logs/qualidade/ são gatekeeping editorial normal do Verificador de Qualidade, não falhas de sistema.
- O ficcao-criador sofreu uma interrupção transitória em 20/11 23:23 -03 e já se recuperou (streak 0, last_status ok).
- Nenhum job com `next_run_at` vencido; nenhuma reexecução forçada.
- Nenhum job pausado. Nenhum alerta crítico gerado.
- Pipeline não travado — **Curador-Chefe não precisa ser acionado** neste ciclo.

**Ação tomada:** relatório de saúde gravado em logs/supervisor/relatorio-saude-2026-11-21.md. Um ciclo concluído; nenhum job modificado.
