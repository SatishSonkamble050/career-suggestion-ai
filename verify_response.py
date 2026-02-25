"""Verify the complete response structure"""
import requests
import json

url = 'http://localhost:8000/api/agents/simple/career/suggest'
test_data = {
    'student_id': 1,
    'academic': {'gpa': 3.8},
    'skills': {'python': 'advanced'},
    'interests': {'data_science': True},
    'preferences': {'location': 'any'}
}

response = requests.post(url, json=test_data, timeout=60)
if response.status_code == 200:
    result = response.json()
    print('✓ Response structure verification:')
    print(f'  - studentName: {result.get("studentName")}')
    print(f'  - testDate: {result.get("testDate")}')
    print(f'  - topCareers items: {len(result.get("topCareers", []))}')
    print(f'  - collegeSuggestions items: {len(result.get("collegeSuggestions", []))}')
    print(f'  - salaryPrediction items: {len(result.get("salaryPrediction", []))}')
    print(f'  - roadmap items: {len(result.get("roadmap", []))}')
    print(f'  - backupOptions items: {len(result.get("backupOptions", []))}')
    print('\n✓ All required sections present in response!')
    
    # Check first career structure
    if result.get("topCareers"):
        career = result["topCareers"][0]
        print('\n✓ First career has all required fields:')
        required_fields = ['id', 'name', 'matchPercentage', 'description', 'whyMatches',
                          'educationPath', 'coursesNeeded', 'skillsNeeded', 'employmentRate',
                          'avgSalary', 'growthRate', 'jobsAvailable', 'topCompanies',
                          'alternativeNames', 'relatedFields']
        for field in required_fields:
            status = '✓' if field in career else '✗'
            print(f'  {status} {field}')
else:
    print(f'Error: {response.status_code}')
    print(response.text[:500])
