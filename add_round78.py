with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Add Round 78 (March) before Round 79 in overview filter
OLD79_OV = 'value="79" onchange="msOptChange(\'ms-round\')"> Round 79 \u2014 April</label>'
NEW78_OV = 'value="78" onchange="msOptChange(\'ms-round\')"> Round 78 \u2014 March</label>\n          <label class="ms-opt"><input type="checkbox" ' + OLD79_OV

if OLD79_OV in html:
    html = html.replace(OLD79_OV, NEW78_OV, 1)
    print('Round 78 added to overview filter')
else:
    print('WARN: overview filter R79 not found')

# Add Round 78 (March) before Round 79 in map filter
OLD79_MAP = 'value="79" onchange="msOptChange(\'ms-m-round\')"> Round 79 \u2014 April</label>'
NEW78_MAP = 'value="78" onchange="msOptChange(\'ms-m-round\')"> Round 78 \u2014 March</label>\n          <label class="ms-opt"><input type="checkbox" ' + OLD79_MAP

if OLD79_MAP in html:
    html = html.replace(OLD79_MAP, NEW78_MAP, 1)
    print('Round 78 added to map filter')
else:
    print('WARN: map filter R79 not found')

# Update subtitles
html = html.replace('April \u2192 July', 'March \u2192 August')
html = html.replace('Apr\u2013Jul', 'Mar\u2013Aug')
html = html.replace('April \u2014 July', 'March \u2014 August')
print('Subtitles updated')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Round 78 in html: {"Round 78" in html}')
print(f'Lines: {len(html.splitlines())}')
