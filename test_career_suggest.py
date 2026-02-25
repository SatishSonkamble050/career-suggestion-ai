"""Test script for career suggest endpoint"""
import requests
import json
import time

# Wait a moment for any server changes to take effect
time.sleep(2)

# Test the career suggest endpoint
url = "http://localhost:8000/api/agents/simple/career/suggest"

test_data = {
    "student_id": 1,
    "academic": {
        "gpa": 3.8,
        "mathsScore": 95,
        "english_score": 88,
        "overall_performance": "excellent"
    },
    "skills": {
        "python": "advanced",
        "data_analysis": "intermediate"
    },
    "interests": {
        "data_science": True,
        "technology": True,
        "analytics": True
    },
    "preferences": {
        "location": "any",
        "industry": "tech"
    }
}

try:
    print("Sending request to:", url)
    print("With data:", json.dumps(test_data, indent=2))
    print("\n" + "="*80 + "\n")
    
    response = requests.post(url, json=test_data, timeout=60)
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print("\nResponse:")
    
    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, indent=2)[:2000])  # Print first 2000 chars
        print("\n✓ SUCCESS! Endpoint returned valid response with status 200")
    else:
        print(response.text[:1000])
        print(f"\n✗ ERROR: Status code {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Cannot connect to http://localhost:8000")
    print("Make sure the server is running with: python -m uvicorn app.main:app --reload")
except Exception as e:
    print(f"✗ ERROR: {str(e)}")
