"""
Sample Report Generator Script
Demonstrates the Reports app functionality with sample LCA data
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lca_tool.settings')
django.setup()

from reports.utils.pdf import generate_lca_pdf_report, generate_simple_pdf
from reports.utils.excel import generate_lca_excel_report, generate_simple_excel
from reports.utils.csv import generate_lca_csv_report

def create_sample_lca_data():
    """Create comprehensive sample LCA data for testing"""
    
    sample_data = {
        "inputs_used": {
            "material": "aluminum",
            "production_rate": 1000,  # tons
            "energy_use": 5000,       # kWh
            "water_use": 2500,        # liters
            "transport_distance": 500, # km
            "recycling_rate": 0.8,    # 80%
            "renewable_energy_percent": 35.5,
            "waste_generation": 150,   # tons
            "process_temperature": 850 # °C
        },
        
        "predicted_parameters": {
            "emission_factor": 2.1,
            "energy_intensity": 4.8,
            "water_efficiency": 0.92,
            "recovery_rate": 0.87
        },
        
        "overall_assessment": {
            "overall_score": 78.5,
            "overall_rating": "Good",
            "sustainability_index": 72.3,
            "environmental_grade": "B+",
            "improvement_potential": "Medium"
        },
        
        "environmental_impact": {
            "carbon_footprint_total": 2456.8,    # kg CO₂
            "carbon_footprint_production": 1820.2,
            "carbon_footprint_transport": 456.6,
            "carbon_footprint_endoflife": 180.0,
            "water_use_total": 3200,             # liters
            "energy_consumption_total": 5200,    # kWh
            "waste_generated": 145.5,            # kg
            "air_pollution_score": 65.2,
            "water_pollution_score": 72.8,
            "soil_impact_score": 58.9,
            "emission_breakdown": {
                "production": 1820.2,
                "transport": 456.6,
                "processing": 180.0
            }
        },
        
        "circularity_metrics": {
            "circularity_index": 72.3,
            "overall_rating": "Good",
            "recycling_score": 85.2,
            "resource_efficiency": 68.5,
            "material_recovery_rate": 82.1,
            "waste_reduction_potential": 15.3,
            "cmur_analysis": {
                "cmur_percent": 78.5,
                "performance_assessment": "Above Average",
                "target_achievement": "Met",
                "improvement_potential": "Low"
            },
            "waste_analysis": {
                "waste_reduction_percent": 12.5,
                "recycling_efficiency": 88.2,
                "material_loops_closed": 3
            }
        },
        
        "energy_analysis": {
            "energy_efficiency_percent": 75.2,
            "material_efficiency_percent": 82.1,
            "process_intensity": 5.2,           # kWh/ton
            "energy_rating": "Good",
            "renewable_integration": 35.5,      # %
            "energy_recovery": 18.3,            # %
            "thermal_efficiency": 68.9          # %
        },
        
        "transport_analysis": {
            "current_transport_emissions": 456.6,  # kg CO₂
            "recommended_mode": "Rail + Truck",
            "potential_emission_savings": 125.4,   # kg CO₂
            "transport_efficiency": 72.1,          # score
            "distance_optimization": 8.5,          # % reduction possible
            "mode_efficiency": {
                "current": "Truck",
                "recommended": "Rail + Truck",
                "savings_percent": 27.5
            }
        },
        
        "recommendations": [
            {
                "priority": "High",
                "category": "Energy Efficiency",
                "action": "Increase renewable energy usage from 35% to 50%",
                "impact": "Reduce carbon footprint by 12-15%",
                "implementation": "Install solar panels and purchase green energy certificates",
                "cost_estimate": "Medium",
                "timeframe": "6-12 months"
            },
            {
                "priority": "Medium", 
                "category": "Waste Reduction",
                "action": "Implement advanced material recovery systems",
                "impact": "Increase recycling rate from 80% to 90%",
                "implementation": "Upgrade sorting and processing equipment",
                "cost_estimate": "High",
                "timeframe": "12-18 months"
            },
            {
                "priority": "Medium",
                "category": "Transport Optimization",
                "action": "Switch from 100% truck to 70% rail + 30% truck transport",
                "impact": "Reduce transport emissions by 27%",
                "implementation": "Negotiate contracts with rail transport providers",
                "cost_estimate": "Low",
                "timeframe": "3-6 months"
            },
            {
                "priority": "Low",
                "category": "Process Optimization",
                "action": "Optimize process temperature to reduce energy consumption",
                "impact": "Improve energy efficiency by 5-8%",
                "implementation": "Process engineering optimization and equipment upgrade",
                "cost_estimate": "Medium",
                "timeframe": "9-15 months"
            }
        ],
        
        "calculation_metadata": {
            "engine_version": "2.1.5",
            "calculation_timestamp": datetime.now().isoformat(),
            "models_loaded": [
                "environmental_model_20250919",
                "circularity_model_20250919", 
                "classification_model_20250919"
            ],
            "data_quality_score": 87.3,
            "confidence_level": 0.89,
            "validation_status": "Passed"
        }
    }
    
    return sample_data


def generate_sample_reports():
    """Generate sample reports in all formats"""
    
    print("🔄 Creating sample LCA data...")
    sample_lca_data = create_sample_lca_data()
    
    project_name = "Sample Aluminum Production LCA"
    print(f"📊 Generating reports for: {project_name}")
    
    # Create reports directory in current project
    reports_dir = os.path.join(os.getcwd(), "sample_reports")
    os.makedirs(reports_dir, exist_ok=True)
    print(f"📁 Reports will be saved in: {reports_dir}")
    
    reports_generated = []
    
    try:
        # Generate PDF Report
        print("\n📄 Generating PDF report...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"LCA_Report_{project_name.replace(' ', '_')}_{timestamp}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
        
        pdf_path = generate_lca_pdf_report(
            project_name=project_name,
            lca_results=sample_lca_data,
            output_path=pdf_path
        )
        reports_generated.append(("PDF", pdf_path))
        print(f"✅ PDF report generated: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")
    
    try:
        # Generate Excel Report
        print("\n📊 Generating Excel report...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        excel_filename = f"LCA_Report_{project_name.replace(' ', '_')}_{timestamp}.xlsx"
        excel_path = os.path.join(reports_dir, excel_filename)
        
        excel_path = generate_lca_excel_report(
            project_name=project_name,
            lca_results=sample_lca_data,
            output_path=excel_path
        )
        reports_generated.append(("Excel", excel_path))
        print(f"✅ Excel report generated: {excel_path}")
        
    except Exception as e:
        print(f"❌ Error generating Excel report: {e}")
    
    try:
        # Generate CSV Reports (all types)
        csv_types = ["comprehensive", "summary", "detailed"]
        
        for csv_type in csv_types:
            print(f"\n📋 Generating {csv_type} CSV report...")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f"LCA_Report_{project_name.replace(' ', '_')}_{csv_type}_{timestamp}.csv"
            csv_path = os.path.join(reports_dir, csv_filename)
            
            csv_path = generate_lca_csv_report(
                project_name=project_name,
                lca_results=sample_lca_data,
                output_path=csv_path,
                report_type=csv_type
            )
            reports_generated.append((f"CSV ({csv_type})", csv_path))
            print(f"✅ {csv_type.title()} CSV report generated: {csv_path}")
            
    except Exception as e:
        print(f"❌ Error generating CSV reports: {e}")
    
    # Generate simple test reports
    try:
        print("\n🧪 Generating simple test reports...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        simple_pdf_path = os.path.join(reports_dir, f"Simple_PDF_Test_{timestamp}.pdf")
        simple_pdf = generate_simple_pdf(
            project_name="Simple Test Project",
            data={"test_param": "test_value", "score": 85.5},
            output_path=simple_pdf_path
        )
        reports_generated.append(("Simple PDF", simple_pdf))
        print(f"✅ Simple PDF generated: {simple_pdf}")
        
        simple_excel_path = os.path.join(reports_dir, f"Simple_Excel_Test_{timestamp}.xlsx")
        simple_excel = generate_simple_excel(
            project_name="Simple Test Project", 
            data={"test_param": "test_value", "score": 85.5},
            output_path=simple_excel_path
        )
        reports_generated.append(("Simple Excel", simple_excel))
        print(f"✅ Simple Excel generated: {simple_excel}")
        
    except Exception as e:
        print(f"❌ Error generating simple reports: {e}")
    
    # Summary
    print(f"\n🎉 Report Generation Complete!")
    print(f"📈 Total reports generated: {len(reports_generated)}")
    print("\n📋 Generated Reports:")
    print("=" * 80)
    
    for report_type, file_path in reports_generated:
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        file_size_mb = file_size / (1024 * 1024)
        relative_path = os.path.relpath(file_path, os.getcwd())
        print(f"{report_type:20} | {file_size_mb:.2f} MB | {relative_path}")
    
    print(f"\n💡 All reports saved in: {reports_dir}")
    print("💡 Use these reports to test the download functionality via the API")
    
    return reports_generated


def save_sample_data():
    """Save sample LCA data to JSON file for API testing"""
    
    sample_data = create_sample_lca_data()
    
    # Save to file for API testing in current directory
    output_file = os.path.join(os.getcwd(), "sample_lca_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    relative_path = os.path.relpath(output_file, os.getcwd())
    print(f"\n💾 Sample LCA data saved to: {relative_path}")
    print("💡 Use this JSON file to test the Reports API endpoints")
    
    return output_file


def main():
    """Main function to run sample report generation"""
    
    print("🚀 LCA Reports Sample Generator")
    print("=" * 50)
    
    try:
        # Generate sample reports
        reports = generate_sample_reports()
        
        # Save sample data for API testing
        json_file = save_sample_data()
        
        print(f"\n🎯 Sample Generation Summary:")
        print(f"   ✅ {len(reports)} reports generated successfully")
        print(f"   ✅ Sample data saved to {json_file}")
        print(f"   ✅ Ready for API testing!")
        
        print(f"\n📖 Next Steps:")
        print(f"   1. Test the generated reports by opening them")
        print(f"   2. Use the Reports API with the sample JSON data")
        print(f"   3. Test download functionality via the API endpoints")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during sample generation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Sample report generation completed successfully!")
    else:
        print("\n💥 Sample report generation failed!")
        sys.exit(1)