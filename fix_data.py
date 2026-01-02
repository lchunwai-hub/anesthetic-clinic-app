import json

# Create clean data structure
clean_data = {
    "products": {
        "填充": [
            {
                "id": "voluma_ng",
                "name": "VOLUMA",
                "source": "SINOPHARM",
                "is_genuine": False,
                "price": 820.0,
                "unit": "per 支",
                "date_added": "2026-01-01 09:38"
            },
            {
                "id": "vobella_g",
                "name": "VOBELLA",
                "source": "SINOPHARM",
                "is_genuine": True,
                "price": 820.0,
                "unit": "per 支",
                "date_added": "2026-01-01 12:00"
            }
        ],
        "水光": [
            {
                "id": "hyal_001",
                "name": "Hyaluronic Acid Solution 5ml",
                "source": "Local Supplier",
                "is_genuine": True,
                "price": 120.0,
                "unit": "per bottle",
                "date_added": "2024-01-01 10:30"
            }
        ],
        "溶脂": [
            {
                "id": "lipo_001",
                "name": "Lipodissolve Solution 10ml",
                "source": "Medical Supply Co",
                "is_genuine": False,
                "price": 85.0,
                "unit": "per vial",
                "date_added": "2024-01-01 10:45"
            }
        ]
    },
    "sources": [
        "Medical Supply Co",
        "Pharma Corp",
        "Local Supplier",
        "Global Med",
        "SINOPHARM"
    ],
    "users": {
        "admin": "admin123",
        "partner": "partner123"
    }
}

# Write with UTF-8 encoding without BOM
with open('clinic_data.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=2)

print('✅ clinic_data.json fixed successfully!')
print(f"✅ 填充: {len(clean_data['products']['填充'])} products")
print(f"✅ 水光: {len(clean_data['products']['水光'])} products")
print(f"✅ 溶脂: {len(clean_data['products']['溶脂'])} products")
