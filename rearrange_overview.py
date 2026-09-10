with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── Current order (lines 1097-1165):
# [KPI cards close </div>]
# Charts Row 1: Compliance Overview (trend, outlet type, region)
# KPI Compliance by Contract Type
#
# ── Target order:
# [KPI cards close </div>]
# KPI Compliance by Contract Type   ← MOVE UP
# Charts Row 1: Compliance Overview

CONTRACT_BLOCK = """

  <!-- KPI Compliance by Contract Type -->
  <div class="section-label" style="margin-top:8px">KPI Compliance by Contract Type</div>
  <div class="chart-card chart-wide fade-in" style="animation-delay:.18s">
    <div class="chart-header">
      <div>
        <div class="chart-title" id="kpi-contract-title">Impulse &amp; Grocery — KPI Compliance</div>
        <div class="chart-subtitle" id="kpi-contract-subtitle">Avg compliance % per KPI for this contract type</div>
      </div>
      <div class="chart-tabs">
        <button class="chart-tab-btn active" data-contract-tab="Impulse &amp; Grocery">Impulse &amp; Grocery</button>
        <button class="chart-tab-btn" data-contract-tab="Supermarket">Supermarket</button>
        <button class="chart-tab-btn" data-contract-tab="Gas Station">Gas Station</button>
        <button class="chart-tab-btn" data-contract-tab="Bazar">Bazar</button>
      </div>
    </div>
    <div class="chart-wrap" style="height:280px"><canvas id="c-kpi-contract"></canvas></div>
    <div style="margin-top:28px;padding-top:20px;border-top:1px solid var(--border)">
      <div class="chart-title" id="kpi-contract-trend-title" style="font-size:14px">Impulse &amp; Grocery — KPI Trend by Month</div>
      <div class="chart-subtitle" id="kpi-contract-trend-subtitle">Compliance % per KPI across rounds (Apr\u2013Jul)</div>
    </div>
    <div class="chart-wrap" style="height:280px"><canvas id="c-kpi-contract-trend"></canvas></div>
  </div>"""

OVERVIEW_BLOCK = """

  <!-- Charts Row 1 -->
  <div class="section-label" style="margin-top:16px">Compliance Overview</div>"""

# Step 1: Find and remove CONTRACT_BLOCK from current location
# (it sits between the charts grid close and KPI Deep Dive)
MARKER_BEFORE = "\n\n\n  <!-- KPI Compliance by Contract Type -->"
MARKER_AFTER  = "\n\n  <!-- Charts Row 2 -->"

old_contract = html[html.find(MARKER_BEFORE):html.find(MARKER_AFTER)]
if old_contract:
    html = html.replace(old_contract, "", 1)
    print("Step 1: Contract block removed from old location")
else:
    print("WARN: Contract block marker not found at old location")

# Step 2: Insert CONTRACT_BLOCK right after KPI cards (after the closing </div> of kpi-grid)
KPI_GRID_END = "  </div>\n\n  <!-- Charts Row 1 -->"
REPLACEMENT  = "  </div>" + CONTRACT_BLOCK + OVERVIEW_BLOCK

if KPI_GRID_END in html:
    html = html.replace(KPI_GRID_END, REPLACEMENT, 1)
    print("Step 2: Contract block inserted after KPI cards")
else:
    print("WARN: KPI grid end marker not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify order
with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()

markers = {}
for i, l in enumerate(lines, 1):
    if 'Key Performance Indicators' in l: markers['1.KPI Cards'] = i
    if 'KPI Compliance by Contract Type' in l and 'section-label' in l: markers['2.Contract Type'] = i
    if 'Compliance Overview' in l and 'section-label' in l: markers['3.Compliance Overview'] = i
    if 'Outlet Detail' in l and 'section-label' in l: markers['4.Outlet Detail'] = i

print("\nFinal section order:")
for k,v in sorted(markers.items(), key=lambda x: x[1]):
    print(f"  Line {v}: {k}")
print(f"\nTotal lines: {len(lines)}")
