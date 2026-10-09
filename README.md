# SISTEMA — treino estilo Solo Leveling

App web de treino em que você é o **Jogador** e o app é o **Sistema** que entrega missões.
Tudo em um único arquivo (`index.html`), funciona no celular e pode ser instalado como PWA.

## Funcionalidades
- **Missões diárias** curtas (5–15 min), com botão **Dia corrido** (versão mínima de 5 min) e **penalidade leve** se você perder um dia.
- **Missões semanais** com barra de progresso e dias restantes (km na semana, academia, sessão longa, dias ativos).
- **XP, níveis e ranks** E → D → C → B → A → S, com animação de LEVEL UP e RANK UP.
- **Atributos**: Força, Agilidade, Resistência e Disciplina (gráfico radar).
- **Dungeon (GPS)**: rastreamento de corrida/caminhada com mapa (Leaflet + OpenStreetMap), ritmo atual e médio, pausa automática, parciais por km e recordes pessoais.
- **Histórico** com calendário, registro manual e backup (exportar/importar).

Todo o progresso fica salvo no `localStorage` do navegador.

## Como usar
1. Ative o GitHub Pages: **Settings → Pages → Branch `main` / pasta `/ (root)` → Save**.
2. Abra `https://crispedtoast836.github.io/Solo-Leveling-Project/` no celular.
3. Instale na tela inicial:
   - **Android (Chrome):** menu ⋮ → "Instalar app".
   - **iPhone (Safari):** Compartilhar → "Adicionar à Tela de Início".

O GPS só funciona em **HTTPS** (o GitHub Pages já é HTTPS).

## Arquivos
| Arquivo | O que é |
|---|---|
| `index.html` | O app completo (HTML + CSS + JS). O balanceamento do jogo fica no objeto `CONFIG`, no topo do script. |
| `sw.js` | Service worker: deixa o app abrir offline. Ao atualizar o app, aumente o número em `CACHE`. |
