import json

# Load the data with proper encoding
with open('clinic_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add new categories
data['products']['肉毒'] = []
data['products']['生髮'] = []

# Write back with proper encoding
with open('clinic_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ Categories added successfully!')
print('All categories:')
for cat in data['products'].keys():
    print(f'  - {cat}')
