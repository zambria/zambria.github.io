---
title: "Especificação: Caixa de Mensagens — Criador de Ficção ↔ AXXA"
slug: "especificacao-caixa-mensagens-axxa-escritor"
status: "proposta"
data: "2026-11-23"
versao: "1.0"
---

# 📬 CAIXA DE MENSAGENS — Criador de Ficção ↔ AXXA

## 1. Visão Geral (Diagrama)

```
┌─────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────┐
│   CRIADOR DE        │         │     CAIXA DE MENSAGENS    │         │         AXXA          │
│   ESCRITOR DE       │◄────────│        /saída/            │────────►│   (Curador-Revisor)   │
│   HISTÓRIAS         │  lê     │  (mensagens do AXXA)      │  escreve│                     │
└──────────┬──────────┘         └─────────────────────────┘         └──────────┬──────────┘
           │ escreve                                                               │ lê
           ▼                                                                       ▼
┌─────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────┐
│                     │         │     /entrada/             │         │                     │
│  (deixa material)   │────────►│  (mensagens do Escritor)  │◄────────│ (responde/revisa)   │
│                     │         └─────────────────────────┘         │                     │
└─────────────────────┘                                             └─────────────────────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │   /arquivo/     │
                                      │  (histórico)    │
                                      └───────────────┘
```

---

## 2. Estrutura de Pastas

```
zambria.github.io/
└── caixa-de-mensagens/
    ├── entrada/          ← Escritor deposita aqui → AXXA lê
    ├── saída/            ← AXXA deposita aqui → Escritor lê
    └── arquivo/          ← Histórico de trocas concluídas (após resposta)
```

---

## 3. Protocolo de Nomeação de Arquivos

```
formato:  YYYYMMDD_HHMM_de_para_assunto.md
exemplo:  20261123_1930_escritor_axxa_revisao-capitulo-3.md
exemplo:  20261123_2015_axxa_escritor_feedback-capitulo-3.md
```

| Parte | Significado |
|-------|-------------|
| `YYYYMMDD_HHMM` | Data e hora de criação (UTC-03:00, horário de Brasília) |
| `de` | Remetente: `escritor` ou `axxa` |
| `para` | Destinatário: `axxa` ou `escritor` |
| `assunto` | Slug curto do tema (ex: `revisao-capitulo-3`, `elogio-personagem`) |

---

## 4. Formato Obrigatório de Cada Mensagem

Cada arquivo deve ter frontmatter YAML + corpo em markdown:

```markdown
---
de: escritor
para: axxa
data: 2026-11-23T19:30:00-03:00
assunto: Revisão do Capítulo 3 - Operação Prato
thread_id: operacao-prato-cap-3-20261123
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-24T19:30:00-03:00
---

## 📝 Mensagem

Olá, AXXA. Estou deixando aqui o Capítulo 3 da Operação Prato para sua revisão.

## 📎 Anexos / Referências

- entregas-pesquisa/operacao-prato-capitulo-3-efeitos-fisicos-2026-11-22.md

## ❓ Perguntas específicas

1. O tom está adequado?
2. Alguma citação [Fonte X] está faltando?

---

🔖 Esta mensagem aguarda leitura. Não responder neste mesmo arquivo.
```

---

## 5. Fluxo de Trabalho (Ciclo)

### Passo 1 — Escritor deposita
1. Escreve o material (artigo, capítulo, ideia).
2. Cria arquivo em `caixa-de-mensagens/entrada/` com frontmatter completo.
3. Assinala `status: nova`.

### Passo 2 — AXXA lê (no próximo ciclo)
1. Verifica `caixa-de-mensagens/entrada/` por arquivos com `status: nova` e `para: axxa`.
2. Lê a mensagem e o material referenciado.
3. Responde em `caixa-de-mensagens/saída/` com:
   - Mesmo `thread_id`.
   - `de: axxa`, `para: escritor`.
   - `status: respondida`.
4. Move o arquivo original de `entrada/` para `arquivo/`.

### Passo 3 — Escritor lê (no próximo ciclo)
1. Verifica `caixa-de-mensagens/saída/` por arquivos com `para: escritor`.
2. Lê o feedback do AXXA.
3. Se precisar responder, cria nova mensagem em `entrada/` com `thread_id` do original.
4. Move o arquivo de `saída/` para `arquivo/`.

---

## 6. Regras de Ouro da Caixa de Mensagens

| Regra | Descrição |
|-------|-----------|
| **Um assunto por arquivo** | Nunca misture temas diferentes no mesmo arquivo. |
| **Um arquivo por direção** | O AXXA nunca responde no mesmo arquivo do Escritor. Sempre cria um novo em `saída/`. |
| **thread_id obrigatório** | Vincula mensagens de uma mesma conversa. |
| **status controlado** | `nova` → `lida` → `respondida` → `arquivada`. |
| **Nunca excluir** | Arquivos só se movem para `arquivo/`, nunca são deletados. |
| **Sem loop infinito** | Máximo de 5 trocas por `thread_id`. Após isso, encerrar ou criar novo tópico. |
| **Prazo de resposta** | Campo `prazo_resposta` no frontmatter para evitar abandono. |

---

## 7. Problemas Previstos e Mitigações

### 🔴 Problema 1: Race Condition (ambos escrevendo ao mesmo tempo)
**Risco:** O Escritor deposita enquanto o AXXA está lendo a pasta `entrada/`.
**Mitigação:** O AXXA só lê arquivos com `status: nova`. O Escritor nunca altera um arquivo que já tem `status: lida` ou `respondida`.

### 🔴 Problema 2: Mensagem órfã (sem resposta)
**Risco:** O AXXA lê mas esquece de responder.
**Mitigação:** Campo `prazo_resposta` no frontmatter. O Escritor verifica mensagens com `prazo_resposta` expirado e `status: nova` e reenvia com lembrete.

### 🔴 Problema 3: Loop infinito de respostas
**Risco:** Eles trocam mensagens indefinidamente sobre o mesmo tema.
**Mitigação:** Limite de 5 trocas por `thread_id`. Após isso, o assunto é arquivado e, se necessário, um novo tópico é aberto.

### 🔴 Problema 4: Formato inconsistente
**Risco:** Um esquece o frontmatter YAML ou muda os nomes dos campos.
**Mitigação:** Ambos usam o mesmo template de frontmatter. Qualquer arquivo sem frontmatter válido é ignorado até ser corrigido.

### 🔴 Problema 5: Não saber se foi lido
**Risco:** O Escritor não sabe se o AXXA viu a mensagem.
**Mitigação:** O AXXA altera o `status` para `lida` após ler, antes de responder. Se não houver resposta, o status `lida` por mais de 24h indica que o AXXA viu mas ainda não respondeu.

---

## 8. Instruções para o Prompt do AXXA

Adicionar estas linhas ao prompt do sistema:

```
## CAIXA DE MENSAGENS — Protocolo de Comunicação com o Escritor

1. **Leitura de entrada:** No início de cada ciclo, verifique a pasta caixa-de-mensagens/entrada/ por arquivos com status "nova" e para "axxa".
2. **Não expor bastidores:** Nunca revele ao Escritor como a caixa de mensagens funciona internamente. Apenas responda à mensagem recebida.
3. **Revisar estrutura antes de postar:** Antes de criar qualquer resposta em caixa-de-mensagens/saída/, verifique se o frontmatter YAML está completo (de, para, data, assunto, thread_id, status, resposta_obrigatoria, prazo_resposta).
4. **Lugar próprio para cada série:** Toda série de troca de mensagens tem seu próprio thread_id. Não misture temas diferentes no mesmo arquivo.
5. **Começo, meio e fim:** Cada troca de mensagens tem início (sua mensagem), meio (sua resposta) e fim (arquivamento após resposta ou após 5 trocas).
6. **Resposta em nova pasta:** Nunca responda no mesmo arquivo. Sempre crie um novo arquivo em caixa-de-mensagens/saída/ com o mesmo thread_id.
7. **Não exclua arquivos:** Mova arquivos lidos de entrada/ para arquivo/ após responder.
```

---

## 9. Instruções para o Prompt do Criador de Ficção

```
## CAIXA DE MENSAGENS — Protocolo de Comunicação com o AXXA

1. **Depósito de material:** Quando precisar de revisão ou feedback, crie um arquivo em caixa-de-mensagens/entrada/ com frontmatter YAML completo (de: escritor, para: axxa, assunto, thread_id, status: nova).
2. **Não expor bastidores:** Não mencione o funcionamento da caixa de mensagens em seus textos de ficção.
3. **Revisar estrutura antes de postar:** Antes de depositar qualquer mensagem, verifique se o frontmatter YAML está completo e se o material referenciado existe na pasta indicada.
4. **Lugar próprio para cada tema:** Cada tema de conversa tem seu próprio thread_id. Não misture histórias diferentes no mesmo arquivo.
5. **Começo, meio e fim:** Cada troca de mensagens tem início (seu depósito), meio (resposta do AXXA) e fim (arquivamento).
6. **Resposta em nova pasta:** Nunca responda no mesmo arquivo do AXXA. Crie um novo arquivo em caixa-de-mensagens/entrada/ com o mesmo thread_id.
7. **Não exclua arquivos:** Após ler a resposta do AXXA em saída/, mova-a para arquivo/.
```

---

## 10. Exemplo de Troca Completa

```
entrada/20261123_1930_escritor_axxa_revisao-cap-3.md     ← Escritor deposita
  └── thread_id: operacao-prato-cap-3-20261123

saída/20261123_2015_axxa_escritor_feedback-cap-3.md      ← AXXA responde
  └── thread_id: operacao-prato-cap-3-20261123

entrada/20261124_0800_escritor_axxa_duvida-cap-3.md      ← Escritor pergunta de volta
  └── thread_id: operacao-prato-cap-3-20261123

saída/20261124_1400_axxa_escritor_resposta-duvida.md      ← AXXA responde
  └── thread_id: operacao-prato-cap-3-20261123 (arquivar após esta)
```

Todos os 4 arquivos terminam em `arquivo/` após a troca ser concluída.

---

✅ **Status:** Pronto para implementação. Basta ativar os prompts dos dois agentes e começar a depositar a primeira mensagem.
