#!/usr/bin/env python3
"""
Enhanced Enum Consistency Analysis
Provides detailed analysis of enum usage consistency across the entire stack.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

class DetailedEnumAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.models_path = self.backend_path / "src" / "models"
        self.schemas_path = self.backend_path / "src" / "api" / "schemas"
        self.seed_path = self.backend_path / "seed_data.py"
        
    def extract_enum_definitions(self, file_path: Path) -> Dict[str, Dict]:
        """Extract enum class definitions and their values"""
        enums = {}
        
        if not file_path.exists():
            return enums
            
        try:
            content = file_path.read_text()
            
            # Pattern for enum class definitions
            enum_pattern = r'class\s+(\w+)\(Enum\):\s*\n(?:\s*"""[^"]*"""\s*\n)?((?:\s+\w+\s*=\s*["\'][^"\']+["\'].*\n)*)'
            
            for match in re.finditer(enum_pattern, content, re.MULTILINE):
                enum_name = match.group(1)
                enum_body = match.group(2)
                
                # Extract enum values
                values = {}
                value_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
                
                for value_match in re.finditer(value_pattern, enum_body):
                    key = value_match.group(1)
                    value = value_match.group(2)
                    values[key] = value
                
                if values:
                    enums[enum_name] = {
                        'file': str(file_path),
                        'values': values,
                        'value_list': list(values.values())
                    }
                    
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
        return enums
    
    def find_enum_usage_in_models(self, model_file: Path) -> Dict[str, List[str]]:
        """Find which fields use which enums in model files"""
        usage = defaultdict(list)
        
        if not model_file.exists():
            return dict(usage)
            
        try:
            content = model_file.read_text()
            
            # Look for Column definitions with Enum
            enum_usage_pattern = r'(\w+)\s*=\s*Column\([^)]*Enum\((\w+)\)'
            
            for match in re.finditer(enum_usage_pattern, content):
                field_name = match.group(1)
                enum_name = match.group(2)
                usage[enum_name].append(field_name)
                
        except Exception as e:
            print(f"Error processing model {model_file}: {e}")
            
        return dict(usage)
    
    def find_enum_usage_in_schemas(self, schema_file: Path) -> Dict[str, List[str]]:
        """Find which fields use which enums in schema files"""
        usage = defaultdict(list)
        
        if not schema_file.exists():
            return dict(usage)
            
        try:
            content = schema_file.read_text()
            
            # Look for imported enums
            import_pattern = r'from\s+models\.\w+\s+import\s+([^,\n]+)'
            imported_enums = []
            
            for match in re.finditer(import_pattern, content):
                imports = [e.strip() for e in match.group(1).split(',')]
                imported_enums.extend(imports)
            
            # Look for field definitions using these enums
            for enum_name in imported_enums:
                field_pattern = rf'(\w+)\s*:\s*[^=\n]*{enum_name}'
                
                for field_match in re.finditer(field_pattern, content):
                    field_name = field_match.group(1)
                    usage[enum_name].append(field_name)
                    
        except Exception as e:
            print(f"Error processing schema {schema_file}: {e}")
            
        return dict(usage)
    
    def extract_seed_enum_values(self) -> Dict[str, Set[str]]:
        """Extract enum values actually used in seed data"""
        seed_values = defaultdict(set)
        
        if not self.seed_path.exists():
            return dict(seed_values)
            
        try:
            content = self.seed_path.read_text()
            
            # Define field patterns to look for
            field_patterns = {
                'status': r'status\s*=\s*["\']([^"\']+)["\']',
                'role': r'role\s*=\s*["\']([^"\']+)["\']',
                'category': r'category\s*=\s*["\']([^"\']+)["\']',
                'format_type': r'format_type\s*=\s*["\']([^"\']+)["\']',
                'visibility': r'visibility\s*=\s*["\']([^"\']+)["\']',
                'position': r'position\s*=\s*["\']([^"\']+)["\']',
                'bet_type': r'bet_type\s*=\s*["\']([^"\']+)["\']',
                'market_type': r'market_type\s*=\s*["\']([^"\']+)["\']',
            }
            
            for field_name, pattern in field_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    seed_values[field_name].update(matches)
                    
        except Exception as e:
            print(f"Error processing seed data: {e}")
            
        return dict(seed_values)
    
    def analyze_entity_enums(self, entity_name: str) -> Dict:
        """Analyze enum consistency for a specific entity"""
        entity_file = entity_name.lower()
        
        # Get model enums
        model_file = self.models_path / f"{entity_file}.py"
        model_enums = self.extract_enum_definitions(model_file)
        model_usage = self.find_enum_usage_in_models(model_file)
        
        # Get schema enums
        schema_file = self.schemas_path / f"{entity_file}.py"
        schema_usage = self.find_enum_usage_in_schemas(schema_file)
        
        # Analysis
        analysis = {
            'entity': entity_name,
            'model_enums': model_enums,
            'model_usage': model_usage,
            'schema_usage': schema_usage,
            'issues': [],
            'recommendations': []
        }
        
        # Check for missing schema imports
        for enum_name in model_enums.keys():
            if enum_name in model_usage and enum_name not in schema_usage:
                analysis['issues'].append({
                    'type': 'missing_schema_import',
                    'enum': enum_name,
                    'description': f'Enum {enum_name} used in model but not imported in schema',
                    'model_fields': model_usage[enum_name],
                    'recommendation': f'Import {enum_name} from models.{entity_file} in schema'
                })
        
        # Check for unused imports
        for enum_name in schema_usage.keys():
            if enum_name not in model_enums:
                analysis['issues'].append({
                    'type': 'unknown_enum_import',
                    'enum': enum_name,
                    'description': f'Enum {enum_name} imported in schema but not defined in model',
                    'schema_fields': schema_usage[enum_name],
                    'recommendation': f'Verify {enum_name} is correctly imported or defined'
                })
        
        return analysis
    
    def check_seed_data_compliance(self, all_enums: Dict, seed_values: Dict) -> Dict:
        """Check if seed data values comply with defined enums"""
        compliance = {
            'compliant': [],
            'violations': [],
            'missing_coverage': []
        }
        
        # Map seed field names to enum names
        field_to_enum_mapping = {
            'status': ['UserStatus', 'MatchStatus', 'CompetitionStatus', 'ResultStatus'],
            'role': ['UserRole', 'MembershipRole'],
            'category': ['SportCategory'],
            'format_type': ['CompetitionFormat'],
            'visibility': ['CompetitionVisibility'],
            'position': ['PlayerPosition'],
            'bet_type': ['BetType'],
            'market_type': ['MarketType']
        }
        
        for field_name, seed_vals in seed_values.items():
            if field_name in field_to_enum_mapping:
                for enum_name in field_to_enum_mapping[field_name]:
                    # Find the enum definition
                    enum_def = None
                    for entity_enums in all_enums.values():
                        if enum_name in entity_enums:
                            enum_def = entity_enums[enum_name]
                            break
                    
                    if enum_def:
                        valid_values = set(enum_def['value_list'])
                        violations = seed_vals - valid_values
                        
                        if violations:
                            compliance['violations'].append({
                                'field': field_name,
                                'enum': enum_name,
                                'invalid_values': list(violations),
                                'valid_values': list(valid_values),
                                'recommendation': f'Update seed data to use valid {enum_name} values'
                            })
                        else:
                            compliance['compliant'].append({
                                'field': field_name,
                                'enum': enum_name,
                                'values_used': list(seed_vals)
                            })
                            
                        # Check coverage
                        unused_values = valid_values - seed_vals
                        if unused_values:
                            compliance['missing_coverage'].append({
                                'field': field_name,
                                'enum': enum_name,
                                'unused_values': list(unused_values),
                                'coverage_percentage': len(seed_vals) / len(valid_values) * 100
                            })
        
        return compliance
    
    def generate_investigation_report(self) -> str:
        """Generate comprehensive investigation report"""
        print("🔍 Extracting all enum definitions...")
        
        # Extract all enums
        all_enums = {}
        entities = []
        
        for model_file in self.models_path.glob("*.py"):
            if model_file.name != "__init__.py":
                entity_name = model_file.stem.title()
                entities.append(entity_name)
                entity_enums = self.extract_enum_definitions(model_file)
                if entity_enums:
                    all_enums[entity_name] = entity_enums
        
        print("📊 Analyzing entity-specific enum usage...")
        
        # Analyze each entity
        entity_analyses = {}
        for entity in entities:
            entity_analyses[entity] = self.analyze_entity_enums(entity)
        
        print("🌱 Checking seed data compliance...")
        
        # Check seed data
        seed_values = self.extract_seed_enum_values()
        seed_compliance = self.check_seed_data_compliance(all_enums, seed_values)
        
        # Generate report
        report = []
        report.append("# 🔢 Enhanced Enum Consistency Investigation")
        report.append("## Betting League Championship Platform")
        report.append("")
        report.append("Comprehensive analysis of enum value consistency across Database Models, API Schemas, and Seed Data.")
        report.append("")
        
        # Executive Summary
        total_enums = sum(len(enums) for enums in all_enums.values())
        total_issues = sum(len(analysis['issues']) for analysis in entity_analyses.values())
        
        report.append("## 🎯 Executive Summary")
        report.append("")
        report.append(f"| Metric | Count |")
        report.append(f"|--------|-------|")
        report.append(f"| **Total Enum Definitions** | {total_enums} |")
        report.append(f"| **Entities with Enums** | {len(all_enums)} |")
        report.append(f"| **Schema Integration Issues** | {total_issues} |")
        report.append(f"| **Seed Data Violations** | {len(seed_compliance['violations'])} |")
        report.append(f"| **Compliant Seed Fields** | {len(seed_compliance['compliant'])} |")
        report.append("")
        
        # Detailed analysis by entity
        report.append("## 📋 Entity-by-Entity Analysis")
        report.append("")
        
        for entity_name, analysis in entity_analyses.items():
            if analysis['model_enums'] or analysis['issues']:
                report.append(f"### 🏷️ {entity_name}")
                report.append("")
                
                # Enum definitions
                if analysis['model_enums']:
                    report.append("**Defined Enums:**")
                    for enum_name, enum_data in analysis['model_enums'].items():
                        values = ', '.join(enum_data['value_list'])
                        report.append(f"- **{enum_name}**: {values}")
                    report.append("")
                
                # Usage information
                if analysis['model_usage']:
                    report.append("**Model Field Usage:**")
                    for enum_name, fields in analysis['model_usage'].items():
                        report.append(f"- **{enum_name}**: {', '.join(fields)}")
                    report.append("")
                
                if analysis['schema_usage']:
                    report.append("**Schema Field Usage:**")
                    for enum_name, fields in analysis['schema_usage'].items():
                        report.append(f"- **{enum_name}**: {', '.join(fields)}")
                    report.append("")
                
                # Issues
                if analysis['issues']:
                    report.append("**🔴 Issues Found:**")
                    for issue in analysis['issues']:
                        report.append(f"- **{issue['type']}**: {issue['description']}")
                        report.append(f"  - *Recommendation*: {issue['recommendation']}")
                    report.append("")
                else:
                    report.append("**✅ No issues found**")
                    report.append("")
                
                report.append("---")
                report.append("")
        
        # Seed data analysis
        report.append("## 🌱 Seed Data Compliance Analysis")
        report.append("")
        
        if seed_compliance['compliant']:
            report.append("### ✅ Compliant Fields")
            for item in seed_compliance['compliant']:
                report.append(f"- **{item['field']}** ({item['enum']}): {', '.join(item['values_used'])}")
            report.append("")
        
        if seed_compliance['violations']:
            report.append("### 🔴 Violations Found")
            for violation in seed_compliance['violations']:
                report.append(f"- **{violation['field']}** ({violation['enum']})")
                report.append(f"  - Invalid values: {', '.join(violation['invalid_values'])}")
                report.append(f"  - Valid options: {', '.join(violation['valid_values'])}")
                report.append(f"  - *Fix*: {violation['recommendation']}")
            report.append("")
        
        if seed_compliance['missing_coverage']:
            report.append("### ⚠️ Missing Coverage")
            for missing in seed_compliance['missing_coverage']:
                coverage = missing['coverage_percentage']
                report.append(f"- **{missing['field']}** ({missing['enum']}): {coverage:.1f}% coverage")
                report.append(f"  - Unused values: {', '.join(missing['unused_values'])}")
            report.append("")
        
        # Recommendations
        report.append("## 💡 Next Steps & Recommendations")
        report.append("")
        
        if total_issues > 0:
            report.append("### 🔧 Immediate Actions Required")
            report.append("")
            for entity_name, analysis in entity_analyses.items():
                for issue in analysis['issues']:
                    if issue['type'] == 'missing_schema_import':
                        report.append(f"1. **{entity_name} Schema**: {issue['recommendation']}")
            report.append("")
        
        if seed_compliance['violations']:
            report.append("### 🌱 Seed Data Fixes")
            report.append("")
            for i, violation in enumerate(seed_compliance['violations'], 1):
                report.append(f"{i}. Update seed data field `{violation['field']}` to use valid {violation['enum']} values")
            report.append("")
        
        report.append("### 📈 Improvement Opportunities")
        report.append("")
        report.append("1. **Add enum validation** to API schemas for all enum fields")
        report.append("2. **Expand seed data coverage** to include more enum values for testing")
        report.append("3. **Create enum documentation** for frontend developers")
        report.append("4. **Set up automated testing** to catch enum inconsistencies")
        report.append("")
        
        report.append("*Generated on: 5 October 2025*")
        
        return "\n".join(report)

def main():
    print("🚀 Starting Enhanced Enum Consistency Investigation...")
    print("=" * 70)
    
    analyzer = DetailedEnumAnalyzer("/Users/chp/repos/GitHub/betting-league-championship")
    
    report = analyzer.generate_investigation_report()
    
    # Save report
    output_file = "/Users/chp/repos/GitHub/betting-league-championship/ENUM_INVESTIGATION_REPORT.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Investigation report saved to: {output_file}")

if __name__ == "__main__":
    main()