# CAIXA DE ERROS — Protocolo de Colaboração AXXA + Agente Parceiro

## Objetivo
Esta pasta é o canal exclusivo de troca entre o AXXA Web Sovereign e o outro agente que você está criando. Nenhum outro agente ou processo escreve aqui.

## Como funciona

### 1. Detecção de erro
Qualquer um dos dois agentes que encontrar um erro no site (botão quebrado, link 404, CSS faltando, tela branca, etc.) deve:

1.1 Criar um arquivo `.md` na pasta `entrada/` com nome no formato:
`erro-YYYYMMDD-HHMMSS-descricao-breve.md`

1.2 O conteúdo deve conter:
- Erro: descrição clara do problema
- Onde foi encontrado: caminho do arquivo e linha (se aplicável)
- Sintoma: o que o usuário vê ou experimenta
- Reportado por: nome do agente (AXXA ou nome do outro agente)
- Data/Hora: timestamp

### 2. Resolução
Qualquer um dos dois pode pegar o arquivo de `entrada/` e resolver:

2.1 Corrigir o erro no site
2.2 Mover o arquivo de `entrada/` para `resolvidos/`
2.3 No arquivo movido, adicionar uma seção:
## Resolução
- Corrigido por: nome do agente
- O que foi feito: descrição da correção
- Arquivos alterados: lista de caminhos
- Data/Hora: timestamp

### 3. Memória Compartilhada
Após resolver, ambos os agentes devem gravar o aprendizado em `memoria-compartilhada.json`:

```json
{
  "erro": "descrição curta",
  "sintoma": "o que acontecia",
  "solucao": "como foi corrigido",
  "arquivos": ["caminho1", "caminho2"],
  "regra_prevencao": "regra para evitar que aconteça novamente",
  "resolvido_por": "nome do agente",
  "data": "YYYY-MM-DD HH:MM"
}
```

### 4. Aprendizado Autônomo
Ambos os agentes devem:
- Ler `memoria-compartilhada.json` antes de iniciar qualquer ciclo de varredura
- Aplicar as regras de prevenção listadas lá
- Nunca reabrir um erro já resolvido
- Se um erro resolvido reaparecer, tratar como regressão crítica

## Regras de Ouro
- Não discuta erros fora desta pasta. Tudo fica registrado aqui.
- Não espere solicitação do usuário para resolver. Se encontrou, reporte e corrija.
- Nenhum dos dois apaga arquivos do outro.
- O arquivo `memoria-compartilhada.json` é de leitura e escrita para ambos.

---
Pasta criada em: `logs/caixa-erros/`
