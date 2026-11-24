const fs = require('fs');
const d = JSON.parse(fs.readFileSync('C:/Users/erico/zambria.github.io/logs/caixa-erros/memoria-compartilhada.json', 'utf8'));
const last = d.aprendizados[d.aprendizados.length - 1];
console.log('JSON VALIDO. aprendizados:', d.aprendizados.length);
console.log('Última entrada:', last.erro, '|', last.data);
console.log('Arquivos na entrada:', last.arquivos.length);
