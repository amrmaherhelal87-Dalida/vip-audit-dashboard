import json
with open('data/vip_data.json', encoding='utf-8') as f:
    data = json.load(f)

# Check for NaN or None in key map fields
issues = []
for r in data:
    problems = []
    if r.get('total_incentive') is None: problems.append('incentive=None')
    if r.get('overall_score') is None:   problems.append('score=None')
    if r.get('outlet_code') is None and r.get('outlet_name') is None: problems.append('no code+name')
    if problems:
        issues.append((r.get('outlet_code', '?'), problems))

print(f'Records with issues: {len(issues)}')
for code, probs in issues[:5]:
    print(f'  {code}: {probs}')

# Check incentive distribution
incentives = [r['total_incentive'] for r in data if r.get('total_incentive') is not None]
nones = sum(1 for r in data if r.get('total_incentive') is None)
print(f'\nIncentive: {len(incentives)} have value, {nones} are None')
print(f'Sample incentive values: {incentives[:5]}')

# Check if r.round values are strings or numbers
rounds = set(type(r['round']).__name__ for r in data[:20])
print(f'\nround field types: {rounds}')
print(f'Sample rounds: {[r["round"] for r in data[:5]]}')
