#!/usr/bin/env python3
"""
FIBO Ontology Agent Test Battery - ENHANCED WITH MULTI-STEP REASONING
Comprehensive test coverage with persistent menu system
"""

import json
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from planner import run_natural_language_query

@dataclass
class TestCase:
    """Individual test case"""
    name: str
    query: str
    expected_function: str
    expected_arguments: List[str]
    should_contain: List[str] = None
    should_not_contain: List[str] = None
    category: str = "general"

@dataclass
class TestResult:
    """Test execution result"""
    test_case: TestCase
    success: bool
    actual_response: str
    execution_time: float
    error_message: Optional[str] = None

class FIBOTestBattery:
    """Comprehensive test battery for FIBO ontology agent"""
    
    def __init__(self):
        self.test_cases = self._create_test_cases()
        self.results: List[TestResult] = []
    
    def _create_test_cases(self) -> List[TestCase]:
        """Create test cases based on ACTUAL ontology content"""
        
        # 1. BASIC FUNCTION COVERAGE TESTS
        basic_tests = [
            TestCase(
                name="Basic Class Explanation",
                query="explain PaidInCapital",
                expected_function="explain_class",
                expected_arguments=["PaidInCapital"],
                should_contain=["PaidInCapital", "paid-in capital"],
                category="basic_functions"
            ),
            TestCase(
                name="Superclass Query",
                query="what are the parents of CapitalSurplus",
                expected_function="get_superclasses",
                expected_arguments=["CapitalSurplus"],
                should_contain=["PaidInCapital", "Superclasses"],
                category="basic_functions"
            ),
            TestCase(
                name="Subclass Query",
                query="what are the subclasses of PaidInCapital",
                expected_function="get_subclasses",
                expected_arguments=["PaidInCapital"],
                should_contain=["CapitalSurplus", "Subclasses"],
                category="basic_functions"
            ),
            TestCase(
                name="Properties Query",
                query="what properties does Income have",
                expected_function="get_properties",
                expected_arguments=["Income"],
                should_contain=["Properties", "Income"],
                category="basic_functions"
            ),
            TestCase(
                name="Class List Query",
                query="what classes are available",
                expected_function="list_classes",
                expected_arguments=[],
                should_contain=["PaidInCapital", "OwnersEquity"],
                category="basic_functions"
            ),
        ]
        
        # 2. ENHANCED FUNCTION TESTS
        enhanced_tests = [
            TestCase(
                name="Keyword Search - Equity",
                query="search for equity concepts",
                expected_function="search_classes_by_keyword",
                expected_arguments=["equity"],
                should_contain=["ShareholdersEquity", "OwnersEquity", "Found"],
                category="enhanced_functions"
            ),
            TestCase(
                name="Keyword Search - Capital", 
                query="find classes containing capital",
                expected_function="search_classes_by_keyword",
                expected_arguments=["capital"],
                should_contain=["PaidInCapital", "CapitalSurplus", "Found"],
                category="enhanced_functions"
            ),
            TestCase(
                name="Related Concepts",
                query="what concepts are related to PaidInCapital",
                expected_function="get_related_concepts",
                expected_arguments=["PaidInCapital"],
                should_contain=["Related concepts", "PaidInCapital"],
                category="enhanced_functions"
            ),
            TestCase(
                name="Relationship Explanation",
                query="how are PaidInCapital and CapitalSurplus related",
                expected_function="explain_relationship",
                expected_arguments=["PaidInCapital", "CapitalSurplus"],
                should_contain=["Relationships", "PaidInCapital", "CapitalSurplus"],
                category="enhanced_functions"
            ),
            TestCase(
                name="Ontology Statistics",
                query="show me ontology statistics",
                expected_function="get_ontology_stats",
                expected_arguments=[],
                should_contain=["Classes:", "Properties:", "modules"],
                category="enhanced_functions"
            ),
        ]
        
        # 3. FIBO CONTENT TESTS
        fibo_content_tests = [
            TestCase(
                name="Shareholders Equity Concept",
                query="explain ShareholdersEquity",
                expected_function="explain_class",
                expected_arguments=["ShareholdersEquity"],
                should_contain=["ShareholdersEquity", "equity"],
                category="fibo_content"
            ),
            TestCase(
                name="Retained Earnings",
                query="tell me about RetainedEarnings",
                expected_function="explain_class",
                expected_arguments=["RetainedEarnings"],
                should_contain=["RetainedEarnings", "earnings"],
                category="fibo_content"
            ),
            TestCase(
                name="EBITDA Concept",
                query="what is EarningsBeforeInterestTaxesDepreciationAmortization",
                expected_function="explain_class",
                expected_arguments=["EarningsBeforeInterestTaxesDepreciationAmortization"],
                should_contain=["EarningsBeforeInterestTaxesDepreciationAmortization"],
                category="fibo_content"
            ),
            TestCase(
                name="Asset Types",
                query="what are the subclasses of FinancialAsset",
                expected_function="get_subclasses",
                expected_arguments=["FinancialAsset"],
                should_contain=["FinancialAsset"],
                category="fibo_content"
            ),
            TestCase(
                name="Income Explanation",
                query="explain Income",
                expected_function="explain_class",
                expected_arguments=["Income"],
                should_contain=["Income", "MonetaryAmount"],
                category="fibo_content"
            ),
        ]
        
        # 4. NATURAL LANGUAGE VARIATION TESTS
        nl_variation_tests = [
            TestCase(
                name="Casual Language - Parents",
                query="who is the parent of RetainedEarnings?",
                expected_function="get_superclasses",
                expected_arguments=["RetainedEarnings"],
                should_contain=["OwnersEquity", "Superclasses"],
                category="natural_language"
            ),
            TestCase(
                name="Formal Language - Inheritance",
                query="What are the superclasses of the PaidInCapital class?",
                expected_function="get_superclasses",
                expected_arguments=["PaidInCapital"],
                should_contain=["OwnersEquity", "Superclasses"],
                category="natural_language"
            ),
            TestCase(
                name="Question Variation - Definition",
                query="Could you define CapitalSurplus for me?",
                expected_function="explain_class",
                expected_arguments=["CapitalSurplus"],
                should_contain=["CapitalSurplus", "capital"],
                category="natural_language"
            ),
            TestCase(
                name="Search Request",
                query="I'm looking for asset types",
                expected_function="search_classes_by_keyword",
                expected_arguments=["asset"],
                should_contain=["FinancialAsset", "PhysicalAsset", "Found"],
                category="natural_language"
            ),
        ]
        
        # 5. ERROR HANDLING TESTS
        error_tests = [
            TestCase(
                name="Non-existent Class",
                query="explain NonExistentClass",
                expected_function="explain_class",
                expected_arguments=["NonExistentClass"],
                should_contain=["not found"],
                category="error_handling"
            ),
            TestCase(
                name="Empty Search",
                query="search for xyz123nonexistent",
                expected_function="search_classes_by_keyword",
                expected_arguments=["xyz123nonexistent"],
                should_contain=["No classes found"],
                category="error_handling"
            ),
            TestCase(
                name="Completely Invalid Class Name",
                query="explain XYZ999Invalid",
                expected_function="explain_class",
                expected_arguments=["XYZ999Invalid"],
                should_contain=["not found"],
                category="error_handling"
            ),
        ]
        
        # 6. CASE SENSITIVITY AND EDGE CASES
        edge_case_tests = [
            TestCase(
                name="Case Insensitive Match",
                query="explain paidincapital",
                expected_function="explain_class",
                expected_arguments=["paidincapital"],
                should_contain=["PaidInCapital"],
                category="edge_cases"
            ),
            TestCase(
                name="Mixed Case Query",
                query="explain OWNERSequity",
                expected_function="explain_class",
                expected_arguments=["OWNERSequity"],
                should_contain=["OwnersEquity"],
                category="edge_cases"
            ),
        ]
        
        # 7. OWL REASONING TESTS
        owl_reasoning_tests = [
            TestCase(
                name="OWL Transitive Closure",
                query="show complete inheritance of CapitalSurplus",
                expected_function="get_all_superclasses",
                expected_arguments=["CapitalSurplus"],
                should_contain=["Complete inheritance chain", "OWL Transitive Closure", "PaidInCapital"],
                category="owl_reasoning"
            ),
            TestCase(
                name="OWL Property Inheritance",
                query="what properties does PaidInCapital inherit",
                expected_function="get_inferred_properties", 
                expected_arguments=["PaidInCapital"],
                should_contain=["Property Inheritance", "OWL Inference"],
                category="owl_reasoning"
            ),
            TestCase(
                name="OWL Reasoning Chain",
                query="show reasoning chain between CapitalSurplus and OwnersEquity",
                expected_function="get_reasoning_chain",
                expected_arguments=["CapitalSurplus", "OwnersEquity"],
                should_contain=["OWL Reasoning Chain", "IS-A", "inheritance"],
                category="owl_reasoning"
            ),
            TestCase(
                name="OWL Inheritance - Multiple Levels",
                query="what is the complete inheritance of RetainedEarnings",
                expected_function="get_all_superclasses",
                expected_arguments=["RetainedEarnings"],
                should_contain=["inheritance chain", "OwnersEquity"],
                category="owl_reasoning"
            ),
        ]
        
        # 8. FUZZY MATCHING TESTS
        fuzzy_matching_tests = [
            TestCase(
                name="Fuzzy Matching - Typo Correction",
                query="explain PaidInCapit",
                expected_function="explain_class", 
                expected_arguments=["PaidInCapit"],
                should_contain=["PaidInCapital", "paid-in capital"],
                category="fuzzy_matching"
            ),
            TestCase(
                name="Fuzzy Matching - Partial Name",
                query="tell me about ShareholderEquity",
                expected_function="explain_class",
                expected_arguments=["ShareholderEquity"],
                should_contain=["ShareholdersEquity", "equity"],
                category="fuzzy_matching"
            ),
            TestCase(
                name="Fuzzy Matching - Case Variations",
                query="explain OWNERSEQUITY",
                expected_function="explain_class",
                expected_arguments=["OWNERSEQUITY"],
                should_contain=["OwnersEquity"],
                category="fuzzy_matching"
            ),
        ]
        
        # 9. MULTI-STEP REASONING TESTS
        multi_step_tests = [
            TestCase(
                name="Multi-Step Comparative Analysis",
                query="Compare the inheritance structures of ShareholdersEquity and RetainedEarnings",
                expected_function="multi_step",
                expected_arguments=["comparative_analysis"],
                should_contain=["Individual Results", "get_all_superclasses", "ShareholdersEquity", "RetainedEarnings", "Analysis"],
                category="multi_step_reasoning"
            ),
            TestCase(
                name="Multi-Step Comprehensive Analysis",
                query="Analyze the complete structure of PaidInCapital including properties and relationships",
                expected_function="multi_step",
                expected_arguments=["comprehensive_analysis"],
                should_contain=["Individual Results", "PaidInCapital", "explain_class", "get_all_superclasses", "Analysis"],
                category="multi_step_reasoning"
            ),
            TestCase(
                name="Multi-Step Equity Comparison",
                query="What are the key differences between equity types in FIBO?",
                expected_function="multi_step",
                expected_arguments=["equity_comparison"],
                should_contain=["Individual Results", "search_classes_by_keyword", "equity", "Analysis"],
                category="multi_step_reasoning"
            ),
            TestCase(
                name="Multi-Step Overview",
                query="Give me a comprehensive overview of OwnersEquity",
                expected_function="multi_step",
                expected_arguments=["comprehensive_overview"],
                should_contain=["Individual Results", "OwnersEquity", "Analysis"],
                category="multi_step_reasoning"
            ),
        ]
        
        # Combine all test suites
        return (basic_tests + enhanced_tests + fibo_content_tests + 
                nl_variation_tests + error_tests + edge_case_tests +
                owl_reasoning_tests + fuzzy_matching_tests + multi_step_tests)
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case"""
        print(f"Running: {test_case.name}")
        start_time = time.time()
        
        try:
            response = run_natural_language_query(test_case.query)
            execution_time = time.time() - start_time
            
            success = True
            error_message = None
            
            if test_case.should_contain:
                for expected in test_case.should_contain:
                    if expected.lower() not in response.lower():
                        success = False
                        error_message = f"Missing expected content: '{expected}'"
                        break
            
            if test_case.should_not_contain and success:
                for forbidden in test_case.should_not_contain:
                    if forbidden.lower() in response.lower():
                        success = False
                        error_message = f"Contains forbidden content: '{forbidden}'"
                        break
            
            return TestResult(
                test_case=test_case,
                success=success,
                actual_response=response,
                execution_time=execution_time,
                error_message=error_message
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_case=test_case,
                success=False,
                actual_response=str(e),
                execution_time=execution_time,
                error_message=f"Exception: {str(e)}"
            )
    
    def run_all_tests(self, categories: List[str] = None) -> Dict[str, Any]:
        """Run all tests or specific categories"""
        if categories:
            test_cases = [t for t in self.test_cases if t.category in categories]
        else:
            test_cases = self.test_cases
        
        print(f"🧪 Running {len(test_cases)} tests...")
        print("=" * 60)
        
        results = []
        for test_case in test_cases:
            result = self.run_single_test(test_case)
            results.append(result)
            
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"{status} {test_case.name} ({result.execution_time:.2f}s)")
            if not result.success and result.error_message:
                print(f"   Error: {result.error_message}")
            print()
        
        self.results = results
        return self._generate_report()
    
    def run_category(self, category: str) -> Dict[str, Any]:
        """Run tests for a specific category"""
        return self.run_all_tests([category])
    
    def print_test_suite_info(self):
        """Display information about available test categories"""
        category_counts = {}
        for test in self.test_cases:
            category = test.category
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += 1
        
        print(f"📊 TEST SUITE BREAKDOWN (Total: {len(self.test_cases)} tests):")
        for category, count in sorted(category_counts.items()):
            print(f"   {category}: {count} tests")
        print()
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        category_stats = {}
        for result in self.results:
            cat = result.test_case.category
            if cat not in category_stats:
                category_stats[cat] = {"total": 0, "passed": 0, "failed": 0}
            
            category_stats[cat]["total"] += 1
            if result.success:
                category_stats[cat]["passed"] += 1
            else:
                category_stats[cat]["failed"] += 1
        
        avg_time = sum(r.execution_time for r in self.results) / total_tests
        max_time = max(r.execution_time for r in self.results)
        min_time = min(r.execution_time for r in self.results)
        
        failed_tests_details = [
            {
                "name": r.test_case.name,
                "query": r.test_case.query,
                "error": r.error_message,
                "response": r.actual_response[:200] + "..." if len(r.actual_response) > 200 else r.actual_response
            }
            for r in self.results if not r.success
        ]
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
            },
            "performance": {
                "avg_execution_time": f"{avg_time:.3f}s",
                "max_execution_time": f"{max_time:.3f}s",
                "min_execution_time": f"{min_time:.3f}s"
            },
            "category_breakdown": category_stats,
            "failed_tests": failed_tests_details
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any] = None):
        """Print formatted test report"""
        if report is None:
            report = self._generate_report()
        
        print("\n" + "="*60)
        print("🧪 FIBO ONTOLOGY AGENT TEST REPORT - ENHANCED")
        print("="*60)
        
        summary = report["summary"]
        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Success Rate: {summary['success_rate']}")
        
        perf = report["performance"]
        print(f"\n⏱️  PERFORMANCE:")
        print(f"   Average: {perf['avg_execution_time']}")
        print(f"   Fastest: {perf['min_execution_time']}")
        print(f"   Slowest: {perf['max_execution_time']}")
        
        print(f"\n📂 CATEGORY BREAKDOWN:")
        for category, stats in report["category_breakdown"].items():
            success_rate = (stats["passed"] / stats["total"]) * 100
            print(f"   {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        if report["failed_tests"]:
            print(f"\n❌ FAILED TESTS:")
            for i, failed in enumerate(report["failed_tests"], 1):
                print(f"   {i}. {failed['name']}")
                print(f"      Query: '{failed['query']}'")
                print(f"      Error: {failed['error']}")
                print(f"      Response: {failed['response']}")
                print()

def main():
    """Main test execution with persistent menu"""
    battery = FIBOTestBattery()
    
    print("🚀 FIBO Ontology Agent Test Battery - ENHANCED WITH MULTI-STEP REASONING")
    print("=" * 70)
    
    # Show test suite breakdown
    battery.print_test_suite_info()
    
    while True:
        print("📋 AVAILABLE TEST SUITES:")
        print("1. All tests (comprehensive)")
        print("2. Basic functions only")
        print("3. Enhanced functions only") 
        print("4. FIBO content tests only")
        print("5. Error handling tests only")
        print("6. OWL reasoning tests only")
        print("7. Fuzzy matching tests only")
        print("8. Multi-step reasoning tests only (NEW!)")
        print("9. Quick test (5 basic tests)")
        print("0. Exit")
        
        choice = input("\n🎯 Enter choice (0-9): ").strip()
        
        if choice == "0":
            print("👋 Exiting test battery. Goodbye!")
            break
        elif choice == "1":
            print(f"\n🧪 Running ALL {len(battery.test_cases)} tests...")
            report = battery.run_all_tests()
        elif choice == "2":
            print("\n🧪 Running basic functions tests...")
            report = battery.run_category("basic_functions")
        elif choice == "3":
            print("\n🧪 Running enhanced functions tests...")
            report = battery.run_category("enhanced_functions")
        elif choice == "4":
            print("\n🧪 Running FIBO content tests...")
            report = battery.run_category("fibo_content")
        elif choice == "5":
            print("\n🧪 Running error handling tests...")
            report = battery.run_category("error_handling")
        elif choice == "6":
            print("\n🧪 Running OWL reasoning tests...")
            report = battery.run_category("owl_reasoning")
        elif choice == "7":
            print("\n🧪 Running fuzzy matching tests...")
            report = battery.run_category("fuzzy_matching")
        elif choice == "8":
            print("\n🧪 Running multi-step reasoning tests...")
            report = battery.run_category("multi_step_reasoning")
        elif choice == "9":
            print("\n🧪 Running quick test (5 basic functions)...")
            quick_tests = battery.test_cases[:5]
            temp_battery = FIBOTestBattery()
            temp_battery.test_cases = quick_tests
            report = temp_battery.run_all_tests()
        else:
            print("❌ Invalid choice. Please enter 0-9.")
            continue
        
        battery.print_report(report)
        
        print("\n" + "=" * 70)
        continue_choice = input("🔄 Run another test suite? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("👋 Exiting test battery. Goodbye!")
            break

if __name__ == "__main__":
    main()