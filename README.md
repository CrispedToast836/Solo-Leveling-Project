# SISTEMA — treino estilo Solo Leveling

App de treino em que você é o **Jogador** e o app é o **Sistema** que entrega missões.
O mesmo código roda de dois jeitos:

- **Site (PWA)** pelo GitHub Pages: `https://crispedtoast836.github.io/Solo-Leveling-Project/`
- **App Android (.apk)** feito com Capacitor e compilado pelo GitHub Actions — com **GPS em segundo plano** (dá para correr com a tela bloqueada).

## Funcionalidades
- **Missões diárias** curtas (5–15 min), com botão **Dia corrido** e **penalidade leve** se você perder um dia.
- **Missões semanais**: km na semana, academia, sessão longa, dias ativos.
- **XP, níveis e ranks** E → D → C → B → A → S, com LEVEL UP e RANK UP.
- **Atributos** Força, Agilidade, Resistência e Disciplina (gráfico radar).
- **Dungeon (GPS)**: corrida/caminhada com mapa, ritmo, pausa automática, parciais por km e recordes.
- **Histórico** com calendário, registro manual e backup (exportar/importar).

## Estrutura do projeto
| Caminho | O que é |
|---|---|
| `www/index.html` | **O app** (HTML + CSS + JS). Fonte única para o site e para o APK. O balanceamento fica no objeto `CONFIG`. |
| `www/sw.js` | Service worker do site (offline). Não é usado no APK. |
| `www/vendor/`, `www/fonts/` | Leaflet, ponte do Capacitor e fontes Orbitron/Rajdhani locais (geradas por `npm run vendor`). |
| `android/` | Projeto Android nativo (permissões, ícones, splash, tema escuro). |
| `capacitor.config.json` | Nome/ID do app e configuração dos plugins. |
| `package.json` | Versões do Capacitor e dos plugins. |
| `.github/workflows/android.yml` | Compila o APK a cada push e no botão "Run workflow". |
| `scripts/copy-vendor.js` | Copia Leaflet, Capacitor e fontes de `node_modules` para `www/`. |
| `scripts/gen_icons.py` | Gera ícones e splash do Android (só se quiser mudar o visual). |
| `index.html` / `sw.js` (raiz) | Só redirecionam o endereço antigo do site para `www/`. |

## Baixar o APK
1. Aba **Actions** → execução mais recente de **Build APK Android** (ícone verde ✓).
2. Seção **Artifacts** → baixe **SISTEMA-apk-N** (um `.zip`) e extraia o `.apk`.
3. Para gerar de novo sem mudar código: **Actions → Build APK Android → Run workflow**.

## APK de release (opcional)
O APK de **debug** já serve para uso pessoal e sempre instala por cima do anterior
(a chave de debug fica fixa em `android/app/debug.keystore`).
Se quiser um APK **release** assinado com sua própria chave:

```bash
# 1) Gere a chave (precisa de Java; guarde o arquivo e as senhas em lugar seguro)
keytool -genkeypair -v -keystore release.keystore -alias sistema \
  -keyalg RSA -keysize 2048 -validity 10000

# 2) Converta para texto (base64) para colar no GitHub
base64 -w 0 release.keystore > release.keystore.base64     # Linux / Git Bash
```

3. No GitHub: **Settings → Secrets and variables → Actions → New repository secret**, crie:
   - `SISTEMA_KEYSTORE_BASE64` — conteúdo do arquivo `release.keystore.base64`
   - `SISTEMA_KEYSTORE_PASSWORD` — senha da keystore
   - `SISTEMA_KEY_ALIAS` — `sistema`
   - `SISTEMA_KEY_PASSWORD` — senha da chave
4. O próximo build gera também `SISTEMA-...-release.apk`.

Atenção: debug e release têm assinaturas diferentes. Para trocar de um para o outro é preciso
desinstalar o app (exporte o backup antes).

## Rodar localmente (opcional)
```bash
npm install
npm run vendor          # copia Leaflet/fontes/Capacitor para www/
npx cap sync android    # copia www/ para o projeto Android
```
