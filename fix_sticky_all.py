with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ── Header = 68px, Tab-nav ≈ 49px → filters stick at top: 117px ──────────────
STICKY_TOP = '117px'

# ── 1. FIX Overview sticky filter (change top:0 → correct offset) ─────────────
OLD_OV_STICKY = """    /* Sticky main filter bar */
    #tab-overview > .filters-bar {
      position: sticky;
      top: 0;
      z-index: 500;
      backdrop-filter: blur(10px);
      background: rgba(15,23,42,0.95);
      border-radius: 0 0 var(--radius) var(--radius);
      border-top: none;
      margin-bottom: 20px;
    }"""

NEW_OV_STICKY = """    /* ── Sticky filter bars: all tabs ── */
    #tab-overview > .filters-bar,
    #tab-map .filters-bar:first-of-type,
    #tab-quarter .filters-bar {
      position: sticky;
      top: """ + STICKY_TOP + """;
      z-index: 300;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      background: rgba(8,12,24,0.92) !important;
      border: 1px solid rgba(232,0,28,0.15) !important;
      border-radius: var(--radius);
      box-shadow: 0 4px 24px rgba(0,0,0,0.5), 0 1px 0 rgba(232,0,28,0.1);
      margin-bottom: 20px;
    }"""

if OLD_OV_STICKY in html:
    html = html.replace(OLD_OV_STICKY, NEW_OV_STICKY, 1)
    fixes += 1
    print("CSS: Unified sticky filter bar for all 3 tabs")
else:
    print("WARN: old sticky CSS block not found — trying append")
    # Append to </style>
    APPEND = """
    /* ── Sticky filter bars: all tabs ── */
    #tab-overview > .filters-bar,
    #tab-map .filters-bar:first-of-type,
    #tab-quarter .filters-bar {
      position: sticky !important;
      top: """ + STICKY_TOP + """;
      z-index: 300;
      backdrop-filter: blur(14px);
      background: rgba(8,12,24,0.92) !important;
      border: 1px solid rgba(232,0,28,0.15) !important;
      box-shadow: 0 4px 24px rgba(0,0,0,0.5);
      margin-bottom: 20px;
    }"""
    html = html.replace('</style>', APPEND + '\n    </style>', 1)
    fixes += 1
    print("CSS: Sticky appended to </style>")

# ── 2. ENSURE map filter bar has the right class/structure ────────────────────
# Map has: <div class="filters-bar" style="margin-bottom:16px">
# This is already caught by #tab-map .filters-bar:first-of-type ✓

# ── 3. ENSURE quarterly filter bar has the correct class ──────────────────────
# Quarterly has: <div class="filters-bar fade-in" style="margin-bottom:24px;padding:12px 16px">
# This is already caught by #tab-quarter .filters-bar ✓

# ── 4. ADD `padding-top` to the content below each sticky filter
#       so content doesn't jump under it when scrolling ─────────────────────
# Already handled by margin-bottom on .filters-bar

# ── 5. Make the Quarterly tab inner wrapper NOT have overflow:hidden
#       (overflow:hidden on parent breaks position:sticky for children) ────────
# Check if there's an overflow on tab-quarter panel
OV_CHECK = "overflow: hidden"
if OV_CHECK in html:
    count = html.count(OV_CHECK)
    print(f"INFO: {count} overflow:hidden found — check if any wraps tab panels")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nFixes: {fixes} — Done.")
