from tools.ontology_tools import get_superclasses

def test_superclasses():
    print("Testing get_superclasses('Shares'):")
    result = get_superclasses("Shares")
    print(result)

if __name__ == "__main__":
    test_superclasses()
