#!/usr/bin/env python3
"""
Field Naming Consistency Analysis
Traces field names across the entire technology stack to identify discrepancies.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional

class FieldNamingAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.models_path = self.backend_path / "src" / "models"
        self.schemas_path = self.backend_path / "src" / "api" / "schemas"
        self.seed_path = self.backend_path / "seed_data.py"
        
        # Storage for field mappings
        self.field_mappings = {}
        
    def extract_database_model_fields(self) -> Dict[str, Dict[str, str]]:
        """Extract field definitions from SQLAlchemy models"""
        model_fields = {}
        
        if not self.models_path.exists():
            print(f"Models path not found: {self.models_path}")
            return model_fields
            
        for model_file in self.models_path.glob("*.py"):
            if model_file.name == "__init__.py":
                continue
                
            try:
                content = model_file.read_text()
                
                # Extract class name
                class_match = re.search(r'class\s+(\w+)\s*\(.*Base.*\):', content)
                if not class_match:
                    continue
                    
                class_name = class_match.group(1)
                model_fields[class_name] = {}
                
                # Extract Column definitions
                column_pattern = r'(\w+)\s*=\s*Column\s*\(\s*([^)]+)\)'
                for match in re.finditer(column_pattern, content):
                    field_name = match.group(1)
                    column_def = match.group(2)
                    model_fields[class_name][field_name] = column_def.strip()
                    
                # Extract relationship definitions
                relationship_pattern = r'(\w+)\s*=\s*relationship\s*\(\s*["\']([^"\']+)["\']'
                for match in re.finditer(relationship_pattern, content):
                    field_name = match.group(1)
                    target_model = match.group(2)
                    model_fields[class_name][field_name] = f"relationship -> {target_model}"
                    
            except Exception as e:
                print(f"Error processing {model_file}: {e}")
                
        return model_fields
    
    def extract_api_schema_fields(self) -> Dict[str, Dict[str, str]]:
        """Extract field definitions from Pydantic schemas"""
        schema_fields = {}
        
        if not self.schemas_path.exists():
            print(f"Schemas path not found: {self.schemas_path}")
            return schema_fields
            
        for schema_file in self.schemas_path.glob("*.py"):
            if schema_file.name == "__init__.py":
                continue
                
            try:
                content = schema_file.read_text()
                
                # Extract class definitions
                class_pattern = r'class\s+(\w+)\s*\([^)]*BaseModel[^)]*\):\s*\n((?:\s+[^\n]+\n)*)'
                for match in re.finditer(class_pattern, content, re.MULTILINE):
                    class_name = match.group(1)
                    class_body = match.group(2)
                    
                    schema_fields[class_name] = {}
                    
                    # Extract field definitions from class body
                    field_pattern = r'(\w+)\s*:\s*([^\n=]+)(?:\s*=\s*([^\n]+))?'
                    for field_match in re.finditer(field_pattern, class_body):
                        field_name = field_match.group(1)
                        field_type = field_match.group(2).strip()
                        default_value = field_match.group(3)
                        
                        field_def = field_type
                        if default_value:
                            field_def += f" = {default_value.strip()}"
                            
                        schema_fields[class_name][field_name] = field_def
                        
            except Exception as e:
                print(f"Error processing {schema_file}: {e}")
                
        return schema_fields
    
    def extract_seed_data_fields(self) -> Dict[str, Set[str]]:
        """Extract field names used in seed data"""
        seed_fields = {}
        
        if not self.seed_path.exists():
            print(f"Seed data file not found: {self.seed_path}")
            return seed_fields
            
        try:
            content = self.seed_path.read_text()
            
            # Look for dictionary definitions with field assignments
            # Pattern for things like: {"field_name": value, ...}
            dict_pattern = r'\{([^}]+)\}'
            
            entities = ["User", "Sport", "Team", "Player", "Competition", "Season", "Match", "Group"]
            
            for entity in entities:
                seed_fields[entity] = set()
                
                # Look for entity-specific patterns
                entity_pattern = rf'{entity.lower()}_data\s*=.*?\[(.*?)\]'
                entity_match = re.search(entity_pattern, content, re.DOTALL)
                
                if entity_match:
                    entity_data = entity_match.group(1)
                    
                    # Extract field names from dictionaries
                    for dict_match in re.finditer(dict_pattern, entity_data):
                        dict_content = dict_match.group(1)
                        
                        # Extract field names
                        field_pattern = r'["\'](\w+)["\']:'
                        for field_match in re.finditer(field_pattern, dict_content):
                            field_name = field_match.group(1)
                            seed_fields[entity].add(field_name)
                            
        except Exception as e:
            print(f"Error processing seed data: {e}")
            
        return seed_fields
    
    def get_database_table_name(self, model_name: str) -> str:
        """Get the database table name for a model"""
        # Common patterns for table naming
        table_mapping = {
            "User": "users",
            "Sport": "sports", 
            "Team": "teams",
            "Player": "players",
            "Competition": "competitions",
            "Season": "seasons",
            "Match": "matches",
            "Bet": "bets",
            "Result": "results",
            "Group": "groups",
            "GroupMembership": "group_memberships",
            "AuditLog": "audit_logs"
        }
        return table_mapping.get(model_name, model_name.lower() + "s")
    
    def analyze_field_consistency(self):
        """Perform comprehensive field consistency analysis"""
        print("🔍 Extracting field definitions from all layers...")
        
        # Extract from all layers
        model_fields = self.extract_database_model_fields()
        schema_fields = self.extract_api_schema_fields()
        seed_fields = self.extract_seed_data_fields()
        
        print(f"✅ Found {len(model_fields)} model classes")
        print(f"✅ Found {len(schema_fields)} schema classes")
        print(f"✅ Found {len(seed_fields)} seed data entities")
        
        # Build comprehensive field mapping
        all_entities = set(model_fields.keys()) | set(schema_fields.keys()) | set(seed_fields.keys())
        
        self.field_mappings = {}
        
        for entity in sorted(all_entities):
            if entity in model_fields:
                model_field_names = set(model_fields[entity].keys())
                schema_field_names = set()
                seed_field_names = set()
                
                # Find corresponding schema
                schema_candidates = [name for name in schema_fields.keys() if entity in name or name in entity]
                for schema_name in schema_candidates:
                    schema_field_names.update(schema_fields[schema_name].keys())
                
                # Get seed data fields
                if entity in seed_fields:
                    seed_field_names = seed_fields[entity]
                
                # Get all unique field names
                all_field_names = model_field_names | schema_field_names | seed_field_names
                
                self.field_mappings[entity] = {
                    'table_name': self.get_database_table_name(entity),
                    'model_fields': model_fields.get(entity, {}),
                    'schema_fields': {name: fields for name, fields in schema_fields.items() if entity in name or name in entity},
                    'seed_fields': seed_field_names,
                    'all_field_names': all_field_names
                }
        
        return self.field_mappings
    
    def generate_consistency_report(self) -> str:
        """Generate detailed consistency report"""
        report = []
        
        for entity, mapping in self.field_mappings.items():
            report.append(f"\n## 🔍 {entity} Field Consistency Analysis")
            report.append(f"**Database Table:** `{mapping['table_name']}`\n")
            
            # Get all field names across layers
            all_fields = mapping['all_field_names']
            model_fields = set(mapping['model_fields'].keys())
            seed_fields = mapping['seed_fields']
            
            # Combine all schema fields
            schema_fields = set()
            for schema_name, fields in mapping['schema_fields'].items():
                schema_fields.update(fields.keys())
            
            if all_fields:
                report.append("| Field Name | Database Model | API Schema | Seed Data | Status |")
                report.append("|------------|----------------|------------|-----------|---------|")
                
                for field in sorted(all_fields):
                    # Check presence in each layer
                    in_model = "✅" if field in model_fields else "❌"
                    in_schema = "✅" if field in schema_fields else "❌"
                    in_seed = "✅" if field in seed_fields else "❌"
                    
                    # Determine status
                    status = "🟢 Consistent" if all([field in model_fields, field in schema_fields]) else "🟡 Partial"
                    if field not in model_fields and field not in schema_fields:
                        status = "🔴 Missing"
                    
                    report.append(f"| `{field}` | {in_model} | {in_schema} | {in_seed} | {status} |")
                
                # Summary stats
                total_fields = len(all_fields)
                consistent_fields = len([f for f in all_fields if f in model_fields and f in schema_fields])
                consistency_rate = (consistent_fields / total_fields) * 100 if total_fields > 0 else 0
                
                report.append(f"\n**Consistency Rate:** {consistency_rate:.1f}% ({consistent_fields}/{total_fields} fields)")
            else:
                report.append("*No fields found for this entity.*")
            
            report.append("\n---")
        
        return "\n".join(report)

def main():
    analyzer = FieldNamingAnalyzer("/Users/chp/repos/GitHub/betting-league-championship")
    
    print("🚀 Starting Field Naming Consistency Analysis...")
    print("=" * 60)
    
    # Perform analysis
    mappings = analyzer.analyze_field_consistency()
    
    # Generate report
    report = analyzer.generate_consistency_report()
    
    print("\n📋 FIELD NAMING CONSISTENCY REPORT")
    print("=" * 60)
    print(report)
    
    # Save to file
    report_file = "/Users/chp/repos/GitHub/betting-league-championship/FIELD_NAMING_CONSISTENCY.md"
    with open(report_file, 'w') as f:
        f.write("# 🔍 Field Naming Consistency Analysis\n")
        f.write("## Betting League Championship Platform\n\n")
        f.write("This document analyzes field naming consistency across the entire technology stack.\n")
        f.write(report)
        f.write(f"\n\n*Generated on: 5 October 2025*\n")
        f.write(f"*Total Entities Analyzed: {len(mappings)}*\n")
    
    print(f"\n✅ Report saved to: {report_file}")

if __name__ == "__main__":
    main()