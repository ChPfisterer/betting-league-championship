#!/usr/bin/env python3
"""
Script to update authentication imports in API endpoint files.
Converts from traditional authentication to Keycloak-only authentication.
"""

import re
import os
from pathlib import Path

def update_auth_imports(file_path):
    """Update authentication imports and function calls in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Add Keycloak import if needed
    if 'from core.keycloak_security import' not in content:
        # Find the position after model imports
        if 'from models.' in content:
            # Add after the last model import
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('from models.'):
                    # Find the end of this import block
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith('from api.') or lines[j].strip() == '' or lines[j].startswith(' ')):
                        j += 1
                    # Insert the Keycloak import before the api imports
                    lines.insert(j, 'from core.keycloak_security import get_current_user_hybrid, get_current_user_id_hybrid')
                    content = '\n'.join(lines)
                    break
    
    # Replace function calls
    content = re.sub(r'Depends\(get_current_user\)', 'Depends(get_current_user_hybrid)', content)
    content = re.sub(r'Depends\(get_current_user_id\)', 'Depends(get_current_user_id_hybrid)', content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Updated {file_path}")
        return True
    return False

def main():
    """Main function to update all endpoint files."""
    base_path = Path("/Users/chp/repos/GitHub/betting-league-championship/backend/src/api/v1/endpoints")
    
    files_to_update = [
        "seasons.py",
        "matches.py", 
        "results.py"
    ]
    
    updated_count = 0
    for filename in files_to_update:
        file_path = base_path / filename
        if file_path.exists():
            if update_auth_imports(file_path):
                updated_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nUpdated {updated_count} files")

if __name__ == "__main__":
    main()