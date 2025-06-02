from agents.classifier_agent import ClassifierAgent
from memory.memory_manager import MemoryManager

def test_classifier():
    # Use a temporary memory store for testing to avoid side effects
    memory = MemoryManager(path="memory/test_memory.json")
    agent = ClassifierAgent(memory)
    sample_text = "We need a quotation for new server units."

    format_type = agent.detect_format("txt")        # should detect as Email by extension
    intent = agent.detect_intent(sample_text)       # should return one of the known labels

    assert format_type == "Email", "Expected format to be Email for .txt files"
    assert intent in ["RFQ", "Invoice", "Complaint", "Regulation"], \
           "Intent should be one of the predefined labels (Invoice, RFQ, Complaint, Regulation)"
    assert memory.get("format") == "Email", "Memory should store the detected format"
    assert memory.get("intent") == intent, "Memory should store the detected intent"