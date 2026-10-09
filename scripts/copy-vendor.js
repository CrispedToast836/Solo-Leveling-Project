/*
 * Copia as dependências do app (que antes vinham de CDN) para dentro de www/,
 * para o APK funcionar 100% offline:
 *   - Leaflet (mapa)              → www/vendor/leaflet/
 *   - Capacitor (ponte nativa)    → www/vendor/capacitor/capacitor.js
 *   - Fontes Orbitron e Rajdhani  → www/fonts/  (+ www/fonts/fonts.css)
 *
 * Rode com:  npm run vendor   (o workflow do GitHub Actions também roda)
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const nm = p => path.join(root, 'node_modules', p);
const www = p => path.join(root, 'www', p);

function copy(from, to) {
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  console.log('  ✓', path.relative(root, to));
}

console.log('Copiando dependências para www/ ...');

// Leaflet
copy(nm('leaflet/dist/leaflet.js'), www('vendor/leaflet/leaflet.js'));
copy(nm('leaflet/dist/leaflet.css'), www('vendor/leaflet/leaflet.css'));
for (const img of fs.readdirSync(nm('leaflet/dist/images'))) {
  copy(nm(`leaflet/dist/images/${img}`), www(`vendor/leaflet/images/${img}`));
}

// Capacitor (registerPlugin sem bundler)
copy(nm('@capacitor/core/dist/capacitor.js'), www('vendor/capacitor/capacitor.js'));

// Fontes (só o subconjunto latino: cobre português)
const FONTS = [
  ['orbitron', 'Orbitron', [500, 700, 900]],
  ['rajdhani', 'Rajdhani', [500, 600, 700]],
];
let css = '/* Gerado por scripts/copy-vendor.js — fontes locais (sem Google Fonts) */\n';
for (const [pkg, family, weights] of FONTS) {
  for (const w of weights) {
    const file = `${pkg}-latin-${w}-normal.woff2`;
    copy(nm(`@fontsource/${pkg}/files/${file}`), www(`fonts/${file}`));
    css += `@font-face{font-family:'${family}';font-style:normal;font-weight:${w};font-display:swap;src:url('${file}') format('woff2')}\n`;
  }
}
fs.writeFileSync(www('fonts/fonts.css'), css);
console.log('  ✓ www/fonts/fonts.css');
console.log('Pronto.');
