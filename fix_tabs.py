with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# Fix 1: contract tab click handler
OLD1 = "buildKPIContractChart(getFilteredData ? getFilteredData() : ALL_DATA);"
NEW1 = "buildKPIContractChart(applyFilters(ALL_DATA));"
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    fixes += 1
    print("Fixed contract tab click handler")
else:
    print("WARN: contract tab handler not found")

# Fix 2: Quarter tab click if it uses getFilteredData
if "getFilteredData()" in html:
    count = html.count("getFilteredData()")
    html = html.replace("getFilteredData()", "applyFilters(ALL_DATA)")
    fixes += count
    print(f"Fixed {count} more getFilteredData() call(s)")

# Fix 3: outlet search uses getFilteredData too (from apply_changes.py)
# Already covered above if present

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes applied: {fixes}")
print("Done.")
