with open('index.html', encoding='utf-8') as f:
    html = f.read()

OLD = """function buildOutletChart(data) {
  destroyChart('c-outlet');
  const types = ['Impulse & Grocery','Supermarket','Gas Station','Bazar'];
  const avgs = types.map(t => {
    const sub = data.filter(r=>r.outlet_type===t);
    return +(avgScore(sub)*100).toFixed(1);
  });
  charts['c-outlet'] = new Chart(ctx('c-outlet'), {
    type: 'bar',
    data: {
      labels: types,
      datasets:[{
        data: avgs,
        backgroundColor: types.map(t => OUTLET_COLORS[t] + '99'),
        borderColor: types.map(t => OUTLET_COLORS[t]),
        borderWidth: 2, borderRadius: 8,
      }]
    },
    options: {
      ...CHART_OPT,
      indexAxis: 'y',
      scales: {
        x: { min:0, max:100, grid:{color:'rgba(255,255,255,0.05)'}, ticks:{callback:v=>v+'%'} },
        y: { grid:{display:false} }
      },
      plugins: {
        legend:{display:false},
        tooltip:{callbacks:{label: ctx => ` ${ctx.parsed.x.toFixed(1)}% avg compliance`}}
      }
    }
  });
}"""

NEW = """function buildOutletChart(data) {
  destroyChart('c-outlet');

  const TYPES = ['Impulse & Grocery','Supermarket','Gas Station','Bazar'];
  const MONTH_ORDER = ['April','May','June','July','August','September','October','November','December','January','February','March'];
  const typeColors = {
    'Impulse & Grocery': RED,
    'Supermarket':       GOLD,
    'Gas Station':       BLUE,
    'Bazar':             PURPLE,
  };

  // Months present in data, in calendar order
  const presentMonths = new Set(data.map(r => r.month).filter(Boolean));
  const months = MONTH_ORDER.filter(m => presentMonths.has(m));

  // One dataset per outlet type
  const datasets = TYPES.map(t => {
    const color = typeColors[t] || '#94a3b8';
    return {
      label: t,
      data: months.map(m => {
        const sub = data.filter(r => r.outlet_type === t && r.month === m);
        return sub.length ? +(avgScore(sub)*100).toFixed(1) : null;
      }),
      backgroundColor: color + 'aa',
      borderColor: color,
      borderWidth: 2, borderRadius: 6,
      datalabels: {
        display: true, anchor:'end', align:'top',
        color:'#cbd5e1', font:{size:9, weight:'600'},
        formatter: v => v != null ? v+'%' : ''
      }
    };
  });

  // Overall total per month
  datasets.push({
    label: 'Overall',
    data: months.map(m => {
      const sub = data.filter(r => r.month === m);
      return sub.length ? +(avgScore(sub)*100).toFixed(1) : null;
    }),
    backgroundColor: 'rgba(255,255,255,0.15)',
    borderColor: '#ffffff',
    borderWidth: 2, borderRadius: 6,
    datalabels: {
      display: true, anchor:'end', align:'top',
      color:'#ffffff', font:{size:9, weight:'700'},
      formatter: v => v != null ? v+'%' : ''
    }
  });

  charts['c-outlet'] = new Chart(ctx('c-outlet'), {
    type: 'bar',
    data: { labels: months, datasets },
    options: {
      ...CHART_OPT,
      scales: {
        x: { grid:{color:'rgba(255,255,255,0.05)'}, ticks:{color:'#94a3b8'} },
        y: {
          min:0, max:100,
          grid:{color:'rgba(255,255,255,0.05)'},
          ticks:{color:'#94a3b8', callback:v=>v+'%'}
        }
      },
      plugins: {
        legend:{
          display: true,
          labels:{ color:'#94a3b8', boxWidth:12, padding:14, font:{size:11} }
        },
        tooltip:{
          callbacks:{
            label: c => ' ' + c.dataset.label + ': ' + (c.parsed.y != null ? c.parsed.y.toFixed(1)+'%' : 'N/A')
          }
        }
      }
    }
  });
}"""

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print("OK: buildOutletChart replaced")
else:
    print("WARN: old function not found exactly — searching loosely")
    import re
    m = re.search(r'function buildOutletChart\(data\) \{.*?\n\}', html, re.DOTALL)
    if m:
        html = html[:m.start()] + NEW + html[m.end():]
        print("OK: replaced via regex")
    else:
        print("ERROR: not found")

# Also update chart subtitle in HTML
html = html.replace(
    '<div class="chart-subtitle">Average score per channel</div>',
    '<div class="chart-subtitle">Monthly compliance % per outlet type + overall total</div>'
)
print("OK: chart subtitle updated")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done. Lines: {len(html.splitlines())}")
