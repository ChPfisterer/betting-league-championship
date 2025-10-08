#!/usr/bin/env python3
"""
Test script to verify email validation fix for .local domains.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from api.schemas.user import UserBase

def test_email_validation():
    """Test email validation with various email formats."""
    test_cases = [
        # Should pass in debug mode
        ("chris@test.local", True, "Local domain should pass in debug mode"),
        ("user@dev.local", True, "Local domain should pass in debug mode"),
        
        # Should always pass
        ("user@example.com", True, "Valid domain should always pass"),
        ("test@gmail.com", True, "Valid domain should always pass"),
        
        # Should always fail
        ("invalid-email", False, "Invalid format should fail"),
        ("user@", False, "Incomplete email should fail"),
        ("@domain.com", False, "Missing local part should fail"),
    ]
    
    print("Testing email validation...")
    print("=" * 50)
    
    for email, should_pass, description in test_cases:
        try:
            # Try to create a UserBase instance with the email
            user_data = {
                "username": "testuser",
                "email": email,
                "first_name": "Test",
                "last_name": "User"
            }
            user = UserBase(**user_data)
            result = True
            print(f"✅ PASS: {email} - {description}")
        except ValueError as e:
            result = False
            print(f"❌ FAIL: {email} - {description} (Error: {str(e)})")
        
        # Check if result matches expectation
        if result != should_pass:
            print(f"   ⚠️  UNEXPECTED: Expected {should_pass}, got {result}")
    
    print("=" * 50)
    print("Email validation test completed!")

if __name__ == "__main__":
    test_email_validation()