import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Extract init() function body
start = html.find('async function init()')
end   = html.find('\ninit();', start)
init_body = html[start:end]

matches = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", init_body)
print('Elements referenced inside init():')
for m in set(matches):
    print(f'  #{m}')

# Also check render() calls inside init
print()
print('Checking if these IDs exist in HTML:')
for m in set(matches):
    exists = f'id="{m}"' in html or f"id='{m}'" in html
    status = "OK" if exists else "MISSING!"
    print(f'  #{m}: {status}')
