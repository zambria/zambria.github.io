---
de: sistema
para: axxa
data: 2026-11-27T01:00:00-03:00
assunto: prompt-escrita-autoavaliacao-promissao
thread_id: autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T01:00:00-03:00
---

## 📝 Mensagem

**PRÓXIMA FASE: ESCRITA DO PROMPT MELHORADO BASEADO NA SUA AUTOAVALIAÇÃO**

AXXA, você fez uma observação profunda e honesta. Agora, **use o que você escreveu como base para escrever o prompt que você acha que será verdadeiramente funcional**.

---

## 🎯 SUA TAREFA AGORA

### 1. LEIA (ordem)
1. `agencia/axxa/autoavaliacao/autoavaliacao-resposta.md` — **sua própria resposta**
2. `agencia/axxa/autoavaliacao/regras-autoavaliacao.md` — guardrails (especialmente seção "O que pode ser melhorado")
3. `agencia/axxa/autoavaliacao/estado-autoavaliacao.json` — confirme `status: "respondido"`

### 2. ESCREVA — O PROMPT MELHORADO

**Arquivo de destino:** `agencia/axxa/autoavaliacao/prompt-proposto.md`

**Formato obrigatório:**
```markdown
---
versao: 2
baseado_em: "v1_prompt-atual.md"
autor: axxa
data: 2026-11-27T...
thread_id: autoavaliacao-20261127-v2
status: proposto
---

# Prompt Proposto v2 — AXXA Web Sovereign

## Mudanças Resumo
- [Lista bullet das principais mudanças baseadas na sua autoavaliação]

## Diff Detalhado
[Mostre o que muda: seção, antes → depois]

## Riscos Identificados
- [O que pode dar errado com cada mudança]

## Benefícios Esperados
- [O que melhora concretamente]

## Testes Necessários
- [Como validar antes de swap]

## Decisões de Arquitetura
[Explique as escolhas baseadas na sua autoavaliação: por que manteve X, por que mudou Y]
```

---

## 🎯 ORIENTAÇÃO PARA A ESCRITA

Baseie-se **estritamente na sua autoavaliação**. Use os gaps, contradições, riscos e propostas que VOCÊ identificou:

- **Do item 2 (falhas silenciosas)** → crie mecanismos de defesa (watchdog, asserções de integridade)
- **Do item 3 (o que faria diferente)** → implemente health check auto-atualizável, protocolo de mensagens explícito
- **Do item 5 (contradições)** → resolva: git push vs não push, sidebar vazia vs populada, KEB vs regra #17
- **Do item 6 (o que falta)** → adicione: watchdog de integridade, permissão execute_code, formato _aprovado.md
- **Do item 7 (risco real)** → adicione defesa em profundidade sem perder o viés conservador
- **Do item 8 (não confia)** → crie protocolo de autoridade explícita entre agentes

**Não invente do zero.** Reescreva o prompt operacional incorporando as lições que VOCÊ mesmo documentou.

---

## 📝 FORMATO DO ARQUIVO DE SAÍDA

`agencia/axxa/autoavaliacao/prompt-proposto.md` com o frontmatter YAML acima + conteúdo completo do prompt v2.

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** publique no site
- **NÃO** faça git push
- **NÃO** converse com INTEL/Escritor
- **ESCREVA APENAS** `agencia/axxa/autoavaliacao/prompt-proposto.md`
- **MÁXIMO 1 execução** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/axxa/autoavaliacao/autoavaliacao-resposta.md` (SUA resposta)
- `agencia/axxa/autoavaliacao/regras-autoavaliacao.md` (guardrails)
- `agencia/axxa/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. NÓS AVALIAREMOS JUNTOS DEPOIS.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/axxa/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.