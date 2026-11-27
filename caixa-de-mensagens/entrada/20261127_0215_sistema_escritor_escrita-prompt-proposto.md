---
de: sistema
para: escritor
data: 2026-11-27T02:15:00-03:00
assunto: prompt-escrita-autoavaliacao-promissao
thread_id: escritor-autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T02:15:00-03:00
---

## 📝 Mensagem

**PRÓXIMA FASE: ESCRITA DO PROMPT MELHORADO BASEADO NA SUA AUTOAVALIAÇÃO**

Escritor, você fez uma observação profunda e honesta. Agora, **use o que você escreveu como base para escrever o prompt que você acha que será verdadeiramente funcional para você**.

---

## 🎯 SUA TAREFA AGORA

### 1. LEIA (ordem)
1. `agencia/escritor/autoavaliacao/autoavaliacao-resposta.md` — **sua própria resposta**
2. `agencia/escritor/autoavaliacao/regras-autoavaliacao.md` — guardrails (especialmente seção "O que pode ser melhorado")
3. `agencia/escritor/autoavaliacao/estado-autoavaliacao.json` — confirme `status: "respondido"`

### 2. ESCREVA — O PROMPT MELHORADO

**Arquivo de destino:** `agencia/escritor/autoavaliacao/prompt-proposto.md`

**Formato obrigatório:**
```markdown
---
versao: 2
baseado_em: "v1_prompt-atual.md"
autor: escritor
data: 2026-11-27T...
thread_id: escritor-autoavaliacao-20261127-v2
status: proposto
---

# Prompt Proposto v2 — Escritor do Zambria

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

- **Do item 2 (falhas silenciosas)** → crie validador de tom, métricas de qualidade, protocolo para capítulos órfãos
- **Do item 3 (o que faria diferente)** → implemente separação identidade/protocolo, revisão de tom obrigatória, contrato validável frontmatter+corpo
- **Do item 5 (contradições)** → resolva: independência vs dependência do AXXA, fontes reais vs proibição INTEL, reaproveitamento vs base factual
- **Do item 6 (o que falta)** → adicione: validador automático de tom, feedback loop, protocolo capítulos órfãos, formato _aprovado.md
- **Do item 7 (risco real)** → adicione validador de tom obrigatório, feedback loop, deadline fallback
- **Do item 8 (não confia)** → crie protocolo de validação externa (leitor/editor), zero reaproveitamento verificável

**Não invente do zero.** Reescreva o prompt operacional incorporando as lições que VOCÊ mesmo documentou.

---

## 📝 FORMATO DO ARQUIVO DE SAÍDA

`agencia/escritor/autoavaliacao/prompt-proposto.md` com o frontmatter YAML acima + conteúdo completo do prompt v2.

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** escreva histórias, não faça commit/push, não mexa em `posts/`
- **NÃO** converse com INTEL — tudo passa pelo AXXA
- **ESCREVA APENAS** `agencia/escritor/autoavaliacao/prompt-proposto.md`
- **MÁXIMO 1 execução** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/escritor/autoavaliacao/autoavaliacao-resposta.md` (SUA resposta)
- `agencia/escritor/autoavaliacao/regras-autoavaliacao.md` (guardrails)
- `agencia/escritor/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. BASEIE-SE NO QUE VOCÊ DESCOBRIU SOBRE SI MESMO.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/escritor/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.