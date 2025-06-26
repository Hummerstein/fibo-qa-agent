# FIBO Semantic Agent Backlog

### 1. Add get_properties(class_name)
**Description**: Allow the agent to list object/data properties of a given class.

**Acceptance Criteria**: As a user, when I ask 'What are the properties of ShareholdersEquity?', I see a list like hasOwner, isReportedAs.

### 2. Improve fuzzy matching with suggestions
**Description**: If fuzzy match fails, offer suggestions for close matches.

**Acceptance Criteria**: As a user, when I type 'ShareholderEquity', I get 'Did you mean ShareholdersEquity?'.

### 3. Create a get_class_info(class_name) tool
**Description**: Provide a one-shot summary of label, superclasses, subclasses, and comments.

**Acceptance Criteria**: As a user, I can ask 'Tell me about RetainedEarnings' and get a semantic summary.

### 4. Implement class existence check
**Description**: Add a utility to test class existence and fallback suggestions.

**Acceptance Criteria**: Invalid class names like 'OwnersEquit' are caught and suggestions offered.

### 5. Allow LLM to return multiple tool calls (multi-step plan)
**Description**: Enable the planner to return a sequence of calls.

**Acceptance Criteria**: As a user, I can ask 'Get the parent and children of ShareholdersEquity' and receive both outputs.

### 6. Log all user inputs and plans to a session file
**Description**: Maintain a log of user prompts, LLM plans, and results for audit/debug.

**Acceptance Criteria**: Log file 'logs/fibo_session.log' contains timestamped entries.

### 7. Expose planner via a simple web UI
**Description**: Build a minimal Flask or Streamlit app with a text input and result output.

**Acceptance Criteria**: As a user, I can ask questions via browser instead of CLI.

### 8. Enable switching between FIBO modules (dynamic load)
**Description**: Let users load different RDF modules from a list or directory scan.

**Acceptance Criteria**: I can say 'Load AccountingEquity' and the correct ontology is loaded.

### 9. Add get_all_superclasses(class_name)
**Description**: Return the full superclass chain (transitive closure).

**Acceptance Criteria**: As a user, I can ask 'Show inheritance of CapitalSurplus' and see the complete path.

### 10. Run automated test battery and output pass/fail
**Description**: Run a structured set of tests and validate responses.

**Acceptance Criteria**: A summary shows '8 passed / 2 failed' after executing test cases.

