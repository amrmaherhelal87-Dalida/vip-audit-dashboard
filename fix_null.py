with open('index.html', encoding='utf-8') as f:
    html = f.read()

OLD = "    document.getElementById('last-updated').textContent =\n      'Updated: ' + new Date().toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'});\n    document.getElementById('footer-date').textContent = new Date().getFullYear();"

NEW = "    const luEl = document.getElementById('last-updated');\n    if (luEl) luEl.textContent = 'Updated: ' + new Date().toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'});\n    const fdEl = document.getElementById('footer-date');\n    if (fdEl) fdEl.textContent = new Date().getFullYear();"

if OLD in html:
    html = html.replace(OLD, NEW)
    print("Fixed: footer-date null reference")
else:
    print("ERROR: target string not found - checking actual bytes...")
    idx = html.find("footer-date")
    print(f"footer-date found at index: {idx}")
    print(repr(html[idx-100:idx+100]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
