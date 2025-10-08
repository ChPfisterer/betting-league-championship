#!/usr/bin/env python3
"""
Script to fix Keycloak configuration to include the 'sub' field in JWT tokens.
This adds the necessary protocol mapper to the betting-frontend client.
"""

import requests
import json
import time

KEYCLOAK_URL = "http://localhost:8090"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
REALM = "betting-platform"
CLIENT_ID = "betting-frontend"

def get_admin_token():
    """Get admin access token for Keycloak API calls."""
    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get admin token: {response.text}")
    
    return response.json()["access_token"]

def get_client_uuid(token, client_id):
    """Get the internal UUID for a client by its clientId."""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get clients: {response.text}")
    
    clients = response.json()
    for client in clients:
        if client["clientId"] == client_id:
            return client["id"]
    
    raise Exception(f"Client {client_id} not found")

def add_sub_protocol_mapper(token, client_uuid):
    """Add protocol mapper for the 'sub' field to the client."""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients/{client_uuid}/protocol-mappers/models"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    mapper_config = {
        "name": "subject-mapper",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-usermodel-property-mapper",
        "consentRequired": False,
        "config": {
            "user.attribute": "id",
            "claim.name": "sub",
            "jsonType.label": "String",
            "id.token.claim": "true",
            "access.token.claim": "true",
            "userinfo.token.claim": "true"
        }
    }
    
    response = requests.post(url, headers=headers, json=mapper_config)
    if response.status_code == 201:
        print("✅ Successfully added 'sub' field protocol mapper")
        return True
    elif response.status_code == 409:
        print("⚠️  Protocol mapper already exists")
        return True
    else:
        raise Exception(f"Failed to add protocol mapper: {response.status_code} - {response.text}")

def verify_sub_field_configuration():
    """Test if the sub field is now included in tokens."""
    # This would require a test login - we'll rely on the backend logs for verification
    print("🔍 To verify the fix:")
    print("1. Logout and login again in the frontend")
    print("2. Check backend logs for 'Token subject:' - should now show a UUID instead of None")
    print("3. Look for absence of 'Token missing sub field' warnings")

def main():
    try:
        print("🔧 Fixing Keycloak JWT 'sub' field configuration...")
        
        # Get admin token
        print("🔐 Getting admin access token...")
        token = get_admin_token()
        
        # Get client UUID
        print(f"🔍 Finding client UUID for '{CLIENT_ID}'...")
        client_uuid = get_client_uuid(token, CLIENT_ID)
        print(f"📝 Client UUID: {client_uuid}")
        
        # Add sub protocol mapper
        print("➕ Adding 'sub' field protocol mapper...")
        add_sub_protocol_mapper(token, client_uuid)
        
        print("\n✅ Keycloak configuration updated successfully!")
        print("\n📋 What was changed:")
        print("- Added 'subject-mapper' protocol mapper to betting-frontend client")
        print("- Maps user.id -> JWT 'sub' claim")
        print("- Included in access tokens, ID tokens, and userinfo")
        
        verify_sub_field_configuration()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())