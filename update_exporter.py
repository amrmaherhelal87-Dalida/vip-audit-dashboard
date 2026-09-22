with open('export_data.py', encoding='utf-8') as f:
    s = f.read()

s = s.replace("r'VIP 2026 April to August.xlsx'", "r'YTD VIP.xlsx'")
s = s.replace("ws = wb['VIP 26']", "ws = wb['YTD VIP 2026']")

with open('export_data.py', 'w', encoding='utf-8') as f:
    f.write(s)
print('Done')
