import json
from memory.memory_manager import MemoryManager

class JSONAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def process_json(self, content: str, source_name: str):
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON"}

        required_fields = ["id", "date", "amount", "sender"]
        missing = [field for field in required_fields if field not in data]

        self.memory.log({
            "source": source_name,
            "json_data": data,
            "missing_fields": missing
        })

        return {"parsed": data, "missing_fields": missing}
