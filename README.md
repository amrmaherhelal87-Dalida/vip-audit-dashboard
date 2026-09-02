# ðŸ‚ VIP Audit Dashboard â€” Red Bull Egypt Q2 2026

A premium dark-mode field audit compliance dashboard for Red Bull Egypt's VIP outlet program.

## ðŸ“Š Overview

Tracks **5,820 audit records** across **4 rounds** (Aprilâ€“July 2026) covering:
- **Impulse & Grocery**, **Gas Station**, **Supermarket**, **Bazar** outlets
- Regions: Delta Â· Cairo Â· Alexandria Â· Giza Â· Canal Â· Sinai Â· Red Sea
- KPIs: Availability, Share of Shelf, Strike Zone, Price Communication, POSM, Cooler Placement

## ðŸš€ Live Dashboard
**[View on Cloudflare Pages â†’](https://amrmaherhelal87-dalida.github.io/vip-audit-dashboard/)**

## âœ¨ Features
- ðŸ”´ Red Bull dark-mode branding (navy + red + gold)
- ðŸŽ¯ Real-time filters: Round Â· Outlet Type Â· Region
- ðŸ“ˆ 6 interactive Chart.js charts
- ðŸ“‹ Sortable audit records table (200 rows)
- ðŸ“± Responsive layout

## ðŸ›  Tech Stack
- Pure HTML + CSS + Vanilla JS
- [Chart.js 4.4](https://www.chartjs.org/) via CDN
- [Inter](https://fonts.google.com/specimen/Inter) font
- Data: `data/vip_data.json` (exported from Excel)

## ðŸ“ Structure
```
vip-audit-dashboard/
â”œâ”€â”€ index.html          # Dashboard
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ vip_data.json   # 5,820 audit records
â”‚   â””â”€â”€ summary.json    # Aggregate stats
â””â”€â”€ README.md
```

## ðŸ”„ Data Source
`Q2-2026 NewContract` sheet from `VIP 2026 April to July.xlsx`  
Exported and normalised via `export_data.py`

---
*Red Bull Egypt Field Operations · Q2 2026 · Last deployed: 2026-08-17 12:26*

