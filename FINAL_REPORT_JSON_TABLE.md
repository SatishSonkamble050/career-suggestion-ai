# Career Guidance Report JSON Structure

## Complete Response Table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `student_id` | `int` | Unique student identifier | `1` |
| `academic_analysis` | `Dict[str, Any]` | Analysis of academic profile | See below |
| `skill_analysis` | `Dict[str, Any]` | Analysis of skills | See below |
| `interest_analysis` | `Dict[str, Any]` | Analysis of interests | See below |
| `preference_analysis` | `Dict[str, Any]` | Analysis of preferences | See below |
| `market_analysis` | `Dict[str, Any]` | Analysis of job market | See below |
| `final_report` | `string` | Comprehensive career guidance report | See below |

---

## Final Report Structure (String)

The `final_report` field contains a formatted text report with the following sections:

### 1. Summary Section
```
Summary: [2-3 sentence overview of student profile and recommendations]
```

| Section | Type | Content |
|---------|------|---------|
| Summary | String | Overview of student profile and key recommendations (2-3 sentences) |

**Example**:
```
John demonstrates exceptional aptitude in mathematics and computer science with a 3.8 GPA 
and expert-level Python skills. His strong interest in AI/Machine Learning aligns perfectly 
with current market demand, positioning him for high-paying technical roles.
```

---

### 2. Top 3 Recommended Careers

```
Top 3 Recommended Careers:
1. [Career 1]
2. [Career 2]
3. [Career 3]
```

| Position | Type | Content |
|----------|------|---------|
| Career 1 | String | First recommended career path |
| Career 2 | String | Second recommended career path |
| Career 3 | String | Third recommended career path |

**Example**:
```
Top 3 Recommended Careers:
1. Machine Learning Engineer
2. Data Scientist
3. AI Research Scientist
```

---

### 3. Career Fit Analysis

For each of the 3 recommended careers:

```
Why [Career X] fits:
[2 sentences explaining alignment between student profile and career]
```

| Career | Type | Content |
|--------|------|---------|
| Career 1 Fit | String | 2+ sentences explaining why Career 1 fits |
| Career 2 Fit | String | 2+ sentences explaining why Career 2 fits |
| Career 3 Fit | String | 2+ sentences explaining why Career 3 fits |

**Example for Career 1**:
```
Why Machine Learning Engineer fits:
Your strong foundation in mathematics and advanced Python skills directly align with 
the technical requirements of ML engineering roles. The high market demand for ML Engineers 
(often paying $150k-250k+) combined with your demonstrated passion for AI makes this role 
an excellent fit for your career trajectory.
```

---

### 4. Required Skills to Develop

```
Required Skills to Develop:
- [Skill 1]: [Description/priority]
- [Skill 2]: [Description/priority]
- [Skill 3]: [Description/priority]
...
```

| Item | Type | Content |
|------|------|---------|
| Skill 1 | String | High-priority skill with reason |
| Skill 2 | String | High-priority skill with reason |
| Skill 3 | String | Additional skill recommendation |
| ... | String | More skills as needed |

**Example**:
```
Required Skills to Develop:
- Advanced Statistics: Critical for ML model evaluation and statistical testing
- Deep Learning Frameworks: Essential for modern AI projects (TensorFlow, PyTorch)
- System Design: Important for production ML pipeline architecture
- Cloud Platforms (AWS/GCP): Industry standard for deploying ML models
- Communication Skills: Important for team collaboration and presenting findings
```

---

### 5. 12-Month Action Plan

```
12-Month Action Plan:

Quarter 1 (Months 1-3):
- [Action 1]
- [Action 2]
- [Action 3]

Quarter 2 (Months 4-6):
- [Action 1]
- [Action 2]
- [Action 3]

Quarter 3 (Months 7-9):
- [Action 1]
- [Action 2]
- [Action 3]

Quarter 4 (Months 10-12):
- [Action 1]
- [Action 2]
- [Action 3]
```

| Quarter | Type | Content |
|---------|------|---------|
| Q1 (Months 1-3) | String | Foundational skills and knowledge building |
| Q2 (Months 4-6) | String | Project work and practical experience |
| Q3 (Months 7-9) | String | Advanced learning and portfolio building |
| Q4 (Months 10-12) | String | Internship/job search preparation |

**Example**:
```
12-Month Action Plan:

Quarter 1 (Months 1-3):
- Complete advanced machine learning course (Coursera or Fast.ai)
- Learn TensorFlow and PyTorch through practical projects
- Build 2-3 portfolio projects using ML algorithms

Quarter 2 (Months 4-6):
- Participate in Kaggle competitions to enhance competitive skills
- Study cloud platforms (AWS SageMaker or Google Cloud ML)
- Read research papers and implement state-of-the-art algorithms

Quarter 3 (Months 7-9):
- Contribute to open-source ML projects on GitHub
- Build end-to-end ML pipeline project for portfolio
- Network with ML professionals at conferences/meetups

Quarter 4 (Months 10-12):
- Prepare for technical interviews for ML engineer roles
- Apply for ML internships or entry-level engineer positions
- Continue portfolio enhancement based on job market feedback
```

---

### 6. Next Steps

```
Next Steps:
1. [Immediate action]
2. [Short-term goal]
3. [Medium-term goal]
4. [Long-term goal]
```

| Step | Type | Content |
|------|------|---------|
| Step 1 | String | Immediate action (this week) |
| Step 2 | String | Short-term goal (1-3 months) |
| Step 3 | String | Medium-term goal (3-6 months) |
| Step 4 | String | Long-term goal (6-12 months) |

**Example**:
```
Next Steps:
1. Enroll in advanced machine learning course by end of this week
2. Complete your first ML portfolio project within 2 months
3. Achieve top 10% ranking in Kaggle competitions within 6 months
4. Secure ML internship or junior engineer role within 12 months
```

---

## Complete Example Final Report

```
Summary: 
John demonstrates exceptional aptitude in mathematics and computer science with a 3.8 GPA 
and expert-level Python skills. His strong interest in AI/Machine Learning aligns perfectly 
with current market demand, positioning him for high-paying technical roles with excellent 
growth potential.

Top 3 Recommended Careers:
1. Machine Learning Engineer
2. Data Scientist
3. AI Research Scientist

Why Machine Learning Engineer fits:
Your strong foundation in mathematics and advanced Python skills directly align with the 
technical requirements of ML engineering roles. The high market demand for ML Engineers 
(often paying $150k-250k+) combined with your demonstrated passion for AI makes this role 
an excellent fit for your career trajectory.

Why Data Scientist fits:
Your statistical knowledge, strong programming skills, and interest in AI position you 
well for data science roles. These positions offer competitive salaries ($120k-180k) and 
are abundant in tech and finance industries where you've expressed interest.

Why AI Research Scientist fits:
Your academic excellence and passion for cutting-edge technology make research roles appealing. 
This path typically requires graduate studies but offers the opportunity to work on 
groundbreaking AI innovations at leading research labs or tech companies.

Required Skills to Develop:
- Advanced Statistics: Critical for ML model evaluation and statistical testing
- Deep Learning Frameworks: Essential for modern AI projects (TensorFlow, PyTorch)
- System Design: Important for production ML pipeline architecture and scalability
- Cloud Platforms (AWS/GCP): Industry standard for deploying ML models at scale
- SQL and Data Engineering: Important for working with large datasets
- Communication Skills: Essential for team collaboration and presenting findings

12-Month Action Plan:

Quarter 1 (Months 1-3):
- Enroll in Advanced Machine Learning course on Coursera or Fast.ai
- Learn TensorFlow and PyTorch through hands-on projects
- Build 2-3 portfolio projects implementing key ML algorithms
- Start contributing to ML-related open-source projects

Quarter 2 (Months 4-6):
- Participate actively in 3-4 Kaggle competitions
- Learn cloud ML platforms (AWS SageMaker or Google Cloud ML)
- Study deep learning architectures (CNNs, RNNs, Transformers)
- Read and implement papers from top ML conferences (NeurIPS, ICML)

Quarter 3 (Months 7-9):
- Contribute meaningfully to 1-2 popular open-source ML projects
- Build end-to-end ML pipeline project for your portfolio
- Network with ML professionals at tech conferences or meetups
- Begin freelancing or consulting on ML projects for experience

Quarter 4 (Months 10-12):
- Prepare intensively for technical ML interview questions
- Apply for ML engineer internships or junior positions
- Refine portfolio based on market feedback and trending technologies
- Secure a position and plan continued learning

Next Steps:
1. Register for an advanced ML course this week and complete the first module
2. Build your first portfolio project on a real dataset within 30 days
3. Reach top 25% in Kaggle competitions within 3 months
4. Land your first ML engineering role or internship within 12 months
```

---

## Alternative Report Sections

Depending on student profile, additional sections might include:

| Optional Section | Type | When Included |
|------------------|------|---------------|
| `Salary Expectations` | String | When career preferences include salary range |
| `Geographic Considerations` | String | When location preferences are specified |
| `Work-Life Balance` | String | When work style preferences are mentioned |
| `Further Education` | String | When pursuing advanced roles like research |
| `Risk Factors` | String | When career path has challenges |
| `Industry Trends` | String | When job market is volatile |

---

## Report Field Mapping

### Mapping to Source Analyses

| Report Section | Contains Info From | Format |
|----------------|-------------------|--------|
| Summary | All analyses | Synthesized text |
| Recommended Careers | Market + Interest + Preference | List + descriptions |
| Career Fit Analysis | All analyses | Narrative text |
| Required Skills | Skill + Interest + Market analyses | Bulleted list |
| Action Plan | Academic + Preference + Market analyses | Quarterly breakdown |
| Next Steps | All analyses | Sequential checklist |

---

## Data Types Reference

```python
{
    "student_id": int,                      # e.g., 1
    "academic_analysis": {                  # Dictionary
        "strengths": ["str"],               # List of strings
        "areas_for_improvement": ["str"],   # List of strings
        "gpa_analysis": "str",              # String description
        "subject_recommendations": ["str"]  # List of strings
    },
    "skill_analysis": {                     # Dictionary
        "current_skills": ["str"],          # List of strings
        "proficiency_level": "str",         # String (Advanced, Expert, etc)
        "skill_gaps": ["str"],              # List of strings
        "in_demand_skills": ["str"]         # List of strings
    },
    "interest_analysis": {                  # Dictionary
        "interest_clusters": ["str"],       # List of strings
        "preferred_industries": ["str"],    # List of strings
        "career_directions": ["str"],       # List of strings
        "passion_areas": ["str"]            # List of strings
    },
    "preference_analysis": {                # Dictionary
        "work_environment": "str",          # String description
        "salary_expectations": "str",       # String range (e.g., "100k-150k")
        "work_life_balance": "str",         # String preference
        "career_growth": "str",             # String goal
        "location_preferences": "str"       # String location
    },
    "market_analysis": {                    # Dictionary
        "in_demand_roles": ["str"],         # List of job titles
        "emerging_fields": ["str"],         # List of fields
        "salary_outlook": "str",            # String with range
        "growth_trends": ["str"],           # List of trends
        "timing_recommendation": "str"      # String timing advice
    },
    "final_report": "str"                   # Complete formatted report as string
}
```

---

## Report Characteristics

| Aspect | Details |
|--------|---------|
| **Format** | Plain text with section headers |
| **Length** | 1,500-3,000 words |
| **Tone** | Professional, encouraging, actionable |
| **Content** | Career guidance specific to student profile |
| **Structure** | Summary → Recommendations → Analysis → Plan → Action |
| **Readability** | Organized by sections with clear headings |
| **Personalization** | Based on all 5 previous analyses |

---

## Extracting Report Sections Programmatically

```python
import re

def extract_report_sections(final_report: str) -> dict:
    """Extract sections from final report"""
    sections = {}
    
    # Extract Summary
    summary = re.search(r'Summary:\s*(.+?)(?=Top|Why|Required)', final_report, re.DOTALL)
    if summary:
        sections['summary'] = summary.group(1).strip()
    
    # Extract Careers
    careers = re.findall(r'^\d+\.\s*(.+)$', final_report, re.MULTILINE)
    sections['careers'] = careers[:3]  # First 3 careers
    
    # Extract Required Skills
    skills = re.findall(r'-\s*(.+?):', final_report)
    sections['required_skills'] = skills
    
    # Extract Quarters
    quarters = re.findall(r'Quarter \d+.*?(?=Quarter|\Z)', final_report, re.DOTALL)
    sections['action_plan'] = quarters
    
    # Extract Next Steps
    steps = re.findall(r'^\d+\.\s*(.+)$', final_report[final_report.find('Next Steps'):], re.MULTILINE)
    sections['next_steps'] = steps
    
    return sections

# Usage
report = workflow_response["final_report"]
sections = extract_report_sections(report)
print(sections['summary'])
print(sections['careers'])
```

---

## JSON Export Example

If you want to convert final_report to JSON:

```python
import json

def parse_report_to_json(final_report: str) -> dict:
    """Convert plain text report to JSON structure"""
    return {
        "type": "career_guidance_report",
        "version": "1.0",
        "sections": {
            "summary": extract_summary(final_report),
            "recommended_careers": extract_careers(final_report),
            "career_fit_analysis": extract_fit_analysis(final_report),
            "required_skills": extract_skills(final_report),
            "action_plan": extract_action_plan(final_report),
            "next_steps": extract_next_steps(final_report)
        },
        "raw_text": final_report
    }
```

---

## Report Customization

The report sections and content vary based on:

| Factor | Impact |
|--------|--------|
| GPA | Affects recommendations |
| Skills | Influences career suggestions |
| Interests | Drives career direction |
| Preferences | Shapes salary/location recommendations |
| Market Data | Provides timing and trend insights |

---

**Report Generation**: LLM (ChatOpenAI) | **Format**: Unstructured String | **Length**: ~2000 words average

**Last Updated**: February 21, 2026
