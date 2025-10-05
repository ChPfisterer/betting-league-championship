#!/usr/bin/env python3
"""
Enum Consistency Analysis
Analyzes enum values across Database Models, API Schemas, and Seed Data to identify inconsistencies.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

class EnumConsistencyAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.models_path = self.backend_path / "src" / "models"
        self.schemas_path = self.backend_path / "src" / "api" / "schemas"
        self.seed_path = self.backend_path / "seed_data.py"
        
    def extract_model_enums(self, model_file: Path) -> Dict[str, Dict[str, Set[str]]]:
        """Extract enum definitions and field constraints from model files"""
        enums = {}
        try:
            content = model_file.read_text()
            
            # Extract Enum class definitions
            enum_pattern = r'class\s+(\w+)\(Enum\):\s*\n((?:\s+[^\n]+\n)*)'
            for match in re.finditer(enum_pattern, content, re.MULTILINE):
                enum_name = match.group(1)
                enum_body = match.group(2)
                
                enum_values = set()
                # Extract enum values: VALUE = "value"
                value_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
                for value_match in re.finditer(value_pattern, enum_body):
                    enum_values.add(value_match.group(2))
                
                if enum_values:
                    enums[enum_name] = {
                        'type': 'enum_class',
                        'values': enum_values,
                        'fields_using': set()
                    }
            
            # Find fields that use these enums
            for enum_name in enums.keys():
                field_pattern = rf'(\w+)\s*=\s*Column\([^)]*Enum\({enum_name}\)'
                for match in re.finditer(field_pattern, content):
                    field_name = match.group(1)
                    enums[enum_name]['fields_using'].add(field_name)
            
            # Extract CheckConstraint enums
            constraint_pattern = r'CheckConstraint\([^)]*IN\s*\([^)]+\)'
            for match in re.finditer(constraint_pattern, content):
                constraint_text = match.group(0)
                # Extract values from IN clause
                values_pattern = r'["\']([^"\']+)["\']'
                values = set(re.findall(values_pattern, constraint_text))
                if values:
                    # Try to find associated field
                    field_context = content[max(0, match.start()-200):match.start()]
                    field_match = re.search(r'(\w+)\s*=\s*Column\([^)]*$', field_context)
                    if field_match:
                        field_name = field_match.group(1)
                        constraint_name = f"{field_name}_constraint"
                        enums[constraint_name] = {
                            'type': 'check_constraint',
                            'values': values,
                            'fields_using': {field_name}
                        }
                        
        except Exception as e:
            print(f"Error processing model {model_file}: {e}")
            
        return enums
    
    def extract_schema_enums(self, schema_file: Path) -> Dict[str, Dict[str, Set[str]]]:
        """Extract enum constraints from Pydantic schemas"""
        enums = {}
        try:
            content = schema_file.read_text()
            
            # Extract Literal type hints
            literal_pattern = r'(\w+)\s*:\s*Literal\[([^\]]+)\]'
            for match in re.finditer(literal_pattern, content):
                field_name = match.group(1)
                literal_values = match.group(2)
                
                # Parse literal values
                values = set()
                value_pattern = r'["\']([^"\']+)["\']'
                values.update(re.findall(value_pattern, literal_values))
                
                if values:
                    enum_name = f"{field_name}_literal"
                    enums[enum_name] = {
                        'type': 'literal',
                        'values': values,
                        'fields_using': {field_name}
                    }
            
            # Extract Enum imports and usage
            enum_import_pattern = r'from\s+[^\s]+\s+import\s+[^,\n]*(\w+Status|\w+Role|\w+Type)[^,\n]*'
            imported_enums = re.findall(enum_import_pattern, content)
            
            for enum_name in imported_enums:
                # Find fields using this enum
                field_pattern = rf'(\w+)\s*:\s*[^=\n]*{enum_name}'
                fields_using = set(re.findall(field_pattern, content))
                
                if fields_using:
                    enums[enum_name] = {
                        'type': 'imported_enum',
                        'values': set(),  # Will be filled from model analysis
                        'fields_using': fields_using
                    }
                    
        except Exception as e:
            print(f"Error processing schema {schema_file}: {e}")
            
        return enums
    
    def extract_seed_enum_values(self) -> Dict[str, Set[str]]:
        """Extract actual enum values used in seed data"""
        seed_enums = {}
        
        if not self.seed_path.exists():
            return seed_enums
            
        try:
            content = self.seed_path.read_text()
            
            # Common enum fields to look for
            enum_fields = {
                'status': 'status_values',
                'role': 'role_values',
                'category': 'category_values',
                'format_type': 'format_values',
                'position': 'position_values',
                'visibility': 'visibility_values',
                'bet_type': 'bet_type_values',
                'market_type': 'market_type_values'
            }
            
            for field_name, enum_key in enum_fields.items():
                # Look for field assignments in constructors
                pattern = rf'{field_name}\s*=\s*["\']([^"\']+)["\']'
                values = set(re.findall(pattern, content, re.IGNORECASE))
                
                if values:
                    seed_enums[enum_key] = values
                    
        except Exception as e:
            print(f"Error processing seed data: {e}")
            
        return seed_enums
    
    def analyze_enum_consistency(self) -> Dict[str, any]:
        """Analyze enum consistency across all layers"""
        analysis_results = {
            'entities': {},
            'summary': {
                'total_enums': 0,
                'consistent_enums': 0,
                'inconsistencies': []
            }
        }
        
        # Analyze each entity
        entity_files = [f for f in self.models_path.glob("*.py") if f.name != "__init__.py"]
        
        for model_file in entity_files:
            entity_name = model_file.stem.title()
            
            # Get corresponding schema file
            schema_file = self.schemas_path / f"{model_file.stem}.py"
            
            # Extract enums from each layer
            model_enums = self.extract_model_enums(model_file)
            schema_enums = {}
            if schema_file.exists():
                schema_enums = self.extract_schema_enums(schema_file)
            
            # Combine and analyze
            entity_analysis = {
                'model_enums': model_enums,
                'schema_enums': schema_enums,
                'inconsistencies': [],
                'recommendations': []
            }
            
            # Check for inconsistencies
            for model_enum_name, model_enum_data in model_enums.items():
                # Find corresponding schema enum
                matching_schema_enums = [
                    (name, data) for name, data in schema_enums.items()
                    if any(field in model_enum_data['fields_using'] for field in data['fields_using'])
                ]
                
                if not matching_schema_enums:
                    entity_analysis['inconsistencies'].append({
                        'type': 'missing_schema_enum',
                        'description': f"Model enum {model_enum_name} not found in schema",
                        'model_enum': model_enum_name,
                        'model_values': list(model_enum_data['values']),
                        'affected_fields': list(model_enum_data['fields_using'])
                    })
                else:
                    # Compare values
                    for schema_enum_name, schema_enum_data in matching_schema_enums:
                        if model_enum_data['values'] != schema_enum_data['values'] and schema_enum_data['values']:
                            entity_analysis['inconsistencies'].append({
                                'type': 'value_mismatch',
                                'description': f"Enum values don't match between model and schema",
                                'model_enum': model_enum_name,
                                'schema_enum': schema_enum_name,
                                'model_values': list(model_enum_data['values']),
                                'schema_values': list(schema_enum_data['values']),
                                'missing_in_schema': list(model_enum_data['values'] - schema_enum_data['values']),
                                'extra_in_schema': list(schema_enum_data['values'] - model_enum_data['values'])
                            })
            
            # Generate recommendations
            if entity_analysis['inconsistencies']:
                for inconsistency in entity_analysis['inconsistencies']:
                    if inconsistency['type'] == 'missing_schema_enum':
                        entity_analysis['recommendations'].append(
                            f"Add {inconsistency['model_enum']} to schema for fields: {', '.join(inconsistency['affected_fields'])}"
                        )
                    elif inconsistency['type'] == 'value_mismatch':
                        entity_analysis['recommendations'].append(
                            f"Synchronize enum values between {inconsistency['model_enum']} and {inconsistency['schema_enum']}"
                        )
            
            analysis_results['entities'][entity_name] = entity_analysis
            analysis_results['summary']['total_enums'] += len(model_enums)
            
            if not entity_analysis['inconsistencies']:
                analysis_results['summary']['consistent_enums'] += len(model_enums)
            else:
                analysis_results['summary']['inconsistencies'].extend(entity_analysis['inconsistencies'])
        
        # Add seed data analysis
        seed_enums = self.extract_seed_enum_values()
        analysis_results['seed_data'] = {
            'enum_values': seed_enums,
            'coverage_analysis': self.analyze_seed_coverage(analysis_results['entities'], seed_enums)
        }
        
        return analysis_results
    
    def analyze_seed_coverage(self, entities: Dict, seed_enums: Dict[str, Set[str]]) -> Dict:
        """Analyze how well seed data covers enum values"""
        coverage = {
            'well_covered': [],
            'partial_coverage': [],
            'no_coverage': [],
            'recommendations': []
        }
        
        # This is a simplified analysis - in a real implementation,
        # you'd map specific enum fields to seed usage patterns
        
        return coverage
    
    def generate_enum_consistency_report(self, analysis: Dict) -> str:
        """Generate comprehensive enum consistency report"""
        report = []
        
        report.append("# 🔢 Enum Consistency Analysis")
        report.append("## Betting League Championship Platform")
        report.append("")
        report.append("This document analyzes enum value consistency across Database Models, API Schemas, and Seed Data.")
        report.append("")
        
        # Summary
        total = analysis['summary']['total_enums']
        consistent = analysis['summary']['consistent_enums']
        consistency_rate = (consistent / total * 100) if total > 0 else 0
        
        report.append("## 📊 Enum Consistency Summary")
        report.append("")
        report.append(f"| Metric | Value |")
        report.append(f"|--------|-------|")
        report.append(f"| **Total Enums Found** | {total} |")
        report.append(f"| **Consistent Enums** | {consistent} |")
        report.append(f"| **Consistency Rate** | {consistency_rate:.1f}% |")
        report.append(f"| **Total Inconsistencies** | {len(analysis['summary']['inconsistencies'])} |")
        report.append("")
        
        # Entity-by-entity analysis
        for entity_name, entity_data in analysis['entities'].items():
            if entity_data['model_enums'] or entity_data['schema_enums']:
                report.append(f"## 🏷️ {entity_name} Enum Analysis")
                report.append("")
                
                # Model enums
                if entity_data['model_enums']:
                    report.append("### Database Model Enums")
                    for enum_name, enum_data in entity_data['model_enums'].items():
                        report.append(f"- **{enum_name}** ({enum_data['type']})")
                        report.append(f"  - Values: {', '.join(sorted(enum_data['values']))}")
                        report.append(f"  - Used by fields: {', '.join(enum_data['fields_using'])}")
                    report.append("")
                
                # Schema enums
                if entity_data['schema_enums']:
                    report.append("### API Schema Enums")
                    for enum_name, enum_data in entity_data['schema_enums'].items():
                        report.append(f"- **{enum_name}** ({enum_data['type']})")
                        if enum_data['values']:
                            report.append(f"  - Values: {', '.join(sorted(enum_data['values']))}")
                        report.append(f"  - Used by fields: {', '.join(enum_data['fields_using'])}")
                    report.append("")
                
                # Inconsistencies
                if entity_data['inconsistencies']:
                    report.append("### 🔴 Inconsistencies Found")
                    for issue in entity_data['inconsistencies']:
                        report.append(f"- **{issue['type'].replace('_', ' ').title()}**: {issue['description']}")
                        if 'missing_in_schema' in issue and issue['missing_in_schema']:
                            report.append(f"  - Missing in schema: {', '.join(issue['missing_in_schema'])}")
                        if 'extra_in_schema' in issue and issue['extra_in_schema']:
                            report.append(f"  - Extra in schema: {', '.join(issue['extra_in_schema'])}")
                    report.append("")
                
                # Recommendations
                if entity_data['recommendations']:
                    report.append("### 💡 Recommendations")
                    for rec in entity_data['recommendations']:
                        report.append(f"- {rec}")
                    report.append("")
                
                report.append("---")
                report.append("")
        
        # Seed data analysis
        if analysis['seed_data']['enum_values']:
            report.append("## 🌱 Seed Data Enum Usage")
            report.append("")
            for enum_key, values in analysis['seed_data']['enum_values'].items():
                report.append(f"- **{enum_key}**: {', '.join(sorted(values))}")
            report.append("")
        
        report.append("*Generated on: 5 October 2025*")
        
        return "\n".join(report)

def main():
    print("🚀 Starting Enum Consistency Analysis...")
    print("=" * 60)
    
    analyzer = EnumConsistencyAnalyzer("/Users/chp/repos/GitHub/betting-league-championship")
    
    print("🔍 Analyzing enum definitions across all layers...")
    analysis = analyzer.analyze_enum_consistency()
    
    print("📋 Generating comprehensive report...")
    report = analyzer.generate_enum_consistency_report(analysis)
    
    # Save report
    output_file = "/Users/chp/repos/GitHub/betting-league-championship/ENUM_CONSISTENCY_ANALYSIS.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Enum analysis saved to: {output_file}")
    
    # Print summary
    print("\n📊 ENUM CONSISTENCY SUMMARY")
    print("=" * 40)
    total = analysis['summary']['total_enums']
    consistent = analysis['summary']['consistent_enums']
    issues = len(analysis['summary']['inconsistencies'])
    
    print(f"Total Enums: {total}")
    print(f"Consistent: {consistent}")
    print(f"Issues Found: {issues}")
    
    if issues > 0:
        print(f"\n🔴 Issues Found:")
        for issue in analysis['summary']['inconsistencies'][:3]:  # Show first 3
            print(f"  - {issue['description']}")
        if issues > 3:
            print(f"  - ... and {issues - 3} more issues")
    else:
        print("🟢 No enum inconsistencies found!")

if __name__ == "__main__":
    main()