#!/usr/bin/env python3
"""
Test the career suggestion API endpoint
"""
import requests
import json

url = "http://localhost:8000/api/agents/simple/career/suggest"

test_data = {
    "student_id": 1,
    "academic": {
        "gpa": 3.8,
        "marks": [95, 92, 88, 90, 85],
        "strengths": ["Mathematics", "Physics", "Computer Science"],
        "stream": "Science"
    },
    "skills": {
        "programming": 8,
        "problem_solving": 8,
        "communication": 7,
        "leadership": 6
    },
    "interests": {
        "technology": "very high",
        "innovation": "high",
        "travel": "medium",
        "business": "medium"
    },
    "preferences": {
        "work_environment": "startup",
        "salary_priority": True,
        "location_preference": "metro_cities",
        "work_life_balance": "important"
    }
}

print("Testing Career Suggestion Endpoint")
print("=" * 50)
print(f"POST {url}")
print(f"\nRequest Data:")
print(json.dumps(test_data, indent=2))

try:
    response = requests.post(url, json=test_data, timeout=120)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Success!")
        print(f"\nResponse Keys: {list(data.keys())}")
        print(f"\nTop Careers: {len(data.get('topCareers', []))} suggestions")
        if data.get('topCareers'):
            print(f"  1. {data['topCareers'][0].get('name')} (Match: {data['topCareers'][0].get('matchPercentage')}%)")
    else:
        print(f"\n✗ Error")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n✗ Failed: {str(e)}")
    print("Make sure the server is running: python -m uvicorn app.main:app --reload")
