import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. ADD popup CSS for multi-round side-by-side layout
# ══════════════════════════════════════════════════════════════════
POPUP_CSS = """
    /* ── Multi-round popup ── */
    .popup-rounds-grid {
      display: flex; gap: 8px; margin-top: 8px;
      overflow-x: auto; max-width: 540px;
      padding-bottom: 4px;
    }
    .popup-round-card {
      min-width: 118px; flex-shrink: 0;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 10px; padding: 8px 10px;
      display: flex; flex-direction: column; gap: 3px;
    }
    .popup-round-label {
      font-size: 10px; font-weight: 700; color: #f5c518;
      text-transform: uppercase; letter-spacing:.5px; margin-bottom: 3px;
    }
    .popup-round-score {
      font-size: 20px; font-weight: 800; line-height: 1; margin-bottom: 4px;
    }
    .popup-round-kpi {
      font-size: 10px; display: flex; justify-content: space-between;
      gap: 4px; color: #94a3b8;
    }
    .popup-round-kpi strong { font-weight: 600; }
    .popup-round-inc {
      margin-top: 5px; font-size: 11px; font-weight: 700; color: #f5c518;
      border-top: 1px solid rgba(255,255,255,0.08); padding-top: 5px;
    }
    .leaflet-popup-content { max-width: 560px !important; }
    .leaflet-popup-content-wrapper { max-width: 580px !important; }
"""
html = html.replace('</style>', POPUP_CSS + '\n    </style>', 1)
fixes += 1
print("CSS: Multi-round popup styles added")

# ══════════════════════════════════════════════════════════════════
# 2. REPLACE old marker forEach with grouped-by-outlet version
#    Strategy: replace from "  data.forEach(r => {" through the
#    closing line that ends with ".bindPopup(popup,..." + "  });"
#    but KEEP the "  markerCluster.addLayers(batch);" line intact.
# ══════════════════════════════════════════════════════════════════

# Locate the old per-record forEach block
LOOP_START = "  data.forEach(r => {\n    const coords = resolveCoords(r);"
LOOP_END   = "    batch.push(L.marker([lat,lon],{icon:makeCircle(color,radius)}).bindPopup(popup,{maxWidth:260,closeButton:false}));\n  });"

idx_s = html.find(LOOP_START)
idx_e = html.find(LOOP_END)

if idx_s == -1:
    print("WARN: Loop start not found")
elif idx_e == -1:
    print("WARN: Loop end not found")
else:
    end_pos = idx_e + len(LOOP_END)  # include the closing })

    NEW_LOOP = """  // ── GROUP by outlet_code: ONE pin per outlet ─────────────────────
  const outletGroups = {};
  data.forEach(r => {
    const key = String(r.outlet_code || r.outlet_name || 'unknown');
    if (!outletGroups[key]) outletGroups[key] = [];
    outletGroups[key].push(r);
  });

  const POPUP_KPIS = {
    'Impulse & Grocery': [
      {l:'Avail',k:'avail_compliance'},{l:'SoS',k:'sos_compliance'},
      {l:'Strike',k:'sz_compliance'},{l:'L.Cooler',k:'large_cooler_compliance'},
    ],
    'Supermarket': [
      {l:'Avail',k:'avail_compliance'},{l:'SoS',k:'sos_compliance'},
      {l:'Strike',k:'sz_compliance'},{l:'Price',k:'price_compliance'},
      {l:'Ambient',k:'ambient_compliance'},{l:'Cooler',k:'cooler_cashier_compliance'},
    ],
    'Gas Station': [
      {l:'Avail',k:'avail_compliance'},{l:'SoS',k:'sos_compliance'},
      {l:'Strike',k:'sz_compliance'},{l:'Price',k:'price_compliance'},
      {l:'Sticky',k:'sticky_compliance'},{l:'Chilled',k:'chilled_cashier_compliance'},
      {l:'Brand',k:'posm_compliance'},
    ],
    'Bazar': [
      {l:'Avail',k:'avail_compliance'},{l:'Outdoor',k:'outdoor_compliance'},
      {l:'Price',k:'price_compliance'},{l:'Cooler',k:'cooler_visible_compliance'},
    ],
  };

  Object.values(outletGroups).forEach(records => {
    records.sort((a,b) => (a.round||0)-(b.round||0));
    let coords = null;
    for (const r of records) { coords = resolveCoords(r); if (coords) break; }
    if (!coords) return;
    const [lat, lon] = coords;

    const latest  = records[records.length-1];
    const avgScore= records.reduce((s,r)=>s+(r.overall_score||0),0)/records.length;
    const incentive = latest.total_incentive||0;
    const radius  = Math.max(5, Math.min(14, 5 + incentive*0.28));

    let color;
    if (f.colorBy==='type')       color = TYPE_COLORS[latest.outlet_type] || '#94a3b8';
    else if (f.colorBy==='score') color = scoreColor(avgScore);
    else                          color = incentiveColor(incentive);

    const typeColor = TYPE_COLORS[latest.outlet_type] || '#94a3b8';
    const kpiDefs  = POPUP_KPIS[latest.outlet_type] || POPUP_KPIS['Impulse & Grocery'];

    const roundCards = records.map(r => {
      const sc    = (r.overall_score||0);
      const scPct = (sc*100).toFixed(0)+'%';
      const scCl  = scoreColor(sc);
      const chips = kpiDefs.map(k => {
        const v  = r[k.k];
        const cl = v===1?'#10b981':v===0?'#e8001c':'#64748b';
        const ic = v===1?'\\u2713':v===0?'\\u2717':'\\u2014';
        return '<div class="popup-round-kpi"><span>'+k.l+'</span><strong style="color:'+cl+'">'+ic+'</strong></div>';
      }).join('');
      const inc = typeof r.total_incentive==='number'?r.total_incentive.toFixed(1)+' EGP':'\\u2014';
      return '<div class="popup-round-card">'
        +'<div class="popup-round-label">R'+r.round+' \u00b7 '+(r.month||'').slice(0,3)+'</div>'
        +'<div class="popup-round-score" style="color:'+scCl+'">'+scPct+'</div>'
        +chips
        +'<div class="popup-round-inc">\\ud83d\\udcb0 '+inc+'</div>'
        +'</div>';
    }).join('');

    const nameHtml = latest.outlet_name
      ? '<div style="color:#94a3b8;font-size:11px;margin:-4px 0 6px;max-width:480px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="'+latest.outlet_name+'">'+latest.outlet_name+'</div>'
      : '';
    const popup =
      '<div class="popup-title">'+(latest.outlet_code||'\\u2014')+'</div>'
      + nameHtml
      + '<div class="popup-row"><span>Type</span><strong><span style="color:'+typeColor+'">\\u25cf</span> '+latest.outlet_type+'</strong></div>'
      + '<div class="popup-row"><span>Region</span><strong>'+(latest.region||'\\u2014')+'</strong></div>'
      + '<div class="popup-row"><span>Governorate</span><strong>'+(latest.governorate||'\\u2014')+'</strong></div>'
      + '<div class="popup-row"><span>Avg Score</span><strong style="color:'+scoreColor(avgScore)+'">'+(avgScore*100).toFixed(1)+'%</strong></div>'
      + '<div class="popup-rounds-grid">'+roundCards+'</div>';

    batch.push(L.marker([lat,lon],{icon:makeCircle(color,radius)}).bindPopup(popup,{maxWidth:560,className:'dark-popup',closeButton:false}));
  });"""

    html = html[:idx_s] + NEW_LOOP + html[end_pos:]
    fixes += 1
    print("JS: Marker loop replaced with outlet-grouped version")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
with open('index.html', encoding='utf-8') as f:
    out = f.read()
lines = out.splitlines()
print(f"File: {len(lines)} lines")
for kw in ['markerCluster.addLayers','popup-rounds-grid','outletGroups','</script>','</html>']:
    status = 'OK' if kw in out else 'MISSING'
    print(f"  {kw}: {status}")

print(f"\nTotal fixes: {fixes} -- Done.")
