#!/usr/bin/env python3
"""
Test script to verify CrewAI fixes and error handling.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

# Load environment variables
load_dotenv()

def test_basic_functionality():
    """Test basic functionality with a simple job description."""
    print("Testing basic functionality...")
    
    try:
        from src.agents import ColdEmailAgents
        from src.portfolio import Portfolio
        
        # Initialize components
        agents = ColdEmailAgents()
        portfolio = Portfolio()
        
        # Test job description
        job_description = """
        Job Title: AI Automation Engineer
        Location: Remote
        Employment Type: Full-time, Permanent
        Experience Requirement: 4+ years
        
        About the Role:
        We're looking for a dynamic and tech savvy AI Automation Engineer to join our team.
        This role is perfect for someone with a strong foundation in automation, scripting, and cloud technologies.
        
        Required Skills:
        - Python, JavaScript
        - AWS, Azure
        - Automation tools (n8n, make.com, Zapier)
        - Machine Learning
        - Communication skills
        """
        
        # Test job analysis
        print("Testing job analysis...")
        jobs = agents.analyze_jobs(job_description)
        print(f"Found {len(jobs)} jobs")
        
        if jobs:
            job = jobs[0]
            print(f"Job Title: {job.get('role', 'Unknown')}")
            print(f"Experience: {job.get('experience', 'Unknown')}")
            print(f"Skills: {job.get('skills', [])}")
            
            # Test email generation
            print("\nTesting email generation...")
            email_content = agents.generate_cold_email(job, "Sample portfolio data")
            print(f"Email generated: {len(email_content)} characters")
            print(f"Email preview: {email_content[:200]}...")
            
            return True
        else:
            print("No jobs found - this might indicate an issue")
            return False
            
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid input."""
    print("\nTesting error handling...")
    
    try:
        from src.agents import ColdEmailAgents
        
        agents = ColdEmailAgents()
        
        # Test with empty text
        jobs = agents.analyze_jobs("")
        print(f"Empty text result: {len(jobs)} jobs (should be 0)")
        
        # Test with invalid JSON-like text
        jobs = agents.analyze_jobs("This is not a job posting at all")
        print(f"Invalid text result: {len(jobs)} jobs")
        
        return True
        
    except Exception as e:
        print(f"Error handling test failed: {e}")
        return False

def test_workflow():
    """Test the complete workflow."""
    print("\nTesting complete workflow...")
    
    try:
        from src.agents import ColdEmailAgents
        from src.portfolio import Portfolio
        
        agents = ColdEmailAgents()
        portfolio = Portfolio()
        
        job_description = """
        Senior Python Developer
        We need a Python developer with 5+ years experience in Django, Flask, and AWS.
        Must have experience with machine learning and data analysis.
        """
        
        # Test complete workflow
        result = agents.process_complete_workflow(job_description, [])
        
        if isinstance(result, dict):
            print("Workflow completed successfully")
            print(f"Result keys: {list(result.keys())}")
            if 'email_content' in result:
                print(f"Email content length: {len(result['email_content'])}")
        else:
            print(f"Workflow returned: {type(result)}")
            
        return True
        
    except Exception as e:
        print(f"Workflow test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("CrewAI Fix Verification Tests")
    print("=" * 40)
    
    # Check environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("Please set your GROQ_API_KEY in the .env file")
        return False
    
    print("✅ GROQ_API_KEY found")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Error Handling", test_error_handling),
        ("Complete Workflow", test_workflow),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The CrewAI fixes are working.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 