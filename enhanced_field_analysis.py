#!/usr/bin/env python3
"""
Enhanced Field Naming Consistency Analysis
Creates detailed field-by-field consistency tables across the entire stack.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

class EnhancedFieldAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.models_path = self.backend_path / "src" / "models"
        self.schemas_path = self.backend_path / "src" / "api" / "schemas"
        self.seed_path = self.backend_path / "seed_data.py"
        
    def extract_model_columns(self, model_file: Path) -> Dict[str, str]:
        """Extract Column definitions from a model file"""
        columns = {}
        try:
            content = model_file.read_text()
            
            # Extract Column definitions with more precision
            # Pattern: field_name = Column(type, ...)
            column_pattern = r'(\w+)\s*=\s*Column\s*\(\s*([^,)]+)(?:,\s*([^)]*))?\)'
            
            for match in re.finditer(column_pattern, content, re.MULTILINE):
                field_name = match.group(1)
                column_type = match.group(2).strip()
                constraints = match.group(3) or ""
                
                # Clean up the type
                if 'UUID' in column_type:
                    db_type = "UUID"
                elif 'String' in column_type:
                    db_type = "VARCHAR"
                elif 'Integer' in column_type:
                    db_type = "INTEGER"
                elif 'Boolean' in column_type:
                    db_type = "BOOLEAN"
                elif 'DateTime' in column_type:
                    db_type = "TIMESTAMP"
                elif 'Text' in column_type:
                    db_type = "TEXT"
                elif 'Decimal' in column_type:
                    db_type = "DECIMAL"
                else:
                    db_type = column_type
                
                columns[field_name] = db_type
                
        except Exception as e:
            print(f"Error processing model {model_file}: {e}")
            
        return columns
    
    def extract_schema_fields(self, schema_file: Path) -> Dict[str, Dict[str, str]]:
        """Extract field definitions from Pydantic schema file"""
        schemas = {}
        try:
            content = schema_file.read_text()
            
            # Find all class definitions that inherit from BaseModel
            class_pattern = r'class\s+(\w+)\s*\([^)]*BaseModel[^)]*\):\s*\n((?:\s+[^\n]+\n)*)'
            
            for match in re.finditer(class_pattern, content, re.MULTILINE):
                class_name = match.group(1)
                class_body = match.group(2)
                
                schemas[class_name] = {}
                
                # Extract field definitions: field_name: type annotation
                field_pattern = r'(\w+)\s*:\s*([^\n=]+?)(?:\s*=\s*[^\n]+)?(?:\n|$)'
                
                for field_match in re.finditer(field_pattern, class_body):
                    field_name = field_match.group(1)
                    field_type = field_match.group(2).strip()
                    
                    # Don't include class attributes or methods
                    if field_name.startswith('_') or 'class ' in field_type:
                        continue
                        
                    schemas[class_name][field_name] = field_type
                        
        except Exception as e:
            print(f"Error processing schema {schema_file}: {e}")
            
        return schemas
    
    def extract_seed_field_usage(self) -> Dict[str, Set[str]]:
        """Extract actual field usage from seed data"""
        seed_usage = {}
        
        if not self.seed_path.exists():
            return seed_usage
            
        try:
            content = self.seed_path.read_text()
            
            # Entity mappings
            entities = {
                'User': ['user', 'User'],
                'Sport': ['sport', 'Sport'], 
                'Team': ['team', 'Team'],
                'Player': ['player', 'Player'],
                'Competition': ['competition', 'Competition'],
                'Season': ['season', 'Season'],
                'Match': ['match', 'Match'],
                'Group': ['group', 'Group'],
            }
            
            for entity, patterns in entities.items():
                seed_usage[entity] = set()
                
                # Look for constructor patterns: Entity(field=value, ...)
                for pattern in patterns:
                    # Find constructor calls
                    constructor_pattern = rf'{pattern}\s*\([^)]+\)'
                    
                    for constructor_match in re.finditer(constructor_pattern, content, re.DOTALL):
                        constructor_text = constructor_match.group(0)
                        
                        # Extract field assignments within constructor
                        field_pattern = r'(\w+)\s*=\s*[^,)]+'
                        
                        for field_match in re.finditer(field_pattern, constructor_text):
                            field_name = field_match.group(1)
                            # Skip Python keywords and methods
                            if field_name not in ['id', 'uuid', 'datetime', 'timezone', 'Decimal']:
                                seed_usage[entity].add(field_name)
                                
        except Exception as e:
            print(f"Error processing seed data: {e}")
            
        return seed_usage
    
    def analyze_entity_consistency(self, entity_name: str) -> Dict[str, any]:
        """Analyze field consistency for a specific entity"""
        result = {
            'entity': entity_name,
            'database_fields': {},
            'schema_fields': {},
            'seed_fields': set(),
            'field_analysis': []
        }
        
        # Get model fields
        model_file = self.models_path / f"{entity_name.lower()}.py"
        if model_file.exists():
            result['database_fields'] = self.extract_model_columns(model_file)
        
        # Get schema fields
        schema_file = self.schemas_path / f"{entity_name.lower()}.py"
        if schema_file.exists():
            schemas = self.extract_schema_fields(schema_file)
            # Find schema that matches entity (could be EntityCreate, EntityUpdate, etc.)
            for schema_name, fields in schemas.items():
                if entity_name.lower() in schema_name.lower():
                    result['schema_fields'].update(fields)
        
        # Get seed fields
        seed_usage = self.extract_seed_field_usage()
        if entity_name in seed_usage:
            result['seed_fields'] = seed_usage[entity_name]
        
        # Analyze each field
        all_fields = set(result['database_fields'].keys()) | set(result['schema_fields'].keys()) | result['seed_fields']
        
        for field_name in sorted(all_fields):
            field_info = {
                'field_name': field_name,
                'in_database': field_name in result['database_fields'],
                'in_schema': field_name in result['schema_fields'],
                'in_seed': field_name in result['seed_fields'],
                'database_type': result['database_fields'].get(field_name, 'N/A'),
                'schema_type': result['schema_fields'].get(field_name, 'N/A'),
                'consistency_status': 'Unknown'
            }
            
            # Determine consistency status
            if field_info['in_database'] and field_info['in_schema']:
                if field_info['in_seed']:
                    field_info['consistency_status'] = '🟢 Full Stack'
                else:
                    field_info['consistency_status'] = '🟡 DB + API'
            elif field_info['in_database']:
                field_info['consistency_status'] = '🔵 DB Only'
            elif field_info['in_schema']:
                field_info['consistency_status'] = '🟠 API Only'
            else:
                field_info['consistency_status'] = '🔴 Seed Only'
            
            result['field_analysis'].append(field_info)
        
        return result
    
    def generate_detailed_report(self, entities: List[str]) -> str:
        """Generate comprehensive field analysis report"""
        report = []
        
        report.append("# 🔍 Field Naming Consistency Analysis")
        report.append("## Betting League Championship Platform")
        report.append("")
        report.append("This document provides field-by-field naming consistency analysis across the entire technology stack.")
        report.append("")
        
        # Summary stats
        total_entities = len(entities)
        report.append("## 📊 Analysis Summary")
        report.append("")
        report.append("| Status | Description |")
        report.append("|--------|-------------|")
        report.append("| 🟢 Full Stack | Field exists in Database, API Schema, and Seed Data |")
        report.append("| 🟡 DB + API | Field exists in Database and API Schema (most common) |")
        report.append("| 🔵 DB Only | Field exists only in Database Model |")
        report.append("| 🟠 API Only | Field exists only in API Schema |")
        report.append("| 🔴 Seed Only | Field exists only in Seed Data |")
        report.append("")
        
        # Analyze each entity
        for entity_name in entities:
            analysis = self.analyze_entity_consistency(entity_name)
            
            report.append(f"## 🏷️ {entity_name} Field Analysis")
            report.append("")
            
            # Statistics
            total_fields = len(analysis['field_analysis'])
            full_stack = len([f for f in analysis['field_analysis'] if f['consistency_status'] == '🟢 Full Stack'])
            db_api = len([f for f in analysis['field_analysis'] if f['consistency_status'] == '🟡 DB + API'])
            
            report.append(f"**Total Fields:** {total_fields} | **Full Stack:** {full_stack} | **DB + API:** {db_api}")
            report.append("")
            
            # Field table
            report.append("| Field Name | Database Type | API Schema Type | Seed Data | Status |")
            report.append("|------------|---------------|-----------------|-----------|---------|")
            
            for field in analysis['field_analysis']:
                seed_check = "✅" if field['in_seed'] else "❌"
                
                report.append(
                    f"| `{field['field_name']}` | "
                    f"{field['database_type']} | "
                    f"{field['schema_type']} | "
                    f"{seed_check} | "
                    f"{field['consistency_status']} |"
                )
            
            # Consistency metrics
            if total_fields > 0:
                consistency_rate = ((full_stack + db_api) / total_fields) * 100
                report.append("")
                report.append(f"**Consistency Rate:** {consistency_rate:.1f}% ({full_stack + db_api}/{total_fields} fields consistent)")
            
            report.append("")
            report.append("---")
            report.append("")
        
        report.append(f"*Generated on: 5 October 2025*")
        report.append(f"*Total Entities Analyzed: {total_entities}*")
        
        return "\n".join(report)

def main():
    print("🚀 Starting Enhanced Field Naming Consistency Analysis...")
    print("=" * 70)
    
    analyzer = EnhancedFieldAnalyzer("/Users/chp/repos/GitHub/betting-league-championship")
    
    # Main entities to analyze
    entities = [
        "User", "Sport", "Team", "Player", "Competition", 
        "Season", "Match", "Bet", "Result", "Group", 
        "GroupMembership", "AuditLog"
    ]
    
    print(f"📋 Analyzing {len(entities)} entities...")
    
    # Generate comprehensive report
    report = analyzer.generate_detailed_report(entities)
    
    # Save to file
    output_file = "/Users/chp/repos/GitHub/betting-league-championship/ENHANCED_FIELD_CONSISTENCY.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Enhanced analysis saved to: {output_file}")
    
    # Print summary
    print("\n📋 QUICK SUMMARY")
    print("=" * 40)
    for entity in entities[:6]:  # Show first 6 entities
        analysis = analyzer.analyze_entity_consistency(entity)
        total = len(analysis['field_analysis'])
        consistent = len([f for f in analysis['field_analysis'] 
                         if 'Full Stack' in f['consistency_status'] or 'DB + API' in f['consistency_status']])
        rate = (consistent / total * 100) if total > 0 else 0
        print(f"{entity:15} | {consistent:2}/{total:2} fields | {rate:5.1f}% consistent")

if __name__ == "__main__":
    main()