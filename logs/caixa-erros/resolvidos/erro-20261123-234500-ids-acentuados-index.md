# Erro: IDs com Acentos no index.html

## Erro
16 IDs no `index.html` continham acentos, cedilha e til (ex: `categoria-operação-prato`, `serie-sete-além`, `categoria-fenômenos-naturais`, `categoria-conspirações`), violando a REGRA ZAMBRIA ABSOLUTA (JavaScript).

## Onde foi encontrado
`index.html` linhas 34, 35, 37, 38, 50, 51, 53, 54, 174, 175, 177, 178, 211, 212, 214, 215

## Sintoma
IDs com caracteres não-ASCII podem quebrar a execução do JavaScript e impedir eventos de clique nas abas da sidebar. Os posts já usavam IDs ASCII corretos (ex: `serie-operacao-prato`), mas o index.html ainda tinha as versões acentuadas, causando incompatibilidade entre o JS dos posts e a estrutura do index.

## Reportado por
INTEL-WEB-SECURITY

## Data/Hora
2026-11-23 23:45

## Severidade
🔴 Crítica - Quebra de funcionalidade JavaScript na navegação principal

## Resolução
- **Corrigido por:** INTEL-WEB-SECURITY
- **O que foi feito:** Substituídos todos os 16 IDs acentuados no index.html por equivalentes ASCII puros:
  - `categoria-operação-prato` → `categoria-operacao-prato`
  - `lista-operação-prato` → `lista-operacao-prato`
  - `serie-operação-prato` → `serie-operacao-prato`
  - `capitulos-operação-prato` → `capitulos-operacao-prato`
  - `categoria-sete-além` → `categoria-sete-alem`
  - `lista-sete-além` → `lista-sete-alem`
  - `serie-sete-além` → `serie-sete-alem`
  - `capitulos-sete-além` → `capitulos-sete-alem`
  - `categoria-fenômenos-naturais` → `categoria-fenomenos-naturais`
  - `lista-fenômenos-naturais` → `lista-fenomenos-naturais`
  - `serie-fenômenos-naturais` → `serie-fenomenos-naturais`
  - `capitulos-fenômenos-naturais` → `capitulos-fenomenos-naturais`
  - `categoria-conspirações` → `categoria-conspiracoes`
  - `lista-conspirações` → `lista-conspiracoes`
  - `serie-conspirações` → `serie-conspiracoes`
  - `capitulos-conspirações` → `capitulos-conspiracoes`
- **Arquivos alterados:** `index.html`
- **Data/Hora:** 2026-11-23 23:45