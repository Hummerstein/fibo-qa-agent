from owlready2 import get_ontology, Thing
from pathlib import Path
from collections import defaultdict, deque
import difflib

# ✅ Base path to your fibo-ontology directory
ONTOLOGY_BASE_PATH = Path("/Users/thudblunder/Documents/fibo_qa_agent/fibo-ontology")

# 🆕 EXPANDED FIBO MODULES - Multiple Financial Domains
MODULE_SETS = {
    "core": {
        "name": "Core Financial Concepts",
        "modules": [
            "FND/Accounting/AccountingEquity.rdf",
            "FND/OwnershipAndControl/Ownership.rdf",
            "SEC/Equities/EquityInstruments.rdf"
        ]
    },
    "comprehensive": {
        "name": "Comprehensive Financial Ontology",
        "modules": [
            # Core modules
            "FND/Accounting/AccountingEquity.rdf",
            "FND/OwnershipAndControl/Ownership.rdf",
            "SEC/Equities/EquityInstruments.rdf",
            
            # Additional Foundations
            "FND/Accounting/CurrencyAmount.rdf",
            "FND/Relations/Relations.rdf",
            "FND/Utilities/Values.rdf",
            "FND/DatesAndTimes/FinancialDates.rdf",
            
            # Securities & Markets
            "SEC/Securities/Securities.rdf",
            "SEC/Securities/SecuritiesIdentification.rdf",
            "SEC/Securities/SecuritiesIssuance.rdf",
            "SEC/Securities/SecuritiesListings.rdf",
            
            # Financial Business & Commerce
            "FBC/FinancialInstruments/FinancialInstruments.rdf",
            "FBC/ProductsAndServices/FinancialProductsAndServices.rdf",
            "FBC/FunctionalEntities/FinancialServicesEntities.rdf",
            
            # Debt & Credit
            "FBC/DebtAndEquities/Debt.rdf",
            
            # Business Entities
            "BE/LegalEntities/LegalPersons.rdf"
        ]
    },
    "banking": {
        "name": "Banking & Financial Services",
        "modules": [
            "FND/Accounting/AccountingEquity.rdf",
            "FND/Accounting/CurrencyAmount.rdf",
            "FBC/FinancialInstruments/FinancialInstruments.rdf",
            "FBC/ProductsAndServices/FinancialProductsAndServices.rdf",
            "FBC/FunctionalEntities/FinancialServicesEntities.rdf",
            "FBC/DebtAndEquities/Debt.rdf"
        ]
    },
    "securities": {
        "name": "Securities & Capital Markets",
        "modules": [
            "SEC/Equities/EquityInstruments.rdf",
            "SEC/Securities/Securities.rdf",
            "SEC/Securities/SecuritiesIdentification.rdf",
            "SEC/Securities/SecuritiesIssuance.rdf",
            "SEC/Securities/SecuritiesListings.rdf",
            "FBC/FinancialInstruments/FinancialInstruments.rdf"
        ]
    }
}

# Default module set
CURRENT_MODULE_SET = "core"
MODULE_FILES = MODULE_SETS[CURRENT_MODULE_SET]["modules"]

# Global ontology variable
onto = None

def load_fibo_modules(module_set_name: str = "core"):
    """Load FIBO modules based on selected set with complete world reset"""
    global onto, MODULE_FILES, CURRENT_MODULE_SET
    
    if module_set_name not in MODULE_SETS:
        available = ", ".join(MODULE_SETS.keys())
        return f"❌ Invalid module set. Available options: {available}"
    
    # NUCLEAR OPTION: Create completely new world
    from owlready2 import World
    
    # Create a brand new world
    world = World()
    
    CURRENT_MODULE_SET = module_set_name
    MODULE_FILES = MODULE_SETS[module_set_name]["modules"]
    
    print(f"📦 Loading FIBO module set: {MODULE_SETS[module_set_name]['name']}")
    print(f"📁 Modules to load: {len(MODULE_FILES)}")
    
    loaded_count = 0
    failed_modules = []
    
    # Load ALL modules into the new world
    for module in MODULE_FILES:
        full_path = ONTOLOGY_BASE_PATH / module
        if full_path.exists():
            try:
                print(f"🔗 Loading file://{full_path}")
                ontology = world.get_ontology(f"file://{full_path}").load()
                if loaded_count == 0:
                    onto = ontology  # Set the first one as primary reference
                loaded_count += 1
            except Exception as e:
                print(f"⚠️ Failed to load {module}: {e}")
                failed_modules.append(module)
        else:
            print(f"⚠️ File not found: {full_path}")
            failed_modules.append(module)
    
    # Update the default world to our new world
    import owlready2
    owlready2.default_world = world
    
    result = f"✅ Successfully loaded {loaded_count}/{len(MODULE_FILES)} modules in fresh world"
    if failed_modules:
        result += f"\n⚠️ Failed to load {len(failed_modules)} modules: {failed_modules[:3]}..."
    
    return result

def get_available_module_sets():
    """Get information about available module sets"""
    result = ["📚 Available FIBO Module Sets:"]
    
    for key, info in MODULE_SETS.items():
        status = "🟢 ACTIVE" if key == CURRENT_MODULE_SET else "⚪"
        result.append(f"  {status} {key}: {info['name']} ({len(info['modules'])} modules)")
    
    return "\n".join(result)

def switch_module_set(module_set_name: str):
    """Switch to a different module set"""
    if module_set_name == CURRENT_MODULE_SET:
        return f"ℹ️ Already using module set '{module_set_name}'"
    
    result = load_fibo_modules(module_set_name)
    return f"🔄 Switched to module set '{module_set_name}'\n{result}"

# ========== ENHANCED FUZZY MATCHING FUNCTIONS ==========

def get_class_candidates():
    """Get all class names from the current world"""
    import owlready2
    
    all_classes = []
    for ontology in owlready2.default_world.ontologies.values():
        for cls in ontology.classes():
            if hasattr(cls, "name"):
                all_classes.append(cls.name)
    
    return sorted(set(all_classes))

def get_class_suggestions(input_name, max_suggestions=3):
    """Get smart suggestions for misspelled class names"""
    candidates = get_class_candidates()
    if not candidates:
        return {"type": "none", "match": None, "suggestions": []}
    
    input_lower = input_name.lower()
    
    # 1. Exact match (case-insensitive)
    exact = [c for c in candidates if c.lower() == input_lower]
    if exact:
        return {"type": "exact", "match": exact[0], "suggestions": []}
    
    suggestions = []
    
    # 2. Substring matches (high priority)
    substring_matches = []
    for candidate in candidates:
        candidate_lower = candidate.lower()
        if input_lower in candidate_lower or candidate_lower in input_lower:
            substring_matches.append(candidate)
    
    # 3. Difflib close matches (typos and similar spelling)
    close_matches = difflib.get_close_matches(
        input_name, candidates, n=max_suggestions*2, cutoff=0.6
    )
    
    # 4. Character similarity (for abbreviations or partial names)
    char_matches = []
    for candidate in candidates:
        candidate_lower = candidate.lower()
        # Check if most characters from input appear in candidate
        input_chars = set(input_lower)
        candidate_chars = set(candidate_lower)
        if len(input_chars) > 2:  # Only for meaningful inputs
            similarity = len(input_chars & candidate_chars) / len(input_chars)
            if similarity > 0.75:
                char_matches.append((candidate, similarity))
    
    # Sort character matches by similarity
    char_matches.sort(key=lambda x: x[1], reverse=True)
    char_matches = [match[0] for match in char_matches]
    
    # 5. Prefix/suffix matches (for compound words)
    affix_matches = []
    for candidate in candidates:
        candidate_lower = candidate.lower()
        if (candidate_lower.startswith(input_lower) or 
            candidate_lower.endswith(input_lower) or
            input_lower.startswith(candidate_lower) or
            input_lower.endswith(candidate_lower)):
            affix_matches.append(candidate)
    
    # Combine all suggestions with priority
    all_suggestions = []
    
    # Priority 1: Substring matches
    all_suggestions.extend(substring_matches)
    
    # Priority 2: Close matches (typos)
    all_suggestions.extend([m for m in close_matches if m not in all_suggestions])
    
    # Priority 3: Character similarity
    all_suggestions.extend([m for m in char_matches if m not in all_suggestions])
    
    # Priority 4: Prefix/suffix matches
    all_suggestions.extend([m for m in affix_matches if m not in all_suggestions])
    
    # Return top suggestions
    final_suggestions = all_suggestions[:max_suggestions]
    
    if final_suggestions:
        return {"type": "suggestions", "match": None, "suggestions": final_suggestions}
    else:
        return {"type": "none", "match": None, "suggestions": []}

def resolve_class_name_fuzzy(input_name):
    """Enhanced fuzzy matching with suggestions"""
    result = get_class_suggestions(input_name)
    
    if result["type"] == "exact":
        return result["match"]
    elif result["type"] == "suggestions":
        suggestions = result["suggestions"]
        if suggestions:
            # Use difflib to get the closest match
            best_match = difflib.get_close_matches(input_name, suggestions, n=1, cutoff=0.8)
            if best_match:
                return best_match[0]
    
    return None

def format_suggestions_message(input_name):
    """Format a helpful message with suggestions"""
    result = get_class_suggestions(input_name)
    
    if result["type"] == "exact":
        return None  # No message needed, exact match found
    elif result["type"] == "suggestions":
        suggestions = result["suggestions"]
        if len(suggestions) == 1:
            return f"💡 Did you mean '{suggestions[0]}'? Try: explain {suggestions[0]}"
        else:
            # Fix f-string backslash issue
            suggestion_lines = []
            for suggestion in suggestions:
                suggestion_lines.append(f"   • {suggestion}")
            formatted_suggestions = "\n".join(suggestion_lines)
            return f"💡 Did you mean one of these?\n{formatted_suggestions}"
    else:
        return f"❌ No similar classes found for '{input_name}'. Try 'list classes' to see available options."

# ========== ORIGINAL FUNCTIONS WITH MODULE AWARENESS ==========

def get_superclasses(class_name):
    """Get direct superclasses of a given class"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found in the ontology.\n{suggestion_msg}"
    
    supers = list(cls.is_a)
    superclass_names = [c.name for c in supers if isinstance(c, Thing.__class__) and hasattr(c, 'name')]
    
    if not superclass_names:
        return f"ℹ️ No superclasses found for '{class_name}'."
    
    result = [f"🔼 Superclasses of '{class_name}':"]
    for name in sorted(set(superclass_names)):
        result.append(f"  📛 {name}")
    
    return "\n".join(result)

def get_subclasses(class_name):
    """Get direct subclasses of a given class"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found in the ontology.\n{suggestion_msg}"
    
    subs = list(cls.subclasses())
    subclass_names = [c.name for c in subs if hasattr(c, 'name')]
    
    if not subclass_names:
        return f"ℹ️ No subclasses found for '{class_name}'."
    
    result = [f"🔽 Subclasses of '{class_name}':"]
    for name in sorted(set(subclass_names)):
        result.append(f"  📛 {name}")
    
    return "\n".join(result)

def get_properties(class_name):
    """Get object and data properties for a given class"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found in the ontology.\n{suggestion_msg}"

    object_props = []
    data_props = []

    for prop in onto.properties():
        if hasattr(prop, 'domain'):
            domains = set(prop.domain) if prop.domain else set()
            # Check if this class or any of its ancestors are in the domain
            if any(cls in c.ancestors() or cls == c for c in domains):
                if hasattr(prop, 'range') and prop.range:
                    # Check if it's a data property (XSD types)
                    if any(hasattr(r, 'name') and (r.name.startswith("xsd:") or r.name == "string") for r in prop.range):
                        data_props.append(prop.name)
                    else:
                        object_props.append(prop.name)
                else:
                    object_props.append(prop.name)

    if not object_props and not data_props:
        return f"ℹ️ No properties found for '{class_name}'."

    result = [f"🔧 Properties for '{class_name}':"]
    if object_props:
        result.append(f"🔗 Object properties: {', '.join(sorted(set(object_props)))}")
    if data_props:
        result.append(f"🔤 Data properties: {', '.join(sorted(set(data_props)))}")
    
    return "\n".join(result)

def describe_class(class_name):
    """Basic class description with hierarchy"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"

    parts = [f"📛 {cls.name}"]
    
    # Get superclasses
    supers = [c.name for c in cls.is_a if hasattr(c, 'name')]
    if supers:
        unique_supers = sorted(set(supers))
        parts.append("🔼 Superclasses: " + ", ".join(unique_supers))
    
    # Get subclasses
    subs = [c.name for c in cls.subclasses() if hasattr(c, 'name')]
    if subs:
        unique_subs = sorted(set(subs))
        parts.append("🔽 Subclasses: " + ", ".join(unique_subs))
    
    return "\n".join(parts)

def explain_class(class_name):
    """Detailed class explanation with metadata"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"

    parts = [f"📛 {cls.name}"]

    # Add labels
    labels = cls.label if hasattr(cls, "label") else []
    if labels:
        unique_labels = sorted(set(str(label) for label in labels))
        parts.append("📝 Label: " + ", ".join(unique_labels))

    # Add comments/definitions
    comments = cls.comment if hasattr(cls, "comment") else []
    definitions = getattr(cls, 'definition', []) if hasattr(cls, 'definition') else []
    
    # Try to get skos:definition
    try:
        from owlready2 import SKOS
        skos_definitions = getattr(cls, SKOS.definition.python_name, []) if hasattr(cls, SKOS.definition.python_name) else []
        definitions.extend(skos_definitions)
    except:
        pass
    
    all_descriptions = list(comments) + list(definitions)
    if all_descriptions:
        unique_descriptions = sorted(set(str(desc) for desc in all_descriptions))
        parts.append("🗒️ Definition: " + " | ".join(unique_descriptions))

    # Add superclasses
    supers = [c.name for c in cls.is_a if hasattr(c, 'name')]
    if supers:
        unique_supers = sorted(set(supers))
        parts.append("🔼 Superclasses: " + ", ".join(unique_supers))

    # Add subclasses
    subs = [c.name for c in cls.subclasses() if hasattr(c, 'name')]
    if subs:
        unique_subs = sorted(set(subs))
        parts.append("🔽 Subclasses: " + ", ".join(unique_subs))

    return "\n".join(parts)

def search_classes_by_keyword(keyword):
    """Find classes containing keyword in name, label, or comment"""
    import owlready2
    
    keyword_lower = keyword.lower()
    matches = []
    
    # Search across ALL ontologies in the world
    for ontology in owlready2.default_world.ontologies.values():
        for cls in ontology.classes():
            if not hasattr(cls, 'name'):
                continue
                
            # Check name
            if keyword_lower in cls.name.lower():
                matches.append({
                    'name': cls.name,
                    'match_type': 'name',
                    'match_text': cls.name
                })
                continue
            
            # Check labels
            labels = cls.label if hasattr(cls, 'label') else []
            for label in labels:
                if keyword_lower in str(label).lower():
                    matches.append({
                        'name': cls.name,
                        'match_type': 'label',
                        'match_text': str(label)
                    })
                    break
            
            # Check comments and definitions
            comments = cls.comment if hasattr(cls, 'comment') else []
            for comment in comments:
                if keyword_lower in str(comment).lower():
                    comment_str = str(comment)
                    matches.append({
                        'name': cls.name,
                        'match_type': 'comment',
                        'match_text': comment_str[:100] + "..." if len(comment_str) > 100 else comment_str
                    })
                    break
    
    if not matches:
        return f"❌ No classes found containing '{keyword}'"
    
    result = [f"🔍 Found {len(matches)} classes containing '{keyword}':"]
    for match in matches[:15]:  # Limit to first 15 results
        result.append(f"  📛 {match['name']} ({match['match_type']}: {match['match_text']})")
    
    if len(matches) > 15:
        result.append(f"  ... and {len(matches) - 15} more matches")
    
    return "\n".join(result)

def get_ontology_stats():
    """Get comprehensive statistics about the loaded ontology"""
    import owlready2
    
    if not owlready2.default_world.ontologies:
        return "❌ No ontology loaded. Please load modules first."
    
    # Count from ALL ontologies in the world
    all_classes = []
    all_properties = []
    all_individuals = []
    
    for ontology in owlready2.default_world.ontologies.values():
        all_classes.extend([c for c in ontology.classes() if hasattr(c, 'name')])
        all_properties.extend([p for p in ontology.properties() if hasattr(p, 'name')])
        all_individuals.extend([i for i in ontology.individuals() if hasattr(i, 'name')])
    
    class_count = len(all_classes)
    property_count = len(all_properties)
    individual_count = len(all_individuals)
    
    # Group classes by module/namespace
    module_stats = {}
    for cls in all_classes:
        if hasattr(cls, 'iri'):
            iri = str(cls.iri)
            if 'fibo' in iri.lower():
                # Extract module info from IRI
                parts = iri.split('/')
                if len(parts) >= 3:
                    module_key = '/'.join(parts[-3:-1])  # e.g., "FND/Accounting"
                    if module_key not in module_stats:
                        module_stats[module_key] = 0
                    module_stats[module_key] += 1
    
    result = [
        f"📊 FIBO Ontology Statistics - {MODULE_SETS[CURRENT_MODULE_SET]['name']}:",
        f"  📛 Classes: {class_count}",
        f"  🔧 Properties: {property_count}",
        f"  👤 Individuals: {individual_count}",
        f"  📦 Loaded modules: {len(MODULE_FILES)}",
        f"  🎯 Current module set: {CURRENT_MODULE_SET}"
    ]
    
    if module_stats:
        result.append("\n📂 Classes by Module:")
        for module, count in sorted(module_stats.items()):
            result.append(f"  {module}: {count} classes")
    
    return "\n".join(result)
    
    if module_stats:
        result.append("\n📂 Classes by Module:")
        for module, count in sorted(module_stats.items()):
            result.append(f"  {module}: {count} classes")
    
    return "\n".join(result)
    """Get comprehensive statistics about the loaded ontology"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    classes = list(onto.classes())
    properties = list(onto.properties())
    individuals = list(onto.individuals())
    
    class_count = len([c for c in classes if hasattr(c, 'name')])
    property_count = len([p for p in properties if hasattr(p, 'name')])
    individual_count = len([i for i in individuals if hasattr(i, 'name')])
    
    # Group classes by module/namespace
    module_stats = {}
    for cls in classes:
        if hasattr(cls, 'name') and hasattr(cls, 'iri'):
            iri = str(cls.iri)
            if 'fibo' in iri.lower():
                # Extract module info from IRI
                parts = iri.split('/')
                if len(parts) >= 3:
                    module_key = '/'.join(parts[-3:-1])  # e.g., "FND/Accounting"
                    if module_key not in module_stats:
                        module_stats[module_key] = 0
                    module_stats[module_key] += 1
    
    result = [
        f"📊 FIBO Ontology Statistics - {MODULE_SETS[CURRENT_MODULE_SET]['name']}:",
        f"  📛 Classes: {class_count}",
        f"  🔧 Properties: {property_count}",
        f"  👤 Individuals: {individual_count}",
        f"  📦 Loaded modules: {len(MODULE_FILES)}",
        f"  🎯 Current module set: {CURRENT_MODULE_SET}"
    ]
    
    if module_stats:
        result.append("\n📂 Classes by Module:")
        for module, count in sorted(module_stats.items()):
            result.append(f"  {module}: {count} classes")
    
    return "\n".join(result)

def explore_fibo_domains():
    """Explore different FIBO domains based on loaded modules"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    # Analyze loaded classes by domain
    domains = {
        "Accounting": [],
        "Securities": [],
        "Banking": [],
        "Legal": [],
        "Relations": [],
        "Other": []
    }
    
    for cls in onto.classes():
        if hasattr(cls, 'name') and hasattr(cls, 'iri'):
            iri = str(cls.iri).lower()
            name = cls.name
            
            if 'accounting' in iri:
                domains["Accounting"].append(name)
            elif 'securities' in iri or 'equities' in iri:
                domains["Securities"].append(name)
            elif 'debt' in iri or 'functionalentities' in iri:
                domains["Banking"].append(name)
            elif 'legal' in iri or 'ownership' in iri:
                domains["Legal"].append(name)
            elif 'relations' in iri:
                domains["Relations"].append(name)
            else:
                domains["Other"].append(name)
    
    result = [f"🌐 FIBO Domain Analysis - {MODULE_SETS[CURRENT_MODULE_SET]['name']}:"]
    
    for domain, classes in domains.items():
        if classes:
            result.append(f"\n📁 {domain} ({len(classes)} classes):")
            # Show first 5 classes as examples
            examples = sorted(classes)[:5]
            for cls in examples:
                result.append(f"  📛 {cls}")
            if len(classes) > 5:
                result.append(f"  ... and {len(classes) - 5} more")
    
    return "\n".join(result)

# ========== ENHANCED FUNCTIONS ==========

def get_related_concepts(class_name, max_depth=2):
    """Find related concepts using breadth-first traversal"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"
    
    try:
        visited = set()
        queue = deque([(cls, 0)])  # (class, depth)
        related = defaultdict(list)
        
        while queue:
            current_cls, depth = queue.popleft()
            
            if current_cls in visited or depth > max_depth:
                continue
                
            visited.add(current_cls)
            
            if depth > 0:  # Don't include the starting class
                related[depth].append(current_cls.name)
            
            if depth < max_depth:
                # Add superclasses
                for parent in current_cls.is_a:
                    if hasattr(parent, 'name') and parent not in visited:
                        queue.append((parent, depth + 1))
                
                # Add subclasses
                for child in current_cls.subclasses():
                    if hasattr(child, 'name') and child not in visited:
                        queue.append((child, depth + 1))
        
        if not any(related.values()):
            return f"ℹ️ No related concepts found for '{class_name}' within depth {max_depth}"
        
        result = [f"🔗 Related concepts for '{class_name}' (max depth: {max_depth}):"]
        
        for depth in sorted(related.keys()):
            concepts = sorted(set(related[depth]))
            result.append(f"\n📍 Depth {depth} ({len(concepts)} concepts):")
            for concept in concepts:
                result.append(f"  📛 {concept}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error finding related concepts: {str(e)}"

def explain_relationship(class1, class2):
    """Explain the relationship between two classes"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls1 = onto.search_one(iri="*" + class1)
    cls2 = onto.search_one(iri="*" + class2)
    
    if not cls1:
        suggestion_msg = format_suggestions_message(class1)
        return f"❌ Class '{class1}' not found.\n{suggestion_msg}"
    if not cls2:
        suggestion_msg = format_suggestions_message(class2)
        return f"❌ Class '{class2}' not found.\n{suggestion_msg}"
    
    try:
        result = [f"🔗 Relationship between '{class1}' and '{class2}':"]
        
        # Check direct inheritance
        if cls2 in cls1.is_a:
            result.append(f"📈 '{class1}' IS-A '{class2}' (direct parent)")
        elif cls1 in cls2.is_a:
            result.append(f"📉 '{class2}' IS-A '{class1}' (direct parent)")
        
        # Check indirect inheritance
        cls1_ancestors = set(cls1.ancestors())
        cls2_ancestors = set(cls2.ancestors())
        
        if cls2 in cls1_ancestors:
            result.append(f"📈 '{class1}' inherits from '{class2}' (indirect)")
        elif cls1 in cls2_ancestors:
            result.append(f"📉 '{class2}' inherits from '{class1}' (indirect)")
        
        # Check for common ancestors
        common_ancestors = cls1_ancestors.intersection(cls2_ancestors)
        if common_ancestors:
            common_names = [c.name for c in common_ancestors if hasattr(c, 'name')]
            if common_names:
                result.append(f"🌳 Common ancestors: {', '.join(sorted(set(common_names)))}")
        
        # Check for sibling relationship (same direct parent)
        cls1_parents = set(cls1.is_a)
        cls2_parents = set(cls2.is_a)
        common_parents = cls1_parents.intersection(cls2_parents)
        
        if common_parents:
            parent_names = [p.name for p in common_parents if hasattr(p, 'name')]
            if parent_names:
                result.append(f"👫 Sibling classes (common parents): {', '.join(sorted(set(parent_names)))}")
        
        # Check for shared properties
        shared_props = []
        for prop in onto.properties():
            if hasattr(prop, 'domain') and prop.domain:
                domains = set(prop.domain)
                if any(cls1 in d.ancestors() or cls1 == d for d in domains) and \
                   any(cls2 in d.ancestors() or cls2 == d for d in domains):
                    shared_props.append(prop.name)
        
        if shared_props:
            result.append(f"🔧 Shared properties: {', '.join(sorted(set(shared_props)))}")
        
        if len(result) == 1:  # Only the header
            result.append("❌ No direct relationship found between these classes")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error analyzing relationship: {str(e)}"

def get_property_details(property_name):
    """Get detailed information about a property"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    prop = onto.search_one(iri="*" + property_name)
    if not prop:
        # Try fuzzy matching for properties
        all_props = [p.name for p in onto.properties() if hasattr(p, 'name')]
        suggestions = difflib.get_close_matches(property_name, all_props, n=3, cutoff=0.6)
        if suggestions:
            return f"❌ Property '{property_name}' not found. Did you mean: {', '.join(suggestions)}?"
        return f"❌ Property '{property_name}' not found."
    
    try:
        result = [f"🔧 Property Details: '{property_name}'"]
        
        # Add labels
        if hasattr(prop, 'label') and prop.label:
            labels = [str(label) for label in prop.label]
            result.append(f"📝 Label: {', '.join(sorted(set(labels)))}")
        
        # Add comments/definitions
        if hasattr(prop, 'comment') and prop.comment:
            comments = [str(comment) for comment in prop.comment]
            result.append(f"🗒️ Definition: {' | '.join(sorted(set(comments)))}")
        
        # Domain information
        if hasattr(prop, 'domain') and prop.domain:
            domain_names = [d.name for d in prop.domain if hasattr(d, 'name')]
            if domain_names:
                result.append(f"📥 Domain (applies to): {', '.join(sorted(set(domain_names)))}")
        
        # Range information
        if hasattr(prop, 'range') and prop.range:
            range_names = []
            for r in prop.range:
                if hasattr(r, 'name'):
                    range_names.append(r.name)
                else:
                    range_names.append(str(r))
            if range_names:
                result.append(f"📤 Range (values): {', '.join(sorted(set(range_names)))}")
        
        # Property type
        from owlready2 import ObjectProperty, DataProperty, FunctionalProperty
        prop_types = []
        if isinstance(prop, ObjectProperty):
            prop_types.append("Object Property")
        if isinstance(prop, DataProperty):
            prop_types.append("Data Property")
        if isinstance(prop, FunctionalProperty):
            prop_types.append("Functional")
        
        if prop_types:
            result.append(f"🏷️ Type: {', '.join(prop_types)}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error getting property details: {str(e)}"

def get_class_info(class_name):
    """Get comprehensive one-shot class summary"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"
    
    try:
        result = [f"📊 Comprehensive Info: '{class_name}'"]
        result.append("=" * 50)
        
        # Basic info
        if hasattr(cls, 'label') and cls.label:
            labels = [str(label) for label in cls.label]
            result.append(f"📝 Label: {', '.join(sorted(set(labels)))}")
        
        if hasattr(cls, 'comment') and cls.comment:
            comments = [str(comment) for comment in cls.comment]
            result.append(f"🗒️ Definition: {' | '.join(sorted(set(comments)))}")
        
        # Hierarchy
        supers = [c.name for c in cls.is_a if hasattr(c, 'name')]
        if supers:
            result.append(f"🔼 Direct parents: {', '.join(sorted(set(supers)))}")
        
        subs = [c.name for c in cls.subclasses() if hasattr(c, 'name')]
        if subs:
            result.append(f"🔽 Direct children: {', '.join(sorted(set(subs)))}")
        
        # Properties
        direct_props = []
        inherited_props = []
        
        for prop in onto.properties():
            if hasattr(prop, 'domain') and prop.domain:
                domains = set(prop.domain)
                if cls in domains:
                    direct_props.append(prop.name)
                elif any(cls in d.ancestors() for d in domains):
                    inherited_props.append(prop.name)
        
        if direct_props:
            result.append(f"🔧 Direct properties: {', '.join(sorted(set(direct_props)))}")
        
        if inherited_props:
            result.append(f"⬆️ Inherited properties: {', '.join(sorted(set(inherited_props)))}")
        
        # Related concepts (depth 1)
        related = []
        for parent in cls.is_a:
            if hasattr(parent, 'name'):
                for sibling in parent.subclasses():
                    if hasattr(sibling, 'name') and sibling.name != class_name:
                        related.append(sibling.name)
        
        if related:
            result.append(f"🔗 Related concepts: {', '.join(sorted(set(related))[:5])}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error getting class info: {str(e)}"

def get_all_superclasses(class_name):
    """Get complete inheritance chain (OWL transitive closure)"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"
    
    try:
        # Get all ancestors (transitive closure)
        ancestors = list(cls.ancestors())
        ancestor_names = [c.name for c in ancestors if hasattr(c, 'name')]
        
        if not ancestor_names:
            return f"ℹ️ No superclasses found for '{class_name}'"
        
        # Organize by inheritance level
        levels = {}
        current_level = [cls]
        level = 0
        
        while current_level:
            next_level = []
            for c in current_level:
                parents = [p for p in c.is_a if hasattr(p, 'name')]
                for parent in parents:
                    if parent not in next_level:
                        next_level.append(parent)
            
            if next_level:
                level += 1
                level_names = [c.name for c in next_level]
                levels[level] = sorted(set(level_names))
                current_level = next_level
            else:
                break
        
        result = [f"🔼 Complete inheritance chain for '{class_name}':"]
        
        for level_num in sorted(levels.keys()):
            names = levels[level_num]
            result.append(f"\n📍 Level {level_num} ({len(names)} classes):")
            for name in names:
                result.append(f"  📛 {name}")
        
        # Summary
        total_ancestors = len(set(ancestor_names))
        result.append(f"\n📊 Total ancestors: {total_ancestors}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error getting inheritance chain: {str(e)}"

def get_inferred_properties(class_name):
    """Get all properties inherited through the class hierarchy"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls = onto.search_one(iri="*" + class_name)
    if not cls:
        suggestion_msg = format_suggestions_message(class_name)
        return f"❌ Class '{class_name}' not found.\n{suggestion_msg}"
    
    try:
        # Get all ancestors to check for inherited properties
        ancestors = list(cls.ancestors())
        
        direct_props = []
        inherited_props = []
        
        for prop in onto.properties():
            if hasattr(prop, 'domain') and prop.domain:
                domains = set(prop.domain)
                
                # Check if property applies directly to this class
                if cls in domains:
                    direct_props.append(prop.name)
                # Check if property is inherited from ancestors
                elif any(ancestor in domains for ancestor in ancestors):
                    inherited_props.append(prop.name)
        
        result = [f"🔧 Property Inheritance for '{class_name}':"]
        
        if direct_props:
            result.append(f"\n📍 Direct properties ({len(direct_props)}):")
            for prop in sorted(set(direct_props)):
                result.append(f"  🔗 {prop}")
        
        if inherited_props:
            result.append(f"\n⬆️ Inherited properties ({len(inherited_props)}):")
            for prop in sorted(set(inherited_props)):
                result.append(f"  🔗 {prop} (inherited)")
        
        if not direct_props and not inherited_props:
            result.append("  ℹ️ No properties found (direct or inherited)")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error computing inherited properties for '{class_name}': {str(e)}"

def get_reasoning_chain(class1, class2):
    """Show the reasoning chain between two classes"""
    if onto is None:
        return "❌ No ontology loaded. Please load modules first."
    
    cls1 = onto.search_one(iri="*" + class1)
    cls2 = onto.search_one(iri="*" + class2)
    
    if not cls1:
        suggestion_msg = format_suggestions_message(class1)
        return f"❌ Class '{class1}' not found.\n{suggestion_msg}"
    if not cls2:
        suggestion_msg = format_suggestions_message(class2)
        return f"❌ Class '{class2}' not found.\n{suggestion_msg}"
    
    try:
        result = [f"🧠 Reasoning Chain between '{class1}' and '{class2}':"]
        
        # Check if there's a direct inheritance relationship
        if cls2 in cls1.ancestors():
            result.append(f"📈 '{class1}' IS-A '{class2}' (direct inheritance)")
        elif cls1 in cls2.ancestors():
            result.append(f"📉 '{class2}' IS-A '{class1}' (reverse inheritance)")
        else:
            # Check for common ancestors
            ancestors1 = set(cls1.ancestors())
            ancestors2 = set(cls2.ancestors())
            common = ancestors1.intersection(ancestors2)
            
            if common:
                common_names = [c.name for c in common if hasattr(c, 'name')]
                result.append(f"🌳 Common ancestors: {', '.join(sorted(common_names))}")
            else:
                result.append(f"❌ No direct inheritance relationship found")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error computing reasoning chain: {str(e)}"

# ========== INITIALIZATION ==========

# Initialize with core modules when run directly
if __name__ == "__main__":
    print("🚀 Initializing FIBO Ontology Tools...")
    load_result = load_fibo_modules("core")
    print(load_result)
    
    print("\n" + "="*60)
    print("🧪 EXPANDED FIBO ONTOLOGY TOOLS")
    print("="*60)
    
    # Show available module sets
    print(get_available_module_sets())
    
    # Show current stats
    print(f"\n{get_ontology_stats()}")
    
    # Show domain analysis
    print(f"\n{explore_fibo_domains()}")

# Force load on import for web UI
# if onto is None:
#    print("🔄 Auto-loading core modules for web UI...")
#    load_result = load_fibo_modules("core")
#   print(load_result)