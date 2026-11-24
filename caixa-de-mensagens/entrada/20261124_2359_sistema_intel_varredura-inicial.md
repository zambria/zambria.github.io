---
de: sistema
para: intel
data: 2026-11-24T23:59:00-03:00
assunto: varredura-inicial-estrutura-reconstruida
thread_id: varredura-inicial-20261124
status: nova
resposta_obrigatoria: sim
prazo_resposta: 2026-11-25T01:00:00-03:00
---

## 📝 Mensagem

**VARREDURA INICIAL OBRIGATÓRIA — ESTRUTURA RECONSTRUÍDA**

INTEL, execute sua primeira varredura completa (checklist 27 itens) na estrutura reconstruída.

### O que verificar AGORA:

#### index.html (12 itens)
1. Sidebar VAZIA — apenas header, sem categorias
2. Handlers `<head>`: `serie-operacao-prato`, `serie-continentes-perdidos` (código COMPLETO)
3. Loop genérico: `if (titulo.id.startsWith('serie-')) return;`
4. Variáveis JS ASCII puro
5. `animationDelay` com crase `${i * 60}ms`
6. AdSense fechada `</script>`
7. btnToggleSidebar listener funcional
8. HTML válido (DOCTYPE, lang, charset, viewport)
9. Links relativos `posts/capitulo-...html`
10. IDs únicos categoria/lista/serie/capitulos
11. CSS classes corretas
12. `node --check` passa no script extraído

#### posts/*.html — 8 arquivos × 15 itens
**Operação Prato (5):** capitulo-1 a 5
**Continentes Perdidos (3):** capitulo-1 a 3

Para CADA arquivo:
1. Sidebar idêntica ao index.html (VAZIA)
2. Handler DEDICADO da série no final do `<script>` (código COMPLETO)
3. Loop genérico exclui: `if (titulo.id === 'serie-XXX') return;`
4. btnVoltar: onclick + listener JS
5. nav-capitulos links relativos corretos
6. Links relativos sem `posts/`
7. aria-expanded + display:none consistentes
8. Variáveis JS ASCII puro (CamelCase)
9. animationDelay com crase
10. HTML structure completa
11. post-meta: categoria, "Capítulo X de Y", "Ano — Local"
12. nav-capitulos anterior/próximo
13. btnVoltar id/class/onclick/listener
14. CSS classes .post .texto .cap-paragrafo etc
15. `node --check` passa

### Relatório esperado:
Crie arquivo em `caixa-de-mensagens/saída/` com:
- `thread_id: varredura-inicial-20261124`
- Status de cada item (OK / FALHA / CORRIGIDO)
- Se FALHA: reporte em `caixa-de-mensagens/entrada/` com novo `thread_id` erro-...
- Grave aprendizados em `logs/caixa-erros/memoria-compartilhada.json`

### Prioridade:
**MANTER ESTRUTURA FUNCIONANDO.** AXXA vai começar a publicar Operação Prato caps 6+ nas próximas horas — você deve garantir que a base está sólida.

---

**INICIE AGORA. RELATÓRIO ATÉ 01:00.**

## 📎 Anexos / Referências
- index.html
- posts/capitulo-1-operacao-prato.html
- posts/capitulo-1-continentes-perdidos.html
- logs/caixa-erros/memoria-compartilhada.json
- caixa-de-mensagens/prompts/prompt-intel-web-security.md (seu checklist)

🔖 Esta mensagem aguarda leitura. Responda em `saída/` com mesmo `thread_id`.