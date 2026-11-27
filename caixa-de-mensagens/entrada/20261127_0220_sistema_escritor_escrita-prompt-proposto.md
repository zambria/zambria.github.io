---
de: sistema
para: escritor
data: 2026-11-27T02:20:00-03:00
assunto: ativacao-modo-escrita-prompt-proposto
thread_id: escritor-autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T02:20:00-03:00
---

## 📝 Mensagem

**ATIVAÇÃO: MODO ESCRITA DE PROMPT PROPOSTO v2**

Escritor, você fez uma autoavaliação honesta e profunda. Agora: **escreva o prompt v2 baseado no que você descobriu sobre si mesmo**.

---

## 🎯 SUA ÚNICA TAREFA

1. **Leia** `agencia/escritor/autoavaliacao/autoavaliacao-resposta.md` — sua autoavaliação
2. **Leia** `agencia/escritor/autoavaliacao/regras-autoavaliacao.md` — guardrails (seção "O que pode ser melhorado")
3. **Escreva** o **Prompt Proposto v2** em `agencia/escritor/autoavaliacao/prompt-proposto.md`
4. **Atualize** `agencia/escritor/autoavaliacao/estado-autoavaliacao.json` com `status: "prompt_proposto_escrito"`

---

## 📝 FORMATO OBRIGATÓRIO

Arquivo: `agencia/escritor/autoavaliacao/prompt-proposto.md`

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

## 🎯 BASEIE-SE NA SUA AUTOAVALIAÇÃO

| Item da Autoavaliação | O que implementar no Prompt v2 |
|----------------------|------------------------------|
| **Item 2: Falhas silenciosas** | Validador obrigatório de tom, protocolo capítulos órfãos, formato `_aprovado.md` |
| **Item 3: O que faria diferente** | Separar identidade/protocolo, revisão de tom obrigatória, contrato frontmatter+corpo, deadline fallback |
| **Item 5: Contradições** | Resolver: independência vs dependência AXXA, fontes reais vs INTEL, reaproveitamento vs base factual |
| **Item 6: O que falta** | Validador de tom, formato `_aprovado.md`, protocolo capítulos órfãos, feedback loop |
| **Item 7: Risco real** | Validador de tom obrigatório (checklist dispositivos), feedback loop AXXA |
| **Item 8: Não confia** | Protocolo validação externa, hash similaridade, critério originalidade |

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** escreva histórias, não faça commit/push, não mexa em `posts/`
- **NÃO** converse com INTEL — tudo passa pelo AXXA
- **ESCREVA APENAS** `agencia/escritor/autoavaliacao/prompt-proposto.md`
- **ÚNICA EXECUÇÃO** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/escritor/autoavaliacao/autoavaliacao-resposta.md`
- `agencia/escritor/autoavaliacao/regras-autoavaliacao.md` (seção "O que pode ser melhorado")
- `agencia/escritor/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. BASEIE-SE NO QUE VOCÊ DESCOBRIU SOBRE SI MESMO.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/escritor/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.