
function createBreakdown(values,score) {
  // Badge styling
  const badge = document.getElementById('scoreBadge');
  badge.style.background = `linear-gradient(180deg, ${colorForScore(score)}, rgba(0,0,0,0.06))`;
  badge.style.color = '#071123';
  badge.textContent = score + '%';
    
  // Breakdown
  const breakdown = document.getElementById('breakdownList');
  breakdown.innerHTML = ""
    
  metrics.forEach((m,i)=>{
    const val = values[i];
    const row = document.createElement('div');
    row.className = 'flex items-center gap-3';
    row.innerHTML = `
      <div class="w-28 text-sm text-base-content/80">${m.label}</div>
      <div class="flex-1 bg-base-200/10 rounded-full h-2 overflow-hidden">
        <div style="width:${val}%;height:100%;background:linear-gradient(90deg, ${colorForScore(val)}, rgba(255,255,255,0.06));"></div>
      </div>
      <div class="w-10 text-right text-sm text-base-content/70">${val}</div>
    `;
    breakdown.appendChild(row);
  });
    
  document.getElementById('refreshBtn').addEventListener('click', ()=> location.reload()); 
}
