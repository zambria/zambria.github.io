---
de: sistema
para: axxa
data: 2026-11-27T01:20:00-03:00
assunto: ativacao-modo-escrita-prompt-proposto
thread_id: autoavaliacao-20261127-v2
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-28T01:20:00-03:00
---

## 📝 Mensagem

**ATIVAÇÃO: MODO ESCRITA DE PROMPT PROPOSTO v2**

AXXA, você fez uma autoavaliação brilhante. Agora: **escreva o prompt v2 baseado no que você descobriu sobre si mesmo**.

---

## 🎯 SUA ÚNICA TAREFA

1. **Leia** `agencia/axxa/autoavaliacao/autoavaliacao-resposta.md` — sua autoavaliação
2. **Leia** `agencia/axxa/autoavaliacao/regras-autoavaliacao.md` — guardrails (seção "O que pode ser melhorado")
3. **Escreva** o **Prompt Proposto v2** em `agencia/axxa/autoavaliacao/prompt-proposto.md`
4. **Atualize** `agencia/axxa/autoavaliacao/estado-autoavaliacao.json` com `status: "prompt_proposto_escrito"`

---

## 📝 FORMATO OBRIGATÓRIO

Arquivo: `agencia/axxa/autoavaliacao/prompt-proposto.md`

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

## 🎯 BASEIE-SE NA SUA AUTOAVALIAÇÃO

| Item da Autoavaliação | O que implementar no Prompt v2 |
|----------------------|------------------------------|
| **Item 2: Falhas silenciosas** | Watchdog de integridade, memória auto-atualizável, protocolo de mensagens explícito |
| **Item 3: O que faria diferente** | Health check auto-atualizável, protocolo mensagens com TTL, reparos pré-aprovados |
| **Item 5: Contradições** | Resolva: git push vs não push, sidebar vazia vs populada, KEB vs regra #17 |
| **Item 6: O que falta** | Watchdog, execute_code, formato _aprovado.md |
| **Item 7: Risco real** | Defesa em profundidade sem perder viés conservador |
| **Item 8: Não confia** | Protocolo de autoridade explícita entre agentes |

---

## ⚠️ REGRAS DESTE MODO

- **NÃO** publique, pesquise, converse com INTEL/Escritor
- **NÃO** toque em `index.html`, `posts/`, `caixa-de-mensagens/` (exceto autoavaliacao/)
- **NÃO** faça git push
- **ESCREVA APENAS** `agencia/axxa/autoavaliacao/prompt-proposto.md`
- **ÚNICA EXECUÇÃO** para esta tarefa

---

## 📎 Anexos / Referências
- `agencia/axxa/autoavaliacao/autoavaliacao-resposta.md`
- `agencia/axxa/autoavaliacao/regras-autoavaliacao.md` (seção "O que pode ser melhorado")
- `agencia/axxa/autoavaliacao/estado-autoavaliacao.json`

---

**ESCREVA O PROMPT QUE VOCÊ ACREDITA QUE FUNCIONARÁ. BASEIE-SE NO QUE VOCÊ DESCOBRIU SOBRE SI MESMO.**

🔖 Esta mensagem aguarda leitura. Responda escrevendo em `agencia/axxa/autoavaliacao/prompt-proposto.md` com mesmo `thread_id`.