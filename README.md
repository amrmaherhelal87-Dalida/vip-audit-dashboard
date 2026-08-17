# 🐂 VIP Audit Dashboard — Red Bull Egypt Q2 2026

A premium dark-mode field audit compliance dashboard for Red Bull Egypt's VIP outlet program.

## 📊 Overview

Tracks **5,820 audit records** across **4 rounds** (April–July 2026) covering:
- **Impulse & Grocery**, **Gas Station**, **Supermarket**, **Bazar** outlets
- Regions: Delta · Cairo · Alexandria · Giza · Canal · Sinai · Red Sea
- KPIs: Availability, Share of Shelf, Strike Zone, Price Communication, POSM, Cooler Placement

## 🚀 Live Dashboard
**[View on Cloudflare Pages →](https://vip-audit-dashboard.pages.dev)**

## ✨ Features
- 🔴 Red Bull dark-mode branding (navy + red + gold)
- 🎯 Real-time filters: Round · Outlet Type · Region
- 📈 6 interactive Chart.js charts
- 📋 Sortable audit records table (200 rows)
- 📱 Responsive layout

## 🛠 Tech Stack
- Pure HTML + CSS + Vanilla JS
- [Chart.js 4.4](https://www.chartjs.org/) via CDN
- [Inter](https://fonts.google.com/specimen/Inter) font
- Data: `data/vip_data.json` (exported from Excel)

## 📁 Structure
```
vip-audit-dashboard/
├── index.html          # Dashboard
├── data/
│   ├── vip_data.json   # 5,820 audit records
│   └── summary.json    # Aggregate stats
└── README.md
```

## 🔄 Data Source
`Q2-2026 NewContract` sheet from `VIP 2026 April to July.xlsx`  
Exported and normalised via `export_data.py`

---
*Red Bull Egypt Field Operations � Q2 2026 � Last deployed: 2026-08-17 12:26*
