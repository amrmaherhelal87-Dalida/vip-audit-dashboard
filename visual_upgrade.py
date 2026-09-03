with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════════════
# COMPREHENSIVE VISUAL UPGRADE — inject before </style>
# ══════════════════════════════════════════════════════════════════

UPGRADE_CSS = """
    /* ════════════════════════════════════════════════════
       VISUAL UPGRADE — Premium Red Bull Dashboard Theme
    ════════════════════════════════════════════════════ */

    /* 1. Background: dot grid + ambient red glow ─────────────── */
    body {
      background-color: var(--bg);
      background-image:
        radial-gradient(ellipse 60% 40% at 8% 0%, rgba(232,0,28,0.10) 0%, transparent 70%),
        radial-gradient(circle at 92% 90%, rgba(59,130,246,0.05) 0%, transparent 50%),
        radial-gradient(rgba(255,255,255,0.025) 1px, transparent 1px);
      background-size: auto, auto, 28px 28px;
    }

    /* 2. Header — glowing red bottom border ─────────────────── */
    header {
      background: linear-gradient(135deg, #060a16 0%, #0e0018 50%, #060a16 100%) !important;
      border-bottom: 1px solid rgba(232,0,28,0.5) !important;
      box-shadow: 0 1px 0 0 rgba(232,0,28,0.15), 0 4px 24px rgba(0,0,0,0.6) !important;
    }

    /* 3. Nav tabs — sliding red underline indicator ─────────── */
    .tab-nav {
      background: rgba(8,12,24,0.7);
      border-bottom: 1px solid rgba(255,255,255,0.06);
      backdrop-filter: blur(12px);
      padding: 0 32px;
      display: flex;
      gap: 4px;
      position: sticky;
      top: 68px;
      z-index: 400;
    }
    .tab-btn {
      position: relative;
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 14px 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: color .2s;
      border-radius: 0;
      letter-spacing: .3px;
    }
    .tab-btn::after {
      content: '';
      position: absolute;
      bottom: -1px; left: 50%; right: 50%;
      height: 2px;
      background: var(--red);
      box-shadow: 0 0 8px var(--red-glow);
      transition: left .25s, right .25s;
      border-radius: 2px 2px 0 0;
    }
    .tab-btn.active { color: #fff; }
    .tab-btn.active::after { left: 12px; right: 12px; }
    .tab-btn:hover { color: #e2e8f0; }
    .tab-icon { margin-right: 6px; }

    /* 4. KPI Cards — gradient body + colored glow on hover ──── */
    .kpi-card {
      background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
      border: 1px solid rgba(255,255,255,0.07);
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      transition: transform .25s, box-shadow .25s;
    }
    .kpi-card::before { height: 2px !important; }
    .kpi-card:hover { transform: translateY(-4px); }
    .kpi-card.red:hover   { box-shadow: 0 12px 40px rgba(232,0,28,0.25), 0 4px 20px rgba(0,0,0,0.4); }
    .kpi-card.gold:hover  { box-shadow: 0 12px 40px rgba(245,197,24,0.2), 0 4px 20px rgba(0,0,0,0.4); }
    .kpi-card.blue:hover  { box-shadow: 0 12px 40px rgba(59,130,246,0.2), 0 4px 20px rgba(0,0,0,0.4); }
    .kpi-card.green:hover { box-shadow: 0 12px 40px rgba(16,185,129,0.2), 0 4px 20px rgba(0,0,0,0.4); }
    .kpi-icon { width: 44px !important; height: 44px !important; border-radius: 12px !important; font-size: 20px !important; }
    .kpi-value { font-size: 34px !important; }
    .kpi-card.red   .kpi-icon { background: rgba(232,0,28,.18); box-shadow: 0 0 16px rgba(232,0,28,.15); }
    .kpi-card.gold  .kpi-icon { background: rgba(245,197,24,.18); box-shadow: 0 0 16px rgba(245,197,24,.12); }
    .kpi-card.blue  .kpi-icon { background: rgba(59,130,246,.18); box-shadow: 0 0 16px rgba(59,130,246,.12); }
    .kpi-card.green .kpi-icon { background: rgba(16,185,129,.18); box-shadow: 0 0 16px rgba(16,185,129,.12); }

    /* 5. Chart Cards — glass morphism ───────────────────────── */
    .chart-card {
      background: linear-gradient(135deg, rgba(17,24,39,0.95) 0%, rgba(26,34,56,0.9) 100%);
      border: 1px solid rgba(255,255,255,0.08);
      box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
      backdrop-filter: blur(4px);
      transition: box-shadow .25s;
    }
    .chart-card:hover {
      box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07), 0 0 0 1px rgba(232,0,28,0.12);
    }
    .chart-title { font-size: 15px !important; font-weight: 700 !important; }
    .chart-subtitle { color: var(--muted); font-size: 12px; margin-top: 3px; }

    /* 6. Section Labels — red left bar + gradient text ──────── */
    .section-label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      background: linear-gradient(90deg, var(--red) 0%, #f59e0b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      padding-left: 14px;
      border-left: 3px solid var(--red);
      box-shadow: none;
      margin-bottom: 16px;
    }
    .section-label::after { display: none; }

    /* 7. Chart Tab Buttons — pill active state ───────────────── */
    .chart-tab-btn {
      padding: 6px 16px;
      border-radius: 20px;
      border: 1px solid rgba(255,255,255,0.1);
      background: transparent;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all .2s;
    }
    .chart-tab-btn:hover { color: #e2e8f0; border-color: rgba(255,255,255,0.2); }
    .chart-tab-btn.active {
      background: var(--red);
      border-color: var(--red);
      color: #fff;
      box-shadow: 0 4px 12px rgba(232,0,28,0.35);
    }

    /* 8. Filter Bar — frosted glass upgrade ─────────────────── */
    .filters-bar {
      background: rgba(17,24,39,0.85) !important;
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.08) !important;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .ms-display, .filters-bar select {
      background: rgba(26,34,56,0.8) !important;
      transition: border-color .2s, box-shadow .2s !important;
    }
    .ms-display:hover, .filters-bar select:focus {
      border-color: rgba(232,0,28,0.5) !important;
      box-shadow: 0 0 0 3px rgba(232,0,28,0.08);
    }

    /* 9. Table Card improvements ────────────────────────────── */
    .table-card {
      background: linear-gradient(135deg, rgba(17,24,39,0.95) 0%, rgba(26,34,56,0.9) 100%);
      border: 1px solid rgba(255,255,255,0.07);
      box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    #data-table thead th {
      background: rgba(232,0,28,0.08);
      border-bottom: 1px solid rgba(232,0,28,0.2);
      color: #e2e8f0;
      font-size: 11px;
      letter-spacing: .6px;
      text-transform: uppercase;
    }
    #data-table tbody tr {
      transition: background .15s;
      border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    #data-table tbody tr:hover { background: rgba(232,0,28,0.05); }
    #data-table tbody tr:nth-child(even) { background: rgba(255,255,255,0.02); }
    #data-table tbody tr:nth-child(even):hover { background: rgba(232,0,28,0.05); }

    /* 10. Reset Button ──────────────────────────────────────── */
    #btn-reset {
      background: transparent;
      border: 1px solid rgba(232,0,28,0.3);
      color: var(--red);
      padding: 8px 16px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all .2s;
    }
    #btn-reset:hover {
      background: rgba(232,0,28,0.1);
      border-color: var(--red);
      box-shadow: 0 0 12px rgba(232,0,28,0.2);
    }

    /* 11. Fade-in animation enhancement ─────────────────────── */
    @keyframes fadeUp {
      from { opacity:0; transform: translateY(16px); }
      to   { opacity:1; transform: translateY(0); }
    }
    .fade-in { animation: fadeUp .45s ease both; }

    /* 12. Scrollbar styling ─────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg2); }
    ::-webkit-scrollbar-thumb { background: rgba(232,0,28,0.4); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--red); }

    /* 13. Map search + outlet search input glow ─────────────── */
    #m-search, #outlet-search {
      transition: border-color .2s, box-shadow .2s;
    }
    #m-search:focus, #outlet-search:focus {
      border-color: rgba(232,0,28,0.5) !important;
      box-shadow: 0 0 0 3px rgba(232,0,28,0.08);
      outline: none;
    }

    /* 14. Badge enhancements ────────────────────────────────── */
    .badge-red  { box-shadow: 0 0 10px rgba(232,0,28,0.2); }
    .badge-gold { box-shadow: 0 0 10px rgba(245,197,24,0.15); }
"""

# Inject before </style>
if UPGRADE_CSS not in html:
    html = html.replace('</style>', UPGRADE_CSS + '\n    </style>', 1)
    print("CSS upgrade injected")
else:
    print("Already injected")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done.")
