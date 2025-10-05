#!/usr/bin/env python3
"""
Field Analysis Script - Extract all fields from models, schemas, and seed data
"""

import re
import os

def extract_model_fields(file_path, class_name):
    """Extract Column fields from SQLAlchemy model files."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find column definitions
        column_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*Column\('
        matches = re.findall(column_pattern, content, re.MULTILINE)
        
        # Get table name
        table_pattern = r'__tablename__\s*=\s*["\']([^"\']+)["\']'
        table_match = re.search(table_pattern, content)
        table_name = table_match.group(1) if table_match else 'unknown'
        
        return {
            'table_name': table_name,
            'fields': matches
        }
    except Exception as e:
        return {'table_name': 'error', 'fields': [f'Error: {e}']}

def extract_schema_fields(file_path):
    """Extract field definitions from Pydantic schema files."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find field definitions in Pydantic models
        field_patterns = [
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*[^=]+\s*=\s*Field\(',
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*[^=]+(?:\s*=\s*[^=\n]+)?$'
        ]
        
        fields = []
        for pattern in field_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            fields.extend(matches)
        
        # Remove duplicates and common non-field items
        excluded = {'Config', 'class', 'model_config'}
        fields = list(set(f for f in fields if f not in excluded))
        
        return sorted(fields)
    except Exception as e:
        return [f'Error: {e}']

def extract_seed_data_fields(file_path):
    """Extract field names used in seed data."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find dictionary keys in seed data (common pattern: "key": value)
        field_pattern = r'["\']([\w_]+)["\']\s*:'
        matches = re.findall(field_pattern, content)
        
        return sorted(list(set(matches)))
    except Exception as e:
        return [f'Error: {e}']

# Model files to analyze
models = {
    'User': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/user.py',
    'Sport': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/sport.py',
    'Team': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/team.py',
    'Player': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/player.py',
    'Competition': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/competition.py',
    'Season': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/season.py',
    'Match': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/match.py',
    'Bet': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/bet.py',
    'Result': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/result.py',
    'Group': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/group.py',
    'GroupMembership': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/group_membership.py',
    'AuditLog': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/models/audit_log.py'
}

# Schema files to analyze
schemas = {
    'User': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/user.py',
    'Sport': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/sport.py',
    'Team': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/team.py',
    'Player': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/player.py',
    'Competition': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/competition.py',
    'Season': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/season.py',
    'Match': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/match.py',
    'Bet': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/bet.py',
    'Result': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/result.py',
    'Group': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/group.py',
    'GroupMembership': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/group_membership.py',
    'AuditLog': '/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/schemas/audit_log.py'
}

# Seed data file
seed_file = '/Users/chp/repos/GitHub/betting-league-championship/backend/seed_data.py'

print("# 🗄️ Database Field Analysis - Betting League Championship")
print("=" * 80)

# Analyze models
model_data = {}
for model_name, file_path in models.items():
    if os.path.exists(file_path):
        model_data[model_name] = extract_model_fields(file_path, model_name)

# Analyze schemas  
schema_data = {}
for schema_name, file_path in schemas.items():
    if os.path.exists(file_path):
        schema_data[schema_name] = extract_schema_fields(file_path)

# Analyze seed data
seed_fields = extract_seed_data_fields(seed_file) if os.path.exists(seed_file) else []

# Generate comprehensive table
print("\n## 📊 Comprehensive Field Mapping Table")
print("| Entity | Database Table | Model Fields | API Schema Fields | Seed Data Fields |")
print("|--------|---------------|--------------|-------------------|------------------|")

for entity in sorted(model_data.keys()):
    model_info = model_data.get(entity, {'table_name': 'N/A', 'fields': []})
    schema_fields = schema_data.get(entity, [])
    
    # Format fields for table
    model_fields_str = '<br>'.join(model_info['fields'][:10])  # Limit for readability
    if len(model_info['fields']) > 10:
        model_fields_str += f"<br>... (+{len(model_info['fields'])-10} more)"
    
    schema_fields_str = '<br>'.join(schema_fields[:10])  # Limit for readability  
    if len(schema_fields) > 10:
        schema_fields_str += f"<br>... (+{len(schema_fields)-10} more)"
    
    # Find entity-related seed fields (simple heuristic)
    entity_seed_fields = [f for f in seed_fields if entity.lower() in f.lower() or any(field.lower() in f.lower() for field in model_info['fields'][:5])]
    seed_fields_str = '<br>'.join(entity_seed_fields[:8])
    if len(entity_seed_fields) > 8:
        seed_fields_str += f"<br>... (+{len(entity_seed_fields)-8} more)"
    
    print(f"| **{entity}** | `{model_info['table_name']}` | {model_fields_str} | {schema_fields_str} | {seed_fields_str} |")

print(f"\n## 📈 Summary Statistics")
print(f"- **Total Entities**: {len(model_data)}")
print(f"- **Total Database Tables**: {len(set(info['table_name'] for info in model_data.values()))}")
print(f"- **Total Model Fields**: {sum(len(info['fields']) for info in model_data.values())}")
print(f"- **Total Schema Fields**: {sum(len(fields) for fields in schema_data.values())}")
print(f"- **Seed Data Field References**: {len(seed_fields)}")

print(f"\n## 🔍 Detailed Field Lists")
for entity in sorted(model_data.keys()):
    model_info = model_data.get(entity, {'table_name': 'N/A', 'fields': []})
    schema_fields = schema_data.get(entity, [])
    
    print(f"\n### {entity} ({model_info['table_name']})")
    print(f"**Model Fields ({len(model_info['fields'])}):**")
    for field in model_info['fields']:
        print(f"- {field}")
    
    print(f"\n**API Schema Fields ({len(schema_fields)}):**")
    for field in schema_fields[:15]:  # Show first 15
        print(f"- {field}")
    if len(schema_fields) > 15:
        print(f"- ... and {len(schema_fields)-15} more")