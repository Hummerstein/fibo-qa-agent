#!/usr/bin/env python3
"""
FIBO Directory Scanner
Analyzes your FIBO ontology directory structure and creates realistic module sets
"""

import os
from pathlib import Path
import json
from collections import defaultdict

# Your FIBO directory path
FIBO_PATH = Path("/Users/thudblunder/Documents/fibo_qa_agent/fibo-ontology")

def scan_fibo_directory():
    """Scan the FIBO directory and catalog all RDF files"""
    
    if not FIBO_PATH.exists():
        print(f"❌ FIBO directory not found: {FIBO_PATH}")
        return None
    
    print(f"🔍 Scanning FIBO directory: {FIBO_PATH}")
    print("=" * 60)
    
    # Find all RDF files
    rdf_files = []
    for root, dirs, files in os.walk(FIBO_PATH):
        for file in files:
            if file.endswith(('.rdf', '.owl', '.ttl')):
                rel_path = Path(root).relative_to(FIBO_PATH) / file
                full_path = Path(root) / file
                file_size = full_path.stat().st_size
                
                rdf_files.append({
                    'path': str(rel_path),
                    'full_path': str(full_path),
                    'size': file_size,
                    'size_kb': round(file_size / 1024, 1)
                })
    
    print(f"📊 Found {len(rdf_files)} RDF/OWL files")
    
    # Group by top-level directories
    by_domain = defaultdict(list)
    for file in rdf_files:
        domain = file['path'].split('/')[0] if '/' in file['path'] else 'ROOT'
        by_domain[domain].append(file)
    
    # Display breakdown
    print(f"\n📂 Domain Breakdown:")
    total_size = 0
    for domain, files in sorted(by_domain.items()):
        domain_size = sum(f['size'] for f in files)
        total_size += domain_size
        print(f"  📁 {domain}: {len(files)} files ({domain_size/1024/1024:.1f} MB)")
        
        # Show first few files as examples
        for file in sorted(files, key=lambda x: x['size'], reverse=True)[:3]:
            print(f"     • {file['path']} ({file['size_kb']} KB)")
        
        if len(files) > 3:
            print(f"     ... and {len(files) - 3} more files")
        print()
    
    print(f"💾 Total size: {total_size/1024/1024:.1f} MB")
    
    return rdf_files, by_domain

def analyze_existing_modules():
    """Check which files from your current MODULE_SETS actually exist"""
    
    # Your current module definitions
    MODULE_SETS = {
        "core": [
            "FND/Accounting/AccountingEquity.rdf",
            "FND/OwnershipAndControl/Ownership.rdf",
            "SEC/Equities/EquityInstruments.rdf"
        ],
        "comprehensive": [
            "FND/Accounting/AccountingEquity.rdf",
            "FND/OwnershipAndControl/Ownership.rdf",
            "SEC/Equities/EquityInstruments.rdf",
            "FND/Accounting/CurrencyAmount.rdf",
            "FND/Relations/Relations.rdf",
            "FND/Utilities/Values.rdf",
            "FND/DatesAndTimes/FinancialDates.rdf",
            "SEC/Securities/Securities.rdf",
            "SEC/Securities/SecuritiesIdentification.rdf",
            "SEC/Securities/SecuritiesIssuance.rdf",
            "SEC/Securities/SecuritiesListings.rdf",
            "FBC/FinancialInstruments/FinancialInstruments.rdf",
            "FBC/ProductsAndServices/FinancialProductsAndServices.rdf",
            "FBC/FunctionalEntities/FinancialServicesEntities.rdf",
            "FBC/DebtAndEquities/Debt.rdf",
            "BE/LegalEntities/LegalPersons.rdf"
        ],
        "banking": [
            "FND/Accounting/AccountingEquity.rdf",
            "FND/Accounting/CurrencyAmount.rdf",
            "FBC/FinancialInstruments/FinancialInstruments.rdf",
            "FBC/ProductsAndServices/FinancialProductsAndServices.rdf",
            "FBC/FunctionalEntities/FinancialServicesEntities.rdf",
            "FBC/DebtAndEquities/Debt.rdf"
        ],
        "securities": [
            "SEC/Equities/EquityInstruments.rdf",
            "SEC/Securities/Securities.rdf",
            "SEC/Securities/SecuritiesIdentification.rdf",
            "SEC/Securities/SecuritiesIssuance.rdf",
            "SEC/Securities/SecuritiesListings.rdf",
            "FBC/FinancialInstruments/FinancialInstruments.rdf"
        ]
    }
    
    print("\n🔍 Checking your current MODULE_SETS against actual files:")
    print("=" * 60)
    
    for module_name, files in MODULE_SETS.items():
        print(f"\n📦 {module_name.upper()} module:")
        existing = 0
        missing = 0
        
        for file_path in files:
            full_path = FIBO_PATH / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"  ✅ {file_path} ({size/1024:.1f} KB)")
                existing += 1
            else:
                print(f"  ❌ {file_path} (MISSING)")
                missing += 1
        
        print(f"  📊 Summary: {existing} exist, {missing} missing")
    
    return MODULE_SETS

def suggest_realistic_modules(by_domain):
    """Suggest realistic module sets based on what actually exists"""
    
    print("\n💡 SUGGESTED REALISTIC MODULE SETS:")
    print("=" * 60)
    
    suggestions = {}
    
    # Core - just what you know works
    if 'FND' in by_domain:
        fnd_files = [f['path'] for f in by_domain['FND']]
        accounting_files = [f for f in fnd_files if 'Accounting' in f]
        
        if accounting_files:
            suggestions['minimal'] = {
                'name': 'Minimal Working Set',
                'files': accounting_files[:1]  # Just one file that works
            }
    
    # Build suggestions based on what exists
    for domain, files in by_domain.items():
        if len(files) >= 2:  # Only suggest domains with multiple files
            suggestions[domain.lower()] = {
                'name': f'{domain} Domain',
                'files': [f['path'] for f in files[:5]]  # Max 5 files per domain
            }
    
    # Print suggestions
    for name, info in suggestions.items():
        print(f"\n📦 {name}:")
        print(f"   Name: {info['name']}")
        print(f"   Files ({len(info['files'])}):")
        for file in info['files']:
            print(f"     • {file}")
    
    return suggestions

def generate_working_module_sets(suggestions):
    """Generate Python code for working MODULE_SETS"""
    
    print(f"\n🔧 WORKING MODULE_SETS CODE:")
    print("=" * 60)
    print("# Replace your MODULE_SETS in ontology_tools.py with this:")
    print()
    print("MODULE_SETS = {")
    
    for name, info in suggestions.items():
        print(f'    "{name}": {{')
        print(f'        "name": "{info["name"]}",')
        print(f'        "modules": [')
        for file in info['files']:
            print(f'            "{file}",')
        print('        ]')
        print('    },')
    
    print("}")

def save_scan_results(rdf_files, by_domain, suggestions):
    """Save scan results to JSON file"""
    
    results = {
        'scan_timestamp': str(Path.cwd()),
        'total_files': len(rdf_files),
        'total_size_mb': sum(f['size'] for f in rdf_files) / 1024 / 1024,
        'by_domain': {domain: len(files) for domain, files in by_domain.items()},
        'all_files': rdf_files,
        'suggested_modules': suggestions
    }
    
    output_file = 'fibo_scan_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")

def main():
    """Main scanner function"""
    print("🧪 FIBO Directory Scanner")
    print("This will analyze your actual FIBO files and suggest working module sets")
    print()
    
    # Scan directory
    rdf_files, by_domain = scan_fibo_directory()
    
    if not rdf_files:
        print("No RDF files found. Check your FIBO_PATH.")
        return
    
    # Check existing modules
    analyze_existing_modules()
    
    # Suggest realistic modules
    suggestions = suggest_realistic_modules(by_domain)
    
    # Generate code
    generate_working_module_sets(suggestions)
    
    # Save results
    save_scan_results(rdf_files, by_domain, suggestions)
    
    print(f"\n✅ Scan complete! You now know exactly what FIBO files you have.")

if __name__ == "__main__":
    main()