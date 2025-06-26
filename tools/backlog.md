
### Add ontology reasoning (sync_reasoner)
**Description**: Use OWLReady2's sync_reasoner to infer class relationships and validate logical structure.

**Acceptance Criteria**: As a user, I can ask 'What is inferred about ShareholdersEquity?' and receive facts that were not explicitly stated.


### Add class consistency checker
**Description**: Check whether the ontology is logically consistent after loading all modules.

**Acceptance Criteria**: A CLI or tool call reports if the ontology is consistent or contains logical contradictions.


### Add class explanation tool
**Description**: Generate a textual explanation of a class using labels, comments, structure, and optional LLM refinement.

**Acceptance Criteria**: I can ask 'Explain OwnersEquity' and get a readable summary with context and usage.


### Support DL-style queries
**Description**: Add basic support for Description Logic queries (e.g., ∃ hasOwner.⊤).

**Acceptance Criteria**: User can enter a DL pattern and receive matching classes.


### Add LLM-based generalization/induction tool
**Description**: Use an LLM to suggest generalized patterns from example class/property combinations.

**Acceptance Criteria**: User can provide 2–3 facts and the LLM responds with a candidate generalization.


### Support multi-hop reasoning plans
**Description**: Let the planner return a sequence of function calls (e.g., superclass then its properties).

**Acceptance Criteria**: A single question like 'What can you tell me about the parent of ShareholdersEquity?' results in two chained tool calls.


### Add natural language to RDF triple generation
**Description**: Allow user to enter statements like 'X owns Y' and receive corresponding RDF subject-predicate-object.

**Acceptance Criteria**: User input is translated to a triple via LLM, confirmed with candidate class/property matching.


### Add semantic clustering of properties or classes via LLM
**Description**: Use an LLM to group related classes or properties by usage patterns.

**Acceptance Criteria**: Given a set of class names, the tool returns clusters or labels based on shared semantics.


### Add equivalent class detection tool
**Description**: Expose any declared or inferred owl:equivalentClass relations in the ontology.

**Acceptance Criteria**: User can call 'get_equivalent_classes("Corporation")' and see matching equivalents.


### Add fuzzy relationship query support
**Description**: Allow user to ask for relations like 'things that can own something', and return matching properties.

**Acceptance Criteria**: LLM maps vague relation prompts to real ontology properties based on name/domain patterns.


### Add ontology reasoning (sync_reasoner)
**Description**: Use OWLReady2's sync_reasoner to infer class relationships and validate logical structure.

**Acceptance Criteria**: As a user, I can ask 'What is inferred about ShareholdersEquity?' and receive facts that were not explicitly stated.


### Add class consistency checker
**Description**: Check whether the ontology is logically consistent after loading all modules.

**Acceptance Criteria**: A CLI or tool call reports if the ontology is consistent or contains logical contradictions.


### Add class explanation tool
**Description**: Generate a textual explanation of a class using labels, comments, structure, and optional LLM refinement.

**Acceptance Criteria**: I can ask 'Explain OwnersEquity' and get a readable summary with context and usage.


### Support DL-style queries
**Description**: Add basic support for Description Logic queries (e.g., ∃ hasOwner.⊤).

**Acceptance Criteria**: User can enter a DL pattern and receive matching classes.


### Add LLM-based generalization/induction tool
**Description**: Use an LLM to suggest generalized patterns from example class/property combinations.

**Acceptance Criteria**: User can provide 2–3 facts and the LLM responds with a candidate generalization.


### Support multi-hop reasoning plans
**Description**: Let the planner return a sequence of function calls (e.g., superclass then its properties).

**Acceptance Criteria**: A single question like 'What can you tell me about the parent of ShareholdersEquity?' results in two chained tool calls.


### Add natural language to RDF triple generation
**Description**: Allow user to enter statements like 'X owns Y' and receive corresponding RDF subject-predicate-object.

**Acceptance Criteria**: User input is translated to a triple via LLM, confirmed with candidate class/property matching.


### Add semantic clustering of properties or classes via LLM
**Description**: Use an LLM to group related classes or properties by usage patterns.

**Acceptance Criteria**: Given a set of class names, the tool returns clusters or labels based on shared semantics.


### Add equivalent class detection tool
**Description**: Expose any declared or inferred owl:equivalentClass relations in the ontology.

**Acceptance Criteria**: User can call 'get_equivalent_classes("Corporation")' and see matching equivalents.


### Add fuzzy relationship query support
**Description**: Allow user to ask for relations like 'things that can own something', and return matching properties.

**Acceptance Criteria**: LLM maps vague relation prompts to real ontology properties based on name/domain patterns.

