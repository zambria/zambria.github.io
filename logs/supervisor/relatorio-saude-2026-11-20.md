# Relatório de Saúde — Supervisor Fiscal ZAMBRIA

**Execução:** 2026-11-20 22:04 -03 (UTC-03:00)
**Workdir:** C:/Users/erico/zambria.github.io/

## 1. jobs.json — registro de jobs
**Status: AUSENTE (erro persistente — arquivo faltando)**

jobs.json não foi encontrado na raiz do workdir. Não foi possível ler `enabled`, `last_status` nem `next_run_at` de nenhum job. Classificado como erro persistente (arquivo faltando) e **alerta crítico**. Não há jobs cadastrados para pausar ou reativar neste ciclo (não há registro de jobs para modificar).

**Ação tomada:** alerta crítico registrado neste relatório e Curador-Chefe informado. Recomendação: criar jobs.json com o registro dos jobs do pipeline (pesquisador-ativo, escritor, revisor-editorial, publicador, pesquisador-profundo, sincronizador-onedrive) para permitir o monitoramento de enabled/last_status/next_run_at nos próximos ciclos.

## 2. Logs das últimas 24h
- logs/curador-decisoes.jsonl: 6 decisões registradas em 2026-11-20T21:58:00-03:00, todas sem erro (avaliação de pesquisas, nomeação de tópicos, seleção de profundidade, revisão de pendentes, sem conflito Escritor/Revisor, publicador).
- logs/supervisor/: vazio (não há relatórios anteriores).
- logs/qualidade/: vazio.
- logs/curador/: vazio.

**Busca por erros (HTTP 429, RuntimeError, SyntaxError, FileNotFoundError):** nenhuma ocorrência encontrada. Sem erros temporários e sem erros persistentes de execução nas últimas 24h.

## 3. Estado dos agentes
- **Pesquisador Ativo (estado-pesquisador.json):** 9 tópicos com status `ok` (ufo, arch, para, crypto, conspir, nature, contos-01 a contos-04); última busca 2026-11-20T21:04:00-03:00; intervalo 6h; próxima execução 2026-11-21T03:04:00-03:00. **Não atrasada** — nenhuma reexecução forçada necessária.
- **Publicador (estado-publicador.json):** 0 publicações hoje, `total_publicados: 0`, aguardando textos aprovados do Escritor. Por decisão de curadoria (fluxo normal), não é erro.
- **drafted.json:** 9 pesquisas processadas, "ufo" em rascunho, atualizado em 2026-11-20T22:01:00-03:00.
- **review/pendentes:** 9 textos aguardando ajustes de forma e convenção do Escritor antes da aprovação final (fluxo normal, não erro).

## 4. Conclusão
O pipeline não apresenta erros de execução nas últimas 24h. O ponto crítico é a ausência do registro de jobs (jobs.json): sem ele, o Supervisor Fiscal não tem jobs para monitorar quanto a enabled/last_status/next_run_at. Pipeline operando, mas sem registro de agendamento visível ao supervisor.
