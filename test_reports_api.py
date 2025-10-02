"""
Reports API Test Script
Demonstrates how to use the Reports API endpoints with sample data
"""

import requests
import json
import os
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000/api"
REPORTS_API = f"{BASE_URL}/reports"

def load_sample_data():
    """Load sample LCA data from JSON file"""
    
    try:
        with open('sample_lca_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Sample LCA data file not found. Run generate_sample_reports.py first.")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing sample data: {e}")
        return None


def get_auth_token():
    """Get authentication token (you'll need to implement this based on your auth system)"""
    
    # This is a placeholder - replace with your actual authentication logic
    print("⚠️  Authentication token needed for API calls")
    print("💡 You'll need to:")
    print("   1. Create a user account via Django admin or API")
    print("   2. Get JWT token via /api/auth/login/ endpoint") 
    print("   3. Replace this function with actual token retrieval")
    
    # For testing, return a placeholder
    token = input("Enter your JWT token (or press Enter to continue with demo): ").strip()
    return token if token else "your-jwt-token-here"


def test_generate_pdf_report(sample_data, auth_token):
    """Test PDF report generation"""
    
    print("\n📄 Testing PDF Report Generation...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "lca_results": sample_data,
        "format": "pdf",
        "project_name": "Test PDF Report via API",
        "options": {
            "include_charts": True,
            "include_recommendations": True
        }
    }
    
    try:
        response = requests.post(f"{REPORTS_API}/generate/", 
                               json=payload, 
                               headers=headers,
                               timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ PDF report generated successfully!")
            print(f"   Report ID: {result.get('report_id')}")
            print(f"   Download URL: {result.get('download_url')}")
            print(f"   File Size: {result.get('file_size')} bytes")
            return result
        else:
            print(f"❌ PDF generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_generate_excel_report(sample_data, auth_token):
    """Test Excel report generation"""
    
    print("\n📊 Testing Excel Report Generation...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "lca_results": sample_data,
        "format": "excel",
        "project_name": "Test Excel Report via API",
        "options": {
            "include_charts": True,
            "include_recommendations": True
        }
    }
    
    try:
        response = requests.post(f"{REPORTS_API}/generate/", 
                               json=payload, 
                               headers=headers,
                               timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Excel report generated successfully!")
            print(f"   Report ID: {result.get('report_id')}")
            print(f"   Download URL: {result.get('download_url')}")
            print(f"   File Size: {result.get('file_size')} bytes")
            return result
        else:
            print(f"❌ Excel generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_generate_csv_report(sample_data, auth_token):
    """Test CSV report generation"""
    
    print("\n📋 Testing CSV Report Generation...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "lca_results": sample_data,
        "format": "csv",
        "project_name": "Test CSV Report via API",
        "options": {
            "csv_type": "comprehensive"
        }
    }
    
    try:
        response = requests.post(f"{REPORTS_API}/generate/", 
                               json=payload, 
                               headers=headers,
                               timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ CSV report generated successfully!")
            print(f"   Report ID: {result.get('report_id')}")
            print(f"   Download URL: {result.get('download_url')}")
            print(f"   File Size: {result.get('file_size')} bytes")
            return result
        else:
            print(f"❌ CSV generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_comparative_report(sample_data, auth_token):
    """Test comparative report generation"""
    
    print("\n🔄 Testing Comparative Report Generation...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # Create variations of the sample data for comparison
    project_a = sample_data.copy()
    project_b = sample_data.copy()
    project_c = sample_data.copy()
    
    # Modify some values for comparison
    project_b['overall_assessment']['overall_score'] = 85.2
    project_b['environmental_impact']['carbon_footprint_total'] = 2100.5
    
    project_c['overall_assessment']['overall_score'] = 65.8
    project_c['environmental_impact']['carbon_footprint_total'] = 2800.3
    
    payload = {
        "projects_data": {
            "Aluminum Project A": project_a,
            "Aluminum Project B": project_b,
            "Aluminum Project C": project_c
        },
        "format": "excel",
        "report_title": "LCA Comparative Analysis - Test Projects",
        "options": {}
    }
    
    try:
        response = requests.post(f"{REPORTS_API}/generate/comparative/", 
                               json=payload, 
                               headers=headers,
                               timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Comparative report generated successfully!")
            print(f"   Report ID: {result.get('report_id')}")
            print(f"   Download URL: {result.get('download_url')}")
            print(f"   Projects Compared: {result.get('projects_compared')}")
            return result
        else:
            print(f"❌ Comparative report generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_reports_summary(auth_token):
    """Test user reports summary endpoint"""
    
    print("\n📈 Testing Reports Summary...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{REPORTS_API}/summary/", 
                              headers=headers,
                              timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Reports summary retrieved successfully!")
            print(f"   Total Reports: {result.get('total_reports')}")
            print(f"   By Format: {result.get('by_format')}")
            print(f"   Total Downloads: {result.get('total_downloads')}")
            print(f"   Total File Size: {result.get('total_file_size_mb')} MB")
            return result
        else:
            print(f"❌ Summary retrieval failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_preview_data(sample_data, auth_token):
    """Test report data preview endpoint"""
    
    print("\n👁️ Testing Report Data Preview...")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "lca_results": sample_data
    }
    
    try:
        response = requests.post(f"{REPORTS_API}/preview/", 
                               json=payload, 
                               headers=headers,
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Preview data retrieved successfully!")
            print(f"   Project Info: {result.get('project_info')}")
            print(f"   Key Metrics: {result.get('key_metrics')}")
            print(f"   Data Sections: {len(result.get('data_sections', []))}")
            print(f"   Recommendations: {result.get('recommendations_count')}")
            return result
        else:
            print(f"❌ Preview failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main function to run API tests"""
    
    print("🚀 Reports API Test Suite")
    print("=" * 50)
    
    # Load sample data
    print("📂 Loading sample LCA data...")
    sample_data = load_sample_data()
    if not sample_data:
        return False
    
    print("✅ Sample data loaded successfully!")
    
    # Get authentication token
    auth_token = get_auth_token()
    
    # Test results tracking
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Preview data
    if test_preview_data(sample_data, auth_token):
        tests_passed += 1
    
    # Test 2: Generate PDF report
    if test_generate_pdf_report(sample_data, auth_token):
        tests_passed += 1
    
    # Test 3: Generate Excel report
    if test_generate_excel_report(sample_data, auth_token):
        tests_passed += 1
    
    # Test 4: Generate CSV report
    if test_generate_csv_report(sample_data, auth_token):
        tests_passed += 1
    
    # Test 5: Generate comparative report
    if test_comparative_report(sample_data, auth_token):
        tests_passed += 1
    
    # Test 6: Get reports summary
    if test_reports_summary(auth_token):
        tests_passed += 1
    
    # Summary
    print(f"\n🎯 Test Results Summary:")
    print(f"   ✅ {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Reports API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    print(f"\n📖 Next Steps:")
    print(f"   1. Start Django server: python manage.py runserver")
    print(f"   2. Create user account and get JWT token")
    print(f"   3. Run this test script with valid authentication")
    print(f"   4. Check generated reports in the Django admin or API")
    
    return tests_passed == total_tests


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 API testing completed successfully!")
    else:
        print("\n💥 Some API tests failed!")
