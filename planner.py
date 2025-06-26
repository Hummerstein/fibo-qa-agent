import requests
import json
from typing import List, Dict, Any
from tools.ontology_tools import (
    # Original functions
    get_superclasses,
    get_subclasses,
    get_properties,
    describe_class,
    get_class_candidates,
    resolve_class_name_fuzzy,
    explain_class,
    # Enhanced functions
    search_classes_by_keyword,
    get_related_concepts,
    explain_relationship,
    get_property_details,
    get_ontology_stats,
    # Bonus functions
    get_class_info,
    get_all_superclasses,
    # OWL reasoning functions
    get_inferred_properties,
    get_reasoning_chain,
    # Fuzzy matching functions
    format_suggestions_message
)

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_MODEL = "google/gemma-3-12b"

SIMPLE_TOOLS_DESCRIPTION = """
You are a semantic planner for FIBO ontology queries. Given a user's question, return a JSON object with:
- function: the tool to call
- arguments: a list of arguments (empty if not required)

Available tools:
- get_superclasses(class_name): Get direct parent classes
- get_subclasses(class_name): Get direct child classes  
- get_properties(class_name): Get properties of a class
- describe_class(class_name): Basic class description
- explain_class(class_name): Detailed class explanation with metadata
- search_classes_by_keyword(keyword): Search for classes containing keyword
- get_related_concepts(class_name, max_depth): Find related concepts (default depth=2)
- explain_relationship(class1, class2): Explain how two classes are related
- get_property_details(property_name): Get detailed property information
- get_class_info(class_name): Comprehensive one-shot class summary
- get_all_superclasses(class_name): Get complete inheritance chain (OWL transitive closure)
- get_inferred_properties(class_name): Get all properties through inheritance (OWL property inheritance)
- get_reasoning_chain(class1, class2): Show OWL reasoning path between classes
- list_classes(): List all available classes
- get_ontology_stats(): Get ontology statistics

Only return valid JSON. Do not explain your answer.
"""

MULTI_STEP_TOOLS_DESCRIPTION = """
You are an advanced semantic planner for FIBO ontology queries with multi-step reasoning capabilities.

For COMPLEX queries that require multiple steps, return a JSON array of function calls:
[
    {"function": "function_name", "arguments": ["arg1", "arg2"]},
    {"function": "another_function", "arguments": ["arg1"]},
    {"step": "analysis", "instruction": "synthesize the results and provide insights"}
]

For SIMPLE queries, return a single JSON object:
{"function": "function_name", "arguments": ["arg1"]}

Available tools:
- get_superclasses(class_name): Get direct parent classes
- get_subclasses(class_name): Get direct child classes  
- get_properties(class_name): Get properties of a class
- describe_class(class_name): Basic class description
- explain_class(class_name): Detailed class explanation with metadata
- search_classes_by_keyword(keyword): Search for classes containing keyword
- get_related_concepts(class_name, max_depth): Find related concepts
- explain_relationship(class1, class2): Explain how two classes are related
- get_property_details(property_name): Get detailed property information
- get_class_info(class_name): Comprehensive one-shot class summary
- get_all_superclasses(class_name): Get complete inheritance chain
- get_inferred_properties(class_name): Get all properties through inheritance
- get_reasoning_chain(class1, class2): Show OWL reasoning path between classes
- list_classes(): List all available classes
- get_ontology_stats(): Get ontology statistics

COMPLEX QUERY EXAMPLES:
User: "Compare the inheritance structures of ShareholdersEquity and RetainedEarnings"
[
    {"function": "get_all_superclasses", "arguments": ["ShareholdersEquity"]},
    {"function": "get_all_superclasses", "arguments": ["RetainedEarnings"]},
    {"step": "analysis", "instruction": "Compare inheritance structures and highlight similarities/differences"}
]

User: "Analyze the complete structure of PaidInCapital including properties and relationships"
[
    {"function": "explain_class", "arguments": ["PaidInCapital"]},
    {"function": "get_all_superclasses", "arguments": ["PaidInCapital"]},
    {"function": "get_subclasses", "arguments": ["PaidInCapital"]},
    {"function": "get_inferred_properties", "arguments": ["PaidInCapital"]},
    {"function": "get_related_concepts", "arguments": ["PaidInCapital"]},
    {"step": "analysis", "instruction": "Synthesize complete structural analysis of PaidInCapital"}
]

User: "What are the key differences between equity types in FIBO?"
[
    {"function": "search_classes_by_keyword", "arguments": ["equity"]},
    {"function": "get_all_superclasses", "arguments": ["ShareholdersEquity"]},
    {"function": "get_all_superclasses", "arguments": ["OwnersEquity"]},
    {"function": "explain_relationship", "arguments": ["ShareholdersEquity", "OwnersEquity"]},
    {"step": "analysis", "instruction": "Compare different equity types and their distinguishing characteristics"}
]

SIMPLE QUERY EXAMPLES:
User: "What is PaidInCapital?"
{"function": "explain_class", "arguments": ["PaidInCapital"]}

User: "Show me the parents of CapitalSurplus"
{"function": "get_superclasses", "arguments": ["CapitalSurplus"]}

Only return valid JSON (single object for simple queries, array for complex queries).
"""

def call_local_llm(prompt, use_multi_step=False):
    """Call LLM with appropriate system prompt"""
    system_prompt = MULTI_STEP_TOOLS_DESCRIPTION if use_multi_step else SIMPLE_TOOLS_DESCRIPTION
    
    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": LM_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3  # Slightly higher for creative planning
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ LLM error: {e}"

def gemma_synthesize_results(instruction: str, results: List[Dict[str, Any]]) -> str:
    """Let Gemma analyze and synthesize results from multiple ontology operations"""
    
    # Prepare results for analysis
    results_text = ""
    for i, result in enumerate(results, 1):
        results_text += f"\n--- Result {i} ({result['function']}) ---\n"
        results_text += result['output']
        results_text += "\n"
    
    synthesis_prompt = f"""
    You are a FIBO ontology expert. Analyze these ontology query results and {instruction}.

    ONTOLOGY RESULTS:
    {results_text}

    INSTRUCTIONS: {instruction}

    Provide a comprehensive analysis that:
    1. Synthesizes the key insights from all results
    2. Explains relationships and patterns
    3. Highlights important financial concepts
    4. Provides practical context where relevant
    5. Uses clear, professional language
    
    Format your response with appropriate headers and bullet points for readability.
    """
    
    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": LM_MODEL,
                "messages": [
                    {"role": "user", "content": synthesis_prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 1000
            }
        )
        response.raise_for_status()
        analysis = response.json()["choices"][0]["message"]["content"]
        
        return f"🧠 **Gemma Analysis & Synthesis:**\n\n{analysis}"
        
    except Exception as e:
        return f"❌ Analysis error: {e}"

def execute_single_function(func_call: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single ontology function call"""
    func = func_call.get("function")
    args = func_call.get("arguments", [])
    
    # Handle functions that don't need class name resolution
    if func == "list_classes":
        return {"function": func, "output": list_classes()}
    elif func == "get_ontology_stats":
        return {"function": func, "output": get_ontology_stats()}
    elif func == "search_classes_by_keyword":
        if args:
            return {"function": func, "output": search_classes_by_keyword(*args)}
        else:
            return {"function": func, "output": "❌ search_classes_by_keyword requires a keyword argument"}

    # Handle functions that need class name resolution with fuzzy matching
    single_class_functions = [
        "get_superclasses", "get_subclasses", "get_properties", 
        "describe_class", "explain_class", "get_related_concepts",
        "get_class_info", "get_all_superclasses", "get_inferred_properties"
    ]
    
    if func in single_class_functions and args:
        original_name = args[0]
        resolved = resolve_class_name_fuzzy(original_name)
        
        if not resolved:
            suggestion_msg = format_suggestions_message(original_name)
            return {"function": func, "output": f"❌ Class '{original_name}' not found.\n{suggestion_msg}"}
        
        args[0] = resolved
        if resolved.lower() != original_name.lower():
            print(f"🔍 Resolved '{original_name}' → '{resolved}'")

    # Handle functions that need two class names
    if func in ["explain_relationship", "get_reasoning_chain"] and len(args) >= 2:
        for i in range(2):
            original_name = args[i]
            resolved = resolve_class_name_fuzzy(original_name)
            
            if not resolved:
                suggestion_msg = format_suggestions_message(original_name)
                return {"function": func, "output": f"❌ Class '{original_name}' not found.\n{suggestion_msg}"}
            
            args[i] = resolved
            if resolved.lower() != original_name.lower():
                print(f"🔍 Resolved '{original_name}' → '{resolved}'")

    # Execute the function
    if func == "get_superclasses":
        return {"function": func, "output": get_superclasses(*args)}
    elif func == "get_subclasses":
        return {"function": func, "output": get_subclasses(*args)}
    elif func == "get_properties":
        return {"function": func, "output": get_properties(*args)}
    elif func == "describe_class":
        return {"function": func, "output": describe_class(*args)}
    elif func == "explain_class":
        return {"function": func, "output": explain_class(*args)}
    elif func == "get_class_info":
        return {"function": func, "output": get_class_info(*args)}
    elif func == "get_all_superclasses":
        return {"function": func, "output": get_all_superclasses(*args)}
    elif func == "get_inferred_properties":
        return {"function": func, "output": get_inferred_properties(*args)}
    elif func == "get_related_concepts":
        if len(args) == 1:
            return {"function": func, "output": get_related_concepts(args[0])}
        else:
            return {"function": func, "output": get_related_concepts(*args)}
    elif func == "explain_relationship":
        if len(args) >= 2:
            return {"function": func, "output": explain_relationship(args[0], args[1])}
        else:
            return {"function": func, "output": "❌ explain_relationship requires two class names"}
    elif func == "get_reasoning_chain":
        if len(args) >= 2:
            return {"function": func, "output": get_reasoning_chain(args[0], args[1])}
        else:
            return {"function": func, "output": "❌ get_reasoning_chain requires two class names"}
    elif func == "get_property_details":
        return {"function": func, "output": get_property_details(*args)}
    else:
        return {"function": func, "output": f"❌ Unsupported function: {func}"}

def list_classes():
    """List all available classes with truncation"""
    candidates = get_class_candidates()
    return "\n".join(f"• {name}" for name in candidates[:100]) + ("\n... (truncated)" if len(candidates) > 100 else "")

def is_complex_query(user_input: str) -> bool:
    """Determine if query needs multi-step planning"""
    complex_indicators = [
        "compare", "analyze", "structure", "complete", "comprehensive",
        "differences", "similarities", "relationship between", "all about",
        "overview of", "breakdown", "in detail", "thorough", "full analysis"
    ]
    
    user_lower = user_input.lower()
    return any(indicator in user_lower for indicator in complex_indicators)

def run_natural_language_query(user_input: str) -> str:
    """Process natural language query with multi-step reasoning capabilities"""
    
    # Determine if this needs multi-step planning
    use_multi_step = is_complex_query(user_input)
    
    print(f"🧠 Query type: {'Multi-step reasoning' if use_multi_step else 'Simple query'}")
    
    # Get plan from Gemma
    raw_plan = call_local_llm(user_input, use_multi_step=use_multi_step)
    print("📦 Raw plan:", raw_plan)

    # Clean up JSON formatting
    if "```" in raw_plan:
        raw_plan = raw_plan.replace("```json", "").replace("```", "").strip()

    try:
        plan = json.loads(raw_plan)
    except json.JSONDecodeError:
        return f"❌ Failed to parse LLM output as JSON:\n{raw_plan}"

    # Handle single-step plan (simple query)
    if isinstance(plan, dict) and "function" in plan:
        print("🔧 Executing single function...")
        result = execute_single_function(plan)
        return result["output"]
    
    # Handle multi-step plan (complex query)
    elif isinstance(plan, list):
        print(f"🔧 Executing multi-step plan ({len(plan)} steps)...")
        
        results = []
        final_analysis = None
        
        for i, step in enumerate(plan, 1):
            if "function" in step:
                print(f"   Step {i}: {step['function']}")
                result = execute_single_function(step)
                results.append(result)
                print(f"   ✅ Completed {step['function']}")
            
            elif "step" in step and step["step"] == "analysis":
                print(f"   Step {i}: Gemma synthesis & analysis...")
                instruction = step.get("instruction", "Analyze and synthesize the results")
                final_analysis = gemma_synthesize_results(instruction, results)
                print(f"   ✅ Analysis complete")
        
        # Compile final response
        response_parts = []
        
        # Add individual results
        response_parts.append("📋 **Individual Results:**\n")
        for i, result in enumerate(results, 1):
            response_parts.append(f"### {i}. {result['function']}")
            response_parts.append(result['output'])
            response_parts.append("")  # Empty line
        
        # Add Gemma's synthesis if available
        if final_analysis:
            response_parts.append("=" * 60)
            response_parts.append(final_analysis)
        
        return "\n".join(response_parts)
    
    else:
        return f"❌ Invalid plan format: {plan}"

# ========== MODULE MANAGEMENT FUNCTIONS ==========

def get_current_module_info():
    """Get information about the currently loaded module set"""
    from tools.ontology_tools import CURRENT_MODULE_SET, MODULE_SETS, get_ontology_stats
    
    current_info = {
        'name': CURRENT_MODULE_SET,
        'display_name': MODULE_SETS[CURRENT_MODULE_SET]['name'],
        'module_count': len(MODULE_SETS[CURRENT_MODULE_SET]['modules']),
        'modules': MODULE_SETS[CURRENT_MODULE_SET]['modules']
    }
    
    # Get current ontology stats
    stats = get_ontology_stats()
    
    return current_info, stats

def switch_fibo_module_set(new_module_set):
    """Switch to a different FIBO module set and return results"""
    from tools.ontology_tools import switch_module_set, MODULE_SETS
    
    if new_module_set not in MODULE_SETS:
        available = list(MODULE_SETS.keys())
        return {
            'success': False,
            'message': f"❌ Invalid module set '{new_module_set}'. Available: {', '.join(available)}",
            'available_sets': available
        }
    
    try:
        # Switch the module set
        result = switch_module_set(new_module_set)
        
        # Get new stats
        current_info, stats = get_current_module_info()
        
        return {
            'success': True,
            'message': result,
            'current_info': current_info,
            'stats': stats
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"❌ Error switching module set: {str(e)}",
            'error': str(e)
        }

def get_all_module_sets_info():
    """Get detailed information about all available module sets"""
    from tools.ontology_tools import MODULE_SETS, CURRENT_MODULE_SET
    
    module_info = {}
    
    for key, info in MODULE_SETS.items():
        module_info[key] = {
            'name': info['name'],
            'module_count': len(info['modules']),
            'modules': info['modules'],
            'is_current': key == CURRENT_MODULE_SET,
            'description': get_module_set_description(key)
        }
    
    return module_info

def get_module_set_description(module_set_name):
    """Get a description of what each module set focuses on"""
    descriptions = {
        'core': 'Basic financial concepts including accounting equity, ownership, and equity instruments. Good for getting started with FIBO.',
        'comprehensive': 'Full financial ontology coverage including debt instruments, financial instruments, securities, currencies, and business entities. Best for complete financial modeling.',
        'banking': 'Focused on banking and financial services including debt, currency amounts, and financial service entities. Ideal for banking applications.',
        'securities': 'Specialized in securities and capital markets including equity instruments, securities identification, issuance, and listings. Perfect for investment and trading applications.'
    }
    
    return descriptions.get(module_set_name, 'Custom module set with specialized focus.')

def compare_module_sets(set1, set2):
    """Compare two module sets to show differences"""
    from tools.ontology_tools import MODULE_SETS
    
    if set1 not in MODULE_SETS or set2 not in MODULE_SETS:
        return "❌ One or both module sets not found"
    
    modules1 = set(MODULE_SETS[set1]['modules'])
    modules2 = set(MODULE_SETS[set2]['modules'])
    
    common = modules1.intersection(modules2)
    only_in_1 = modules1 - modules2
    only_in_2 = modules2 - modules1
    
    comparison = {
        'set1': {'name': set1, 'total': len(modules1)},
        'set2': {'name': set2, 'total': len(modules2)},
        'common': list(common),
        'only_in_set1': list(only_in_1),
        'only_in_set2': list(only_in_2),
        'overlap_percentage': (len(common) / max(len(modules1), len(modules2))) * 100
    }
    
    return comparison

def get_available_module_sets():
    """Get list of available module sets (for compatibility)"""
    from tools.ontology_tools import MODULE_SETS
    return list(MODULE_SETS.keys())

def switch_module_set(module_set_name):
    """Switch module set (wrapper for compatibility)"""
    from tools.ontology_tools import switch_module_set as orig_switch
    return orig_switch(module_set_name)

# ========== ENHANCED QUERY PROCESSING ==========

def run_query_with_module_awareness(user_input: str) -> str:
    """Enhanced query processor that can handle module switching requests"""
    
    # Check if user is asking about module sets or wants to switch
    user_lower = user_input.lower()
    
    module_keywords = {
        'switch to comprehensive': 'comprehensive',
        'use comprehensive': 'comprehensive',
        'load comprehensive': 'comprehensive',
        'switch to banking': 'banking',
        'use banking': 'banking', 
        'load banking': 'banking',
        'switch to securities': 'securities',
        'use securities': 'securities',
        'load securities': 'securities',
        'switch to core': 'core',
        'use core': 'core',
        'load core': 'core'
    }
    
    # Check for module switching requests
    for phrase, module_name in module_keywords.items():
        if phrase in user_lower:
            result = switch_fibo_module_set(module_name)
            if result['success']:
                return f"✅ **Module Set Switched Successfully!**\n\n{result['message']}\n\n📊 **New Stats:**\n{result['stats']}"
            else:
                return result['message']
    
    # Check for module information requests
    if any(phrase in user_lower for phrase in ['available modules', 'module sets', 'what modules', 'current module']):
        current_info, stats = get_current_module_info()
        all_modules = get_all_module_sets_info()
        
        response = [f"📚 **Current Module Set:** {current_info['display_name']} ({current_info['name']})"]
        response.append(f"📊 **Current Stats:**\n{stats}")
        response.append("\n🔄 **Available Module Sets:**")
        
        for key, info in all_modules.items():
            status = "🟢 ACTIVE" if info['is_current'] else "⚪"
            response.append(f"  {status} **{key}**: {info['name']} ({info['module_count']} modules)")
            response.append(f"     {info['description']}")
        
        response.append("\n💡 **To switch:** Try 'switch to comprehensive' or 'use banking modules'")
        
        return "\n".join(response)
    
    # Check for module comparison requests
    if 'compare' in user_lower and any(word in user_lower for word in ['modules', 'sets']):
        # Simple comparison between current and comprehensive
        current_info, _ = get_current_module_info()
        if current_info['name'] != 'comprehensive':
            comparison = compare_module_sets(current_info['name'], 'comprehensive')
            
            response = [f"📊 **Module Set Comparison: {comparison['set1']['name']} vs {comparison['set2']['name']}**"]
            response.append(f"  📦 {comparison['set1']['name']}: {comparison['set1']['total']} modules")
            response.append(f"  📦 {comparison['set2']['name']}: {comparison['set2']['total']} modules")
            response.append(f"  🔗 Common modules: {len(comparison['common'])}")
            response.append(f"  📈 Overlap: {comparison['overlap_percentage']:.1f}%")
            
            if comparison['only_in_set2']:
                response.append(f"\n🆕 **Additional in {comparison['set2']['name']}:**")
                for module in sorted(comparison['only_in_set2'])[:5]:
                    response.append(f"  • {module}")
                if len(comparison['only_in_set2']) > 5:
                    response.append(f"  ... and {len(comparison['only_in_set2']) - 5} more")
            
            return "\n".join(response)
    
    # If not a module-related query, run the normal query processing
    return run_natural_language_query(user_input)

# ========== INTERACTIVE MODE ==========

def interactive_mode():
    """Run interactive question-answering mode"""
    print("✅ Enhanced FIBO Planner with Multi-Step Reasoning! 🧠⚡")
    print("\n🆕 New Multi-Step Capabilities:")
    print("  • 🔗 Complex query planning and execution")
    print("  • 🧠 Gemma-powered analysis and synthesis")
    print("  • 📊 Comparative analysis across multiple concepts")
    print("  • 💡 Intelligent insights and pattern recognition")
    print("  • 🎯 Comprehensive structural analysis")
    
    print("\n🧠 Try these multi-step reasoning queries:")
    print("  • 'Compare the inheritance structures of ShareholdersEquity and RetainedEarnings'")
    print("  • 'Analyze the complete structure of PaidInCapital including properties and relationships'")
    print("  • 'What are the key differences between equity types in FIBO?'")
    print("  • 'Give me a comprehensive overview of OwnersEquity'")
    print("  • 'Compare and contrast FinancialAsset and PhysicalAsset'")
    print()

    while True:
        user_input = input("💬 Ask a FIBO question (or 'q' to quit): ").strip()
        if user_input.lower() in {"q", "quit", "exit"}:
            print("👋 Exiting.")
            break

        result = run_query_with_module_awareness(user_input)
        print("🧠", result)
        print()

if __name__ == "__main__":
    interactive_mode()