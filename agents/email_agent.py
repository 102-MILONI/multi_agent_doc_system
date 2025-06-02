import re
from memory.memory_manager import MemoryManager

class EmailAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def process_email(self, content: str, source_name: str):
        sender_match = re.search(r"From:\s*(.*)", content, flags=re.IGNORECASE)
        sender = sender_match.group(1).strip() if sender_match else "Unknown"

        urgency = "High" if "urgent" in content.lower() else "Normal"

        intent_keywords = ["invoice", "rfq", "complaint", "regulation"]
        intent = next((kw.capitalize() for kw in intent_keywords if kw in content.lower()), "Unknown")

        result = {
            "sender": sender,
            "urgency": urgency,
            "intent": intent
        }

        self.memory.log({
            "source": source_name,
            "email_meta": result
        })

        return result
