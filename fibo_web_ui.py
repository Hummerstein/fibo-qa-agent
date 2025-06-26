#!/usr/bin/env python3
"""
FIBO Semantic Agent Web UI
Streamlit interface for the FIBO ontology semantic agent with multi-step reasoning
"""

import streamlit as st
import time
import json
from typing import Dict, Any, List
import traceback

# Import your existing modules
try:
    from planner import (
        run_natural_language_query,
        is_complex_query,
        get_current_module_info,
        switch_fibo_module_set,
        get_all_module_sets_info,
        compare_module_sets,
        run_query_with_module_awareness
    )
    from tools.ontology_tools import (
        get_ontology_stats,
        get_class_candidates,
        explore_fibo_domains,
        MODULE_SETS,
        CURRENT_MODULE_SET,
        onto,
        # Import functions for raw query testing
        get_superclasses,
        get_subclasses,
        get_properties,
        describe_class,
        explain_class,
        search_classes_by_keyword,
        get_related_concepts,
        explain_relationship,
        get_property_details,
        get_class_info,
        get_all_superclasses,
        get_inferred_properties,
        get_reasoning_chain
    )
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)

# Page configuration
st.set_page_config(
    page_title="FIBO Semantic Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .query-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_ontology_loaded():
    """Check if ontology is loaded and show loading animation if not"""
    from tools.ontology_tools import onto, load_fibo_modules
    
    if onto is None:
        st.warning("🔄 **Ontology not loaded.** Loading FIBO modules...")
        
        # Create a progress bar for loading
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate loading progress
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text(f"🔍 Initializing FIBO ontology tools... {i+1}%")
            elif i < 70:
                status_text.text(f"📦 Loading core FIBO modules... {i+1}%")
            else:
                status_text.text(f"🔗 Building ontology graph... {i+1}%")
            time.sleep(0.02)  # Small delay for visual effect
        
        # Actually load the ontology
        try:
            result = load_fibo_modules("core")
            progress_bar.progress(100)
            status_text.text("✅ Ontology loaded successfully!")
            time.sleep(1)  # Show success message briefly
            
            # Clear the loading UI
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 **FIBO Ontology Ready!** You can now query the financial ontology.")
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ **Failed to load ontology:** {str(e)}")
            st.stop()

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">🧠 FIBO Semantic Agent</h1>', unsafe_allow_html=True)
    st.markdown("**Financial Industry Business Ontology Query System with Multi-Step Reasoning**")
    
    if not IMPORTS_OK:
        st.error(f"❌ **Import Error:** {IMPORT_ERROR}")
        st.error("Make sure `planner.py` and `tools/ontology_tools.py` are available in the current directory.")
        st.stop()
    
    # Check and load ontology if needed
    check_ontology_loaded()

def render_module_switcher_sidebar():
    """Render module switcher in sidebar"""
    st.sidebar.markdown("## 📚 FIBO Module Management")
    
    try:
        # Get current module info
        current_info, stats = get_current_module_info()
        all_modules = get_all_module_sets_info()
        
        # Display current module
        st.sidebar.markdown(f'<div class="success-box"><strong>🟢 Active:</strong> {current_info["display_name"]}</div>', 
                           unsafe_allow_html=True)
        
        # Module selector
        module_options = list(all_modules.keys())
        current_index = module_options.index(current_info['name'])
        
        selected_module = st.sidebar.selectbox(
            "🔄 Switch Module Set:",
            options=module_options,
            index=current_index,
            format_func=lambda x: f"{x}: {all_modules[x]['name']}"
        )
        
        # Switch button
        if st.sidebar.button("🚀 Switch Module Set", key="switch_btn") and selected_module != current_info['name']:
            with st.spinner(f"Switching to {selected_module}..."):
                result = switch_fibo_module_set(selected_module)
                
                if result['success']:
                    st.sidebar.success("✅ Module set switched!")
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ Switch failed: {result['message']}")
        
        # Display module details
        selected_info = all_modules[selected_module]
        
        with st.sidebar.expander("📋 Module Details"):
            st.write(f"**Description:** {selected_info['description']}")
            st.write(f"**Modules:** {selected_info['module_count']}")
            
            if st.checkbox("Show module files", key="show_modules"):
                st.write("**Files:**")
                for module in selected_info['modules']:
                    st.write(f"• `{module}`")
        
        # Quick stats
        with st.sidebar.expander("📊 Ontology Statistics"):
            st.text(stats)
            
        # Quick actions
        st.sidebar.markdown("### ⚡ Quick Actions")
        if st.sidebar.button("🔍 Explore Domains", key="explore_btn"):
            st.session_state['run_explore'] = True
        
        if st.sidebar.button("📋 List Classes", key="list_btn"):
            st.session_state['run_list'] = True
            
    except Exception as e:
        st.sidebar.error(f"❌ Error in module switcher: {str(e)}")

def render_query_examples():
    """Render example queries"""
    with st.expander("💡 Example Queries"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔍 Simple Queries:**")
            examples_simple = [
                "What is ShareholdersEquity?",
                "Show me the parents of OwnersEquity", 
                "What properties does CapitalSurplus have?",
                "Search for classes containing 'equity'",
                "List all available classes"
            ]
            for example in examples_simple:
                if st.button(f"`{example}`", key=f"simple_{hash(example)}"):
                    st.session_state['query_input'] = example
                    st.session_state['run_query'] = True
        
        with col2:
            st.markdown("**🧠 Multi-Step Reasoning:**")
            examples_complex = [
                "Compare ShareholdersEquity and RetainedEarnings inheritance",
                "Analyze the complete structure of PaidInCapital",
                "What are the key differences between equity types?",
                "Give me a comprehensive overview of OwnersEquity",
                "Compare FinancialAsset and PhysicalAsset relationships"
            ]
            for example in examples_complex:
                if st.button(f"`{example}`", key=f"complex_{hash(example)}"):
                    st.session_state['query_input'] = example
                    st.session_state['run_query'] = True

def render_module_comparison():
    """Render module comparison tool"""
    st.markdown("### 🔍 Module Set Comparison")
    
    try:
        all_modules = get_all_module_sets_info()
        module_names = list(all_modules.keys())
        
        col1, col2 = st.columns(2)
        
        with col1:
            set1 = st.selectbox("First Module Set:", module_names, key="comp_set1")
        
        with col2:
            set2 = st.selectbox("Second Module Set:", module_names, 
                               index=1 if len(module_names) > 1 else 0, key="comp_set2")
        
        if st.button("🔍 Compare Module Sets") and set1 != set2:
            comparison = compare_module_sets(set1, set2)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"📦 {set1} Modules", comparison['set1']['total'])
            with col2:
                st.metric(f"📦 {set2} Modules", comparison['set2']['total'])
            with col3:
                st.metric("🔗 Overlap", f"{comparison['overlap_percentage']:.1f}%")
            
            # Details
            if comparison['common']:
                with st.expander(f"🤝 Common Modules ({len(comparison['common'])})"):
                    for module in sorted(comparison['common']):
                        st.write(f"• `{module}`")
            
            col1, col2 = st.columns(2)
            with col1:
                if comparison['only_in_set1']:
                    with st.expander(f"🟦 Only in {set1} ({len(comparison['only_in_set1'])})"):
                        for module in sorted(comparison['only_in_set1']):
                            st.write(f"• `{module}`")
            
            with col2:
                if comparison['only_in_set2']:
                    with st.expander(f"🟨 Only in {set2} ({len(comparison['only_in_set2'])})"):
                        for module in sorted(comparison['only_in_set2']):
                            st.write(f"• `{module}`")
                            
    except Exception as e:
        st.error(f"❌ Error in module comparison: {str(e)}")

def render_main_interface():
    """Render the main query interface"""
    
    # Query input
    query_input = st.text_input(
        "💬 Ask a question about FIBO:",
        placeholder="e.g., 'What is ShareholdersEquity?' or 'switch to comprehensive'",
        key="query_input",
        value=st.session_state.get('query_input', '')
    )
    
    # Query controls
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        query_button = st.button("🚀 Query", key="query_btn", type="primary")
    
    with col2:
        if st.button("🧠 Multi-Step", key="multistep_btn"):
            st.session_state['force_multistep'] = True
            st.session_state['run_query'] = True
    
    with col3:
        if st.button("🗑️ Clear", key="clear_btn"):
            st.session_state['query_input'] = ''
            st.session_state['last_result'] = ''
            st.rerun()
    
    # Check if query should run
    should_run = (
        query_button or 
        st.session_state.get('run_query', False) or
        st.session_state.get('force_multistep', False)
    )
    
    if should_run and query_input.strip():
        run_query(query_input.strip())
        
        # Clear the run flags
        st.session_state['run_query'] = False
        st.session_state['force_multistep'] = False
    
    # Handle quick actions
    if st.session_state.get('run_explore', False):
        st.session_state['run_explore'] = False
        run_query("explore fibo domains")
    
    if st.session_state.get('run_list', False):
        st.session_state['run_list'] = False  
        run_query("list classes")

def run_query(query: str):
    """Execute a query and display results"""
    
    # Show query being processed
    st.markdown(f'<div class="query-box"><strong>🔍 Query:</strong> {query}</div>', 
                unsafe_allow_html=True)
    
    # Determine query type
    is_complex = is_complex_query(query) or st.session_state.get('force_multistep', False)
    query_type = "Multi-step reasoning" if is_complex else "Simple query"
    
    st.info(f"🧠 **Query Type:** {query_type}")
    
    # Execute query with progress
    start_time = time.time()
    
    with st.spinner("Processing query..."):
        try:
            # Use the enhanced query function that handles module switching
            result = run_query_with_module_awareness(query)
            execution_time = time.time() - start_time
            
            # Display result
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
            
            # Show execution info
            st.success(f"✅ **Query completed** in {execution_time:.2f} seconds")
            
            # Store result in session state
            st.session_state['last_result'] = result
            
        except Exception as e:
            st.error(f"❌ **Query Error:** {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())

def render_advanced_tools():
    """Render advanced tools section"""
    with st.expander("🛠️ Advanced Tools"):
        
        # Module comparison
        render_module_comparison()
        
        st.markdown("---")
        
        # Raw query testing
        st.markdown("### 🧪 Raw Query Testing")
        raw_query = st.text_area(
            "Direct ontology function call:",
            placeholder="e.g., get_superclasses('ShareholdersEquity')"
        )
        
        if st.button("🧪 Execute Raw Query") and raw_query.strip():
            try:
                # Create a safe environment for raw query execution
                safe_globals = {
                    'get_superclasses': get_superclasses,
                    'get_subclasses': get_subclasses,
                    'get_properties': get_properties,
                    'describe_class': describe_class,
                    'explain_class': explain_class,
                    'search_classes_by_keyword': search_classes_by_keyword,
                    'get_related_concepts': get_related_concepts,
                    'explain_relationship': explain_relationship,
                    'get_property_details': get_property_details,
                    'get_class_info': get_class_info,
                    'get_all_superclasses': get_all_superclasses,
                    'get_inferred_properties': get_inferred_properties,
                    'get_reasoning_chain': get_reasoning_chain,
                    'get_ontology_stats': get_ontology_stats,
                    'explore_fibo_domains': explore_fibo_domains
                }
                
                # This is unsafe in production, but useful for testing
                result = eval(raw_query.strip(), {"__builtins__": {}}, safe_globals)
                st.code(str(result))
            except Exception as e:
                st.error(f"❌ Raw query error: {str(e)}")

def main():
    """Main Streamlit app"""
    
    # Initialize session state
    if 'query_input' not in st.session_state:
        st.session_state['query_input'] = ''
    if 'last_result' not in st.session_state:
        st.session_state['last_result'] = ''
    
    # Render header
    render_header()
    
    # Render sidebar
    render_module_switcher_sidebar()
    
    # Main content
    main_col, info_col = st.columns([2, 1])
    
    with main_col:
        # Main query interface
        render_main_interface()
        
        # Show last result if available
        if st.session_state.get('last_result'):
            with st.expander("📋 Last Result", expanded=False):
                st.markdown(st.session_state['last_result'])
    
    with info_col:
        # Example queries
        render_query_examples()
        
        # Advanced tools
        render_advanced_tools()
    
    # Footer
    st.markdown("---")
    st.markdown("**🧠 FIBO Semantic Agent** | Built with Streamlit | Enhanced with Multi-Step Reasoning")

if __name__ == "__main__":
    main()