backlog_items = [
    {
        "title": "Add get_properties(class_name)",
        "description": "Allow the agent to list object/data properties of a given class.",
        "criteria": "As a user, when I ask 'What are the properties of ShareholdersEquity?', I see a list like hasOwner, isReportedAs."
    },
    {
        "title": "Improve fuzzy matching with suggestions",
        "description": "If fuzzy match fails, offer suggestions for close matches.",
        "criteria": "As a user, when I type 'ShareholderEquity', I get 'Did you mean ShareholdersEquity?'."
    },
    {
        "title": "Create a get_class_info(class_name) tool",
        "description": "Provide a one-shot summary of label, superclasses, subclasses, and comments.",
        "criteria": "As a user, I can ask 'Tell me about RetainedEarnings' and get a semantic summary."
    },
    {
        "title": "Implement class existence check",
        "description": "Add a utility to test class existence and fallback suggestions.",
        "criteria": "Invalid class names like 'OwnersEquit' are caught and suggestions offered."
    },
    {
        "title": "Allow LLM to return multiple tool calls (multi-step plan)",
        "description": "Enable the planner to return a sequence of calls.",
        "criteria": "As a user, I can ask 'Get the parent and children of ShareholdersEquity' and receive both outputs."
    },
    {
        "title": "Log all user inputs and plans to a session file",
        "description": "Maintain a log of user prompts, LLM plans, and results for audit/debug.",
        "criteria": "Log file 'logs/fibo_session.log' contains timestamped entries."
    },
    {
        "title": "Expose planner via a simple web UI",
        "description": "Build a minimal Flask or Streamlit app with a text input and result output.",
        "criteria": "As a user, I can ask questions via browser instead of CLI."
    },
    {
        "title": "Enable switching between FIBO modules (dynamic load)",
        "description": "Let users load different RDF modules from a list or directory scan.",
        "criteria": "I can say 'Load AccountingEquity' and the correct ontology is loaded."
    },
    {
        "title": "Add get_all_superclasses(class_name)",
        "description": "Return the full superclass chain (transitive closure).",
        "criteria": "As a user, I can ask 'Show inheritance of CapitalSurplus' and see the complete path."
    },
    {
        "title": "Run automated test battery and output pass/fail",
        "description": "Run a structured set of tests and validate responses.",
        "criteria": "A summary shows '8 passed / 2 failed' after executing test cases."
    }
]

file_path = "backlog.md"

with open(file_path, "w") as f:
    f.write("# FIBO Semantic Agent Backlog\n\n")
    for i, item in enumerate(backlog_items, 1):
        f.write(f"### {i}. {item['title']}\n")
        f.write(f"**Description**: {item['description']}\n\n")
        f.write(f"**Acceptance Criteria**: {item['criteria']}\n\n")

print(f"✅ Backlog written to {file_path}")
