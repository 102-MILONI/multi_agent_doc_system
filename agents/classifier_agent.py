from transformers import pipeline
from utils.file_loader import detect_format
from memory.memory_manager import MemoryManager

class ClassifierAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.intent_labels = ["Invoice", "RFQ", "Complaint", "Regulation"]

    def classify_and_route(self, content: str, extension: str, source_name: str):
        format_type = detect_format(extension, content)

        if not content.strip():
            return format_type, "Unknown"

        result = self.pipe(content, self.intent_labels)
        intent = result["labels"][0]

        self.memory.log({
            "source": source_name,
            "type": format_type,
            "intent": intent
        })

        return format_type, intent

    def detect_format(self, extension: str, content: str = ""):
        return detect_format(extension, content)

    def detect_intent(self, content: str):
        result = self.pipe(content, self.intent_labels)
        return result["labels"][0]
