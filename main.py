from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.memory_manager import MemoryManager
from utils.file_loader import load_file

if __name__ == "__main__":
    # Specify the input file path for CLI processing (can be changed as needed)
    file_path = "examples/sample_email.txt"  
    # e.g., use "examples/sample_invoice.json" or "examples/sample_complaint.pdf" to test other types

    # Determine the file extension
    file_extension = file_path.split(".")[-1].lower()

    # Load the file content (handles PDFs and text files accordingly)
    try:
        content = load_file(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        exit(1)

    # Initialize shared memory and agents
    memory = MemoryManager()
    classifier = ClassifierAgent(memory)
    email_agent = EmailAgent(memory)
    json_agent = JSONAgent(memory)

    # Classify the document and print the results
    doc_format, intent = classifier.classify_and_route(content, file_extension, source_name=file_path)
    print(f"Document Format: {doc_format}")
    print(f"Detected Intent: {intent}")

    # Route to the appropriate agent and print additional processing (if any)
    if doc_format == "Email":
        email_result = email_agent.process_email(content, file_path)
        print("Email Metadata:", email_result)
    elif doc_format == "JSON":
        json_result = json_agent.process_json(content, file_path)
        print("JSON Parse Result:", json_result)
    # For PDF or other formats, no further CLI processing is implemented beyond classification.
    else:
        print("No specialized processing for this document format in CLI mode.")