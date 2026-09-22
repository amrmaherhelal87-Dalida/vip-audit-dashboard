
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);

if (!scriptMatch) { console.log('No scripts found'); process.exit(1); }

let errs = 0;
scriptMatch.forEach((block, i) => {
  const code = block.replace(/<script[^>]*>/, '').replace(/<\/script>/, '');
  if (!code.trim()) return;
  try {
    new Function(code);
    console.log(`Script ${i+1}: OK (${code.length} chars)`);
  } catch(e) {
    console.error(`Script ${i+1}: ERROR — ${e.message}`);
    // Show where the error is
    const lines = code.split('\n');
    const m = e.message.match(/line (\d+)/);
    if (m) {
      const ln = parseInt(m[1]);
      for (let j = Math.max(0,ln-3); j<Math.min(lines.length,ln+3); j++) {
        console.error(`  ${j+1}: ${lines[j]}`);
      }
    }
    errs++;
  }
});
console.log(`\nTotal errors: ${errs}`);
