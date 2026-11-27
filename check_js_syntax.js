const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function extractJS(html) {
  const scripts = html.match(/<script[^>]*>([\s\S]*?)<\/script>/gi);
  if (!scripts) return '';
  return scripts.map(s => s.replace(/<script[^>]*>/i, '').replace(/<\/script>/i, '')).join('\n');
}

const files = [
  'index.html',
  'posts/capitulo-1-operacao-prato.html',
  'posts/capitulo-2-operacao-prato.html',
  'posts/capitulo-3-operacao-prato.html',
  'posts/capitulo-4-operacao-prato.html',
  'posts/capitulo-5-operacao-prato.html',
  'posts/capitulo-1-continentes-perdidos.html',
  'posts/capitulo-2-continentes-perdidos.html',
  'posts/capitulo-3-continentes-perdidos.html',
];

for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const js = extractJS(html);
  const tempFile = '/tmp/check_' + f.replace(/\//g, '_') + '.js';
  fs.writeFileSync(tempFile, js);
  try {
    execSync('node --check ' + tempFile, { stdio: 'pipe' });
    console.log(f + ': OK');
  } catch (e) {
    console.log(f + ': ERRO');
    console.log(e.stdout?.toString() || e.stderr?.toString() || e.message);
  }
  fs.unlinkSync(tempFile);
}