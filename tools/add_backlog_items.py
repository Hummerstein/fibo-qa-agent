from pathlib import Path

backlog_path = Path("backlog.md")

new_items = [
    {
        "title": "Add ontology reasoning (sync_reasoner)",
        "description": "Use OWLReady2's sync_reasoner to infer class relationships and validate logical structure.",
        "criteria": "As a user, I can ask 'What is inferred about ShareholdersEquity?' and receive facts that were not explicitly stated."
    },
    {
        "title": "Add class consistency checker",
        "description": "Check whether the ontology is logically consistent after loading all modules.",
        "criteria": "A CLI or tool call reports if the ontology is consistent or contains logical contradictions."
    },
    {
        "title": "Add class explanation tool",
        "description": "Generate a textual explanation of a class using labels, comments, structure, and optional LLM refinement.",
        "criteria": "I can ask 'Explain OwnersEquity' and get a readable summary with context and usage."
    },
    {
        "title": "Support DL-style queries",
        "description": "Add basic support for Description Logic queries (e.g., ∃ hasOwner.⊤).",
        "criteria": "User can enter a DL pattern and receive matching classes."
    },
    {
        "title": "Add LLM-based generalization/induction tool",
        "description": "Use an LLM to suggest generalized patterns from example class/property combinations.",
        "criteria": "User can provide 2–3 facts and the LLM responds with a candidate generalization."
    },
    {
        "title": "Support multi-hop reasoning plans",
        "description": "Let the planner return a sequence of function calls (e.g., superclass then its properties).",
        "criteria": "A single question like 'What can you tell me about the parent of ShareholdersEquity?' results in two chained tool calls."
    },
    {
        "title": "Add natural language to RDF triple generation",
        "description": "Allow user to enter statements like 'X owns Y' and receive corresponding RDF subject-predicate-object.",
        "criteria": "User input is translated to a triple via LLM, confirmed with candidate class/property matching."
    },
    {
        "title": "Add semantic clustering of properties or classes via LLM",
        "description": "Use an LLM to group related classes or properties by usage patterns.",
        "criteria": "Given a set of class names, the tool returns clusters or labels based on shared semantics."
    },
    {
        "title": "Add equivalent class detection tool",
        "description": "Expose any declared or inferred owl:equivalentClass relations in the ontology.",
        "criteria": "User can call 'get_equivalent_classes(\"Corporation\")' and see matching equivalents."
    },
    {
        "title": "Add fuzzy relationship query support",
        "description": "Allow user to ask for relations like 'things that can own something', and return matching properties.",
        "criteria": "LLM maps vague relation prompts to real ontology properties based on name/domain patterns."
    }
]

with open(backlog_path, "a") as f:
    for i, item in enumerate(new_items, 1):
        f.write(f"\n### {item['title']}\n")
        f.write(f"**Description**: {item['description']}\n\n")
        f.write(f"**Acceptance Criteria**: {item['criteria']}\n\n")
f"✅ Added {len(new_items)} new items to backlog.md"
