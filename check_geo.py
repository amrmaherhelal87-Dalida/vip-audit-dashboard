import json
with open('data/vip_data.json', encoding='utf-8') as f:
    data = json.load(f)

has_geo = [r for r in data if r.get('lat') or r.get('lon')]
no_geo  = [r for r in data if not r.get('lat') and not r.get('lon')]
print(f'Records with geo: {len(has_geo)}/{len(data)}')
print(f'Records without geo: {len(no_geo)}')
for r in has_geo[:5]:
    print(f'  lat={r["lat"]}, lon={r["lon"]}, region={r["region"]}')
