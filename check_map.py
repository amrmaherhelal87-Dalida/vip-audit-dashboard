import json
with open('data/vip_data.json', encoding='utf-8') as f:
    data = json.load(f)

# Simulate applyMapFilters with default 'all' settings
filtered = [r for r in data if r.get('lat') and r.get('lon')]
print(f'After lat/lon filter: {len(filtered)}')

EG = dict(latMin=22, latMax=31.65, lonMin=24.7, lonMax=37.0)
def inEgypt(lat, lon):
    return EG['latMin']<=lat<=EG['latMax'] and EG['lonMin']<=lon<=EG['lonMax']

def resolveCoords(r):
    try:
        px = float(r['lat'])
        py = float(r['lon'])
    except:
        return None
    latStd, lonStd = py, px
    latSwp, lonSwp = px, py
    stdOk = inEgypt(latStd, lonStd)
    swpOk = inEgypt(latSwp, lonSwp)
    if stdOk and not swpOk: return [latStd, lonStd]
    if swpOk and not stdOk: return [latSwp, lonSwp]
    if stdOk and swpOk: return [latStd, lonStd]
    return None

resolved = 0; failed = 0
fail_samples = []
for r in filtered:
    c = resolveCoords(r)
    if c:
        resolved += 1
    else:
        failed += 1
        if len(fail_samples) < 3:
            fail_samples.append(r)

print(f'Resolved OK: {resolved}')
print(f'Failed (neither convention): {failed}')
for r in fail_samples:
    print(f'  FAILED: lat={r["lat"]}, lon={r["lon"]}, region={r["region"]}')

# Outlet groups
groups = {}
for r in filtered:
    k = str(r.get('outlet_code') or r.get('outlet_name') or 'unknown')
    if k not in groups: groups[k] = []
    groups[k].append(r)

markers = 0
for recs in groups.values():
    recs.sort(key=lambda x: x.get('round') or 0)
    for r in recs:
        c = resolveCoords(r)
        if c:
            markers += 1
            break

print(f'Total outlet groups: {len(groups)}')
print(f'Groups that would get a marker: {markers}')
