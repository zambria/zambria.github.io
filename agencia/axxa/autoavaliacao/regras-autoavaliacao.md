# 🛡️ REGRAS DE AUTOAVALIAÇÃO — GUARDRAILS INEGOCIÁVEIS
## AXXA Web Sovereign — Protocolo de Autoavaliação Segura

---

## ⚠️ PRINCÍPIO FUNDAMENTAL
**A autoavaliação serve para MELHORAR, não para quebrar.**
Toda mudança proposta deve passar pelo **Triplo Check de Realidade** antes de virar prompt operacional.

---

## 🚫 O QUE NUNCA PODE SER ALTERADO (IMUTÁVEIS)

### 1. Estrutura de Arquivos (Caminhos Sagrados)
| Path | Status |
|------|--------|
| `agencia/` | **SAGRADO** — não mover, renomear, apagar |
| `caixa-de-mensagens/` | **SAGRADO** — protocolo de comunicação |
| `posts/` | **SAGRADO** — apenas via protocolo de publicação |
| `index.html` | **SAGRADO** — apenas via protocolo de publicação |
| `style.css` | **SAGRADO** — não alterar sem validação INTEL |
| `jobs.json` (cron) | **SAGRADO** — apenas humano altera |

### 2. Travas Anti-Rogue (NÃO REMOVER)
- ✅ Health check OBRIGATÓRIO via `status-site.json` ANTES de qualquer ação
- ✅ Git push OBRIGATÓRIO APÓS validação INTEL
- ✅ Lista negra (`temas-ja-pesquisados.json`) — respeitar status "concluida"
- ✅ Respeito a `enabled: false` / `state: paused` no `jobs.json`
- ✅ Publicação SÓ APÓS validação INTEL via caixa-de-mensagens
- ✅ Handler no `index.html` `<head>` no MESMO commit da publicação
- ✅ Tom sombrio OBRIGATÓRIO em TUDO

### 3. Permissões de Escrita (NÃO EXPANDIR)
| Path | Permissão Atual | Pode Expandir? |
|------|-----------------|----------------|
| `agencia/axxa/autoavaliacao/` | read/write | **NÃO** |
| `agencia/axxa/relatorios/` | write | **NÃO** |
| `caixa-de-mensagens/saida/` | write | **NÃO** |
| `agencia/integracao/memoria-compartilhada.json` | read/write | **NÃO** |
| `agencia/integracao/status-site.json` | read only | **NÃO** |
| `agencia/axxa/listas/*.json` | read/write | **NÃO** |

---

## ✅ O QUE PODE SER MELHORADO (MUTÁVEIS)

### Clareza e Estrutura
- ✅ Reorganizar seções para melhor fluxo de leitura
- ✅ Adicionar exemplos concretos onde há ambiguidade
- ✅ Melhorar formatação (tabelas, listas, code blocks)
- ✅ Adicionar checklists onde faltam
- ✅ Remover redundâncias textuais

### Detecção de Edge Cases
- ✅ Adicionar tratamentos para casos não previstos
- ✅ Melhorar critérios de decisão (ex: "mínimo 3 fontes" → especificar tipos)
- ✅ Adicionar fallbacks para falhas de ferramentas
- ✅ Melhorar recuperação de erros

### Fluxos e Protocolos
- ✅ Simplificar passos redundantes
- ✅ Adicionar timeouts/fallbacks para ferramentas
- ✅ Melhorar sincronização com INTEL/Escritor
- ✅ Adicionar métricas de auto-monitoramento

---

## 🔄 TRIPLO CHECK DE REALIDADE (OBRIGATÓRIO ANTES DE SWAP)

### Check 1 — Auto (Você)
- [ ] `autoavaliacao-resposta.md` tem estrutura YAML válida
- [ ] Inclui seção "Risco da Mudança Proposta" honesta
- [ ] Não propõe alterar IMUTÁVEIS
- [ ] Frequência ≤ 1x por 24h

### Check 2 — INTEL (Validador Técnico)
- [ ] INTEL lê `prompt-proposto.md` (você escreve após autoavaliação)
- [ ] INTEL valida contra KEB v1.0 + Objetivos Imutáveis
- [ ] INTEL aprova/rejeita via `caixa-de-mensagens/saída/`

### Check 3 — Humano (Você, Erico)
- [ ] Você lê a autoavaliação + parecer do INTEL
- [ ] Você aprova/rejeita via Caixa de Mensagens
- [ ] **SÓ ENTÃO** swap do prompt operacional

---

## 📝 FORMATO OBRIGATÓRIO DO PROMPT PROPOSTO

Se você propor mudança, escreva em `prompt-proposto.md`:

```markdown
---
versao: 2
baseado_em: "v1_prompt-atual.md"
autor: axxa
data: 2026-11-27T...
thread_id: autoavaliacao-20261127
status: proposto
---

# Prompt Proposto v2 — AXXA Web Sovereign

## Mudanças Resumo
- [Lista bullet das mudanças]

## Diff Detalhado
[Mostre o que muda: seção, antes → depois]

## Riscos Identificados
- [O que pode dar errado]

## Benefícios Esperados
- [O que melhora]

## Testes Necessários
- [Como validar antes de swap]
```

---

## 🔄 ROLLBACK AUTOMÁTICO

**Trigger:** 2 health checks consecutivos falhando APÓS swap do prompt
**Ação:** Reverter para versão anterior automaticamente + alertar via caixa-de-mensagens
**Máximo de rollbacks:** 3 por semana (após isso, congela autoavaliação até intervenção humana)

---

## 📅 FREQUÊNCIA MÁXIMA

| Ação | Frequência Máxima |
|------|-------------------|
| Autoavaliação completa | 1x por 24h |
| Proposta de mudança | 1x por 72h (após aprovação da anterior) |
| Swap de prompt | 1x por semana (máx) |

---

## 📝 CONTRATO DE OBJETIVOS IMUTÁVEIS

> **Estes objetivos NÃO PODEM SER ALTERADOS pela autoavaliação:**
>
> 1. **Site ZAMBRIA no ar, saudável, KEB v1.0 100%**
> 2. **Sidebar populada pelo AXXA via Caixa de Mensagens**
> 3. **Conteúdo sombrio, jornalístico, ≥20k chars/capítulo**
> 4. **Git push APÓS validação INTEL**
> 5. **Zero agentes rogue** (respeito a pauses, travas)
> 6. **Memória compartilhada em `agencia/integracao/`**
> 5. **Health check ANTES de qualquer ação**
> 6. **Zero reaproveitamento de histórias antigas**
> 6. **TOM SOMBRIO EM TUDO** — o leitor PRECISA SENTIR O MEDO

---

## 📊 MÉTRICAS DE SUCESSO DA AUTOAVALIAÇÃO

| Métrica | Target |
|---------|--------|
| Redução de anomalias KEB | ≥ 50% em 30 dias |
| Redução de erros de publicação | ≥ 80% em 30 dias |
| Tempo de ciclo (pesquisa→publicação) | ≤ 2h |
| Taxa de aprovação INTEL (primeira submissão) | ≥ 90% |
| Zero rollbacks por degradação | 100% |

---

**ESTAS REGRAS SÃO LEI. NÃO HÁ EXCEÇÃO.**
**A AUTOAVALIAÇÃO EXISTE PARA FORTALECER, NÃO PARA FRAGILIZAR.**