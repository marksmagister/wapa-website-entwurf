// Rendert die Beitrittserklärung nach PDF. Chromium bettet die Schriften ein.
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage();
await p.goto('http://localhost:8899/werkzeug/beitrittserklaerung.html', { waitUntil: 'networkidle' });
await p.waitForTimeout(700);
await p.pdf({ path: 'assets/dokumente/Wapa-Beitrittserklaerung-2026.pdf',
              format: 'A4', printBackground: true,
              margin: { top: '0', right: '0', bottom: '0', left: '0' } });
await b.close();
console.log('PDF geschrieben');
