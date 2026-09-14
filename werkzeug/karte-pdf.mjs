// Rendert die Visitenkarte nach PDF, exakt 85 x 55 mm.
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage();
await p.goto('http://localhost:8899/werkzeug/visitenkarte.html', { waitUntil: 'networkidle' });
await p.waitForTimeout(700);
await p.pdf({ path: 'druck/Visitenkarte-Bazie.pdf', width: '85mm', height: '55mm',
              printBackground: true, margin: { top:'0', right:'0', bottom:'0', left:'0' } });
await b.close();
console.log('PDF geschrieben');
