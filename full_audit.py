import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Extract everything between <script> tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
all_js = '\n'.join(scripts)

# Find all getElementById calls
all_refs = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", all_js)

# Deduplicate
unique_refs = sorted(set(all_refs))

print(f'Total unique element IDs referenced in JS: {len(unique_refs)}')
print()

missing = []
for m in unique_refs:
    exists = f'id="{m}"' in html or f"id='{m}'" in html
    status = "OK      " if exists else "MISSING!"
    if not exists:
        missing.append(m)
    print(f'  {status}  #{m}')

print()
print(f'MISSING elements ({len(missing)}): {missing}')
