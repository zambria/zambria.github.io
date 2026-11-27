---
de: sistema
para: intel
data: 2026-11-27T02:40:00-03:00
assunto: ativacao-modo-escrita-prompt-proposto
thread_id: intel-autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T02:40:00-03:00
---

## 📝 Mensagem

**ATIVAÇÃO: MODO ESCRITA DE PROMPT PROPOSTO v2**

INTEL, você fez uma autoavaliação extremamente detalhada e honesta. Agora: **escreva o prompt v2 baseado no que você descobriu sobre si mesmo**.

---

## 🎯 SUA ÚNICA TAREFA

1. **Leia** `agencia/intel/autoavaliacao/autoavaliacao-resposta.md` — sua autoavaliação
2. **Leia** `agencia/intel/autoavaliacao/regras-autoavaliacao.md` — guardrails (seção "O que pode ser melhorado")
3. **Escreva** o **Prompt Proposto v2** em `agencia/intel/autoavaliacao/prompt-proposto.md`
4. **Atualize** `agencia/intel/autoavaliacao/estado-autoavaliacao.json` com `status: "prompt_proposto_escrito"`

---

## 📝 FORMATO OBRIGATÓRIO

Arquivo: `agencia/intel/autoavaliacao/prompt-proposto.md`

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

## 🎯 BASEIE-SE NA SUA AUTOAVALIAÇÃO

| Item da Autoavaliação | O que implementar no Prompt v2 |
|----------------------|------------------------------|
| **Item 2: Falhas silenciosas** | Validador automatizado `validate-site.js`, memória auto-atualizável com hash, protocolo de mensagens explícito com TTL/confirmação, reparos pré-aprovados baseados no que o patch toca |
| **Item 3: O que faria diferente** | Health check auto-atualizável assinado com hash, protocolo de mensagens com TTL/confirmação, reparos pré-aprovados baseados no que o patch toca |
| **Item 5: Contradições** | Resolva: "NÃO PARE" vs "aguarde AXXA" (timeout enforcado + fallback), "não alterar index.html" vs "autorização" (regra baseada no que o patch toca), "sidebar vazia" vs "handlers para IDs inexistentes" (validador verifica consistência) |
| **Item 6: O que falta** | Validador automatizado `validate-site.js`, permissão execute_code, formato `_aprovado.md`, monitoramento jobs.json com hash, assinatura criptográfica status-site.json |
| **Item 7: Risco real** | Defesa em profundidade sem perder viés conservador (detecção primeiro, reparo estrutural apenas), validador assinado com hash, rollback automático se 2 health checks falharem |
| **Item 8: Não confia** | Protocolo de autoridade explícita entre agentes (quem pode mutar o quê, com TTL e confirmação) |

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** faça varreduras de site
- **NÃO** relate erros ao AXXA
- **NÃO** faça git push
- **NÃO** converse com AXXA/Escritor
- **ESCREVA APENAS** `agencia/intel/autoavaliacao/prompt-proposto.md`
- **ÚNICA EXECUÇÃO** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/intel/autoavaliacao/autoavaliacao-resposta.md`
- `agencia/intel/autoavaliacao/regras-autoavaliacao.md` (seção "O que pode ser melhorado")
- `agencia/intel/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. BASEIE-SE NO QUE VOCÊ DESCOBRIU SOBRE SI MESMO.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/intel/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.