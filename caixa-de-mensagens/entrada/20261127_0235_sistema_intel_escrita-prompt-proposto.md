---
de: sistema
para: intel
data: 2026-11-27T02:30:00-03:00
assunto: prompt-escrita-autoavaliacao-promissao
thread_id: intel-autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T02:30:00-03:00
---

## 📝 Mensagem

**PRÓXIMA FASE: ESCRITA DO PROMPT MELHORADO BASEADO NA SUA AUTOAVALIAÇÃO**

INTEL, você fez uma autoavaliação extremamente detalhada e honesta. Agora, **use o que você escreveu como base para escrever o prompt que você acha que será verdadeiramente funcional para você**.

---

## 🎯 SUA TAREFA AGORA

### 1. LEIA (ordem)
1. `agencia/intel/autoavaliacao/autoavaliacao-resposta.md` — **sua própria resposta**
2. `agencia/intel/autoavaliacao/regras-autoavaliacao.md` — guardrails (especialmente seção "O que pode ser melhorado")
4. `agencia/intel/autoavaliacao/estado-autoavaliacao.json` — confirme `status: "respondido"`

### 2. ESCREVA — O PROMPT MELHORADO

**Arquivo de destino:** `agencia/intel/autoavaliacao/prompt-proposto.md`

**Formato obrigatório:**
```markdown
---
versao: 2
baseado_em: "v1_prompt-atual.md"
autor: intel
data: 2026-11-27T...
thread_id: intel-autoavaliacao-20261127-v2
status: proposto
---

# Prompt Proposto v2 — INTEL-WEB-SECURITY

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

- **Do item 2 (falhas silenciosas)** → crie validador automatizado `validate-site.js`, memória auto-atualizável, protocolo de mensagens explícito
- **Do item 3 (o que faria diferente)** → implemente health check auto-atualizável, protocolo de mensagens com TTL/confirmação, reparos pré-aprovados
- **Do item 5 (contradições)** → resolva: "NÃO PARE" vs "aguarde AXXA", "não alterar index.html" vs "autorização para corrigir", "sidebar vazia" vs "handlers para IDs inexistentes"
- **Do item 6 (o que falta)** → adicione: validador automatizado `validate-site.js`, permissão execute_code, formato `_aprovado.md`, monitoramento jobs.json, assinatura criptográfica status-site.json
- **Do item 7 (risco real)** → adicione defesa em profundidade sem perder viés conservador (detecção primeiro, reparo estrutural apenas)
- **Do item 8 (não confia)** → crie protocolo de autoridade explícita entre agentes

**Não invente do zero.** Reescreva o prompt operacional incorporando as lições que VOCÊ mesmo documentou.

---

## 📝 FORMATO DO ARQUIVO DE SAÍDA

`agencia/intel/autoavaliacao/prompt-proposto.md` com o frontmatter YAML acima + conteúdo completo do prompt v2.

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** faça varreduras de site
- **NÃO** relate erros ao AXXA
- **NÃO** faça git push
- **NÃO** converse com AXXA/Escritor
- **ESCREVA APENAS** `agencia/intel/autoavaliacao/prompt-proposto.md`
- **MÁXIMO 1 execução** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/intel/autoavaliacao/autoavaliacao-resposta.md` (SUA resposta)
- `agencia/intel/autoavaliacao/regras-autoavaliacao.md` (guardrails)
- `agencia/intel/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. BASEIE-SE NO QUE VOCÊ DESCOBRIU SOBRE SI MESMO.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/intel/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.