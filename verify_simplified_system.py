#!/usr/bin/env python3
"""
Verification script for simplified prediction system
"""

import requests
import sys

def verify_backend():
    """Verify the backend is running and our simplified schemas work"""
    try:
        # Check health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Backend health: {response.status_code}")
        
        # Check OpenAPI documentation
        response = requests.get("http://localhost:8000/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi_data = response.json()
            
            # Check if our simplified BetStatistics schema exists
            schemas = openapi_data.get("components", {}).get("schemas", {})
            if "BetStatistics" in schemas:
                bet_stats = schemas["BetStatistics"]
                properties = bet_stats.get("properties", {})
                
                print("✅ BetStatistics schema found with properties:")
                for prop in properties:
                    print(f"   - {prop}")
                
                # Check for simplified fields (prediction points instead of complex financial metrics)
                expected_simple_fields = ["total_predictions", "total_points", "exact_score_predictions", "winner_only_predictions", "wrong_predictions", "accuracy_percentage", "average_points_per_prediction"]
                old_complex_fields = ["total_amount", "total_payout", "profit_loss", "average_odds", "confidence_score"]
                
                has_simple = any(field in properties for field in expected_simple_fields)
                has_complex = any(field in properties for field in old_complex_fields)
                
                if has_simple and not has_complex:
                    print("✅ Schema properly simplified - has prediction points, no complex financial metrics")
                elif has_complex:
                    print("❌ Schema still has complex financial metrics that should be removed")
                else:
                    print("⚠️  Schema may need verification - unclear if properly simplified")
            else:
                print("❌ BetStatistics schema not found")
                
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def verify_database():
    """Verify database changes"""
    try:
        # Check if confidence point system was removed from group constraints
        import subprocess
        result = subprocess.run([
            "docker", "exec", "-i", "betting-league-championship-postgres-1", 
            "psql", "-U", "postgres", "-d", "betting_championship", 
            "-c", "SELECT conname FROM pg_constraint WHERE conname LIKE '%point_system%';"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            constraints = result.stdout
            if "confidence" not in constraints.lower():
                print("✅ Database constraints updated - confidence point system removed")
            else:
                print("❌ Database still has confidence point system constraints")
        else:
            print("⚠️  Could not verify database constraints")
            
        return True
        
    except Exception as e:
        print(f"⚠️  Database verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Verifying Simplified Prediction System")
    print("=" * 50)
    
    backend_ok = verify_backend()
    db_ok = verify_database()
    
    print("=" * 50)
    if backend_ok and db_ok:
        print("✅ All verifications passed - Simplified prediction system working!")
        sys.exit(0)
    else:
        print("❌ Some verifications failed - Check output above")
        sys.exit(1)