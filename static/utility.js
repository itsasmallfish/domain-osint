const metrics = [
  { key: 'ssl', label: 'SSL/TLS' },
  { key: 'dns', label: 'DNS' },
  { key: 'surface', label: 'Surface' },
  { key: 'rep', label: 'Reputation' },
  { key: 'exposure', label: 'Exposure' }
];

function colorForScore(s){
  const p = Math.max(0, Math.min(1, s/100));
  const h = (1 - p) * 120; // green (120) -> red (0)
  return `hsl(${h}deg 85% 55%)`;
}

const clamp = v => Math.max(0, Math.min(100, Number(v) || 0));

