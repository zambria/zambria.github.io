# Relatório do Supervisor Fiscal ZAMBRIA

- **Site:** https://zambria.github.io
- **Repositório:** C:\Users\erico\zambria.github.io
- **Executado em:** 2026-11-18T11:25:10
- **Tom editorial ZAMBRIA:** sério, sombrio, adulto formal, sarcástico às vezes
- **Limite:** 2 posts/dia

## Resumo
- Verificações: 5 | OK: 4 | Problemas: 1
- **Status geral:** com_problemas

## Verificações
### ✅ CSS carregado
- Evidência: GET https://zambria.github.io/style.css -> HTTP 200, 4897 bytes

### ✅ Botão da sidebar
- Evidência: botao=True, js_toggle=True, aside=True
- Detalhes: {"botao_presente": true, "js_toggle_presente": true, "aside_presente": true}

### ❌ Posts ausentes / duplicados
- Evidência: online=['ovnis-e-uaps-quando-o-c-u-deixa-de-ser-identificado'], local=['ovnis-e-uaps-quando-o-c-u-deixa-de-ser-identificado']
- Problema: placeholder 'Nenhum post publicado ainda' visível apesar de já haver post(s) publicado(s)
- Sugere correção: Remover entradas duplicadas do index.html, apagar o bloco <div class="vazio"> quando houver posts, reenviar os posts faltantes e garantir que o publicador injete cada post uma única vez.
- Detalhes: {"posts_online": ["ovnis-e-uaps-quando-o-c-u-deixa-de-ser-identificado"], "posts_locais": ["ovnis-e-uaps-quando-o-c-u-deixa-de-ser-identificado"], "duplicados": [], "ausentes_online": [], "extras_online": [], "placeholder_vazio_visivel": true, "total_online": 1, "total_locais": 1}

### ✅ Limite de 2 posts por dia
- Evidência: 1/2 posts hoje (total 1, última 2026-11-18).
- Detalhes: {"posts_hoje": 1, "ultima_publicacao": "2026-11-18", "total_publicados": 1, "hoje": "2026-11-18", "limite": 2}

### ✅ Estrutura de pastas
- Evidência: drafts, review, posts, publicados presentes em zambria.github.io

## Estrutura esperada ZAMBRIA
- `/drafts/` — rascunhos do agente pesquisador/revisor
- `/review/` — conteúdos aprovados aguardando publicação
- `/posts/` — artigos publicados (HTML)
- `/publicados/` — fontes arquivadas (.md)

---
*Gerado pelo Agente Supervisor Fiscal ZAMBRIA.*