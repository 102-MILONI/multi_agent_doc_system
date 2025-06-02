import json
import os
import csv
from datetime import datetime

class MemoryManager:
    def __init__(self, path: str = "memory/memory_store.json"):
        self.path = path
        self.csv_path = "memory/memory_export.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def log(self, data: dict):
        data["timestamp"] = datetime.utcnow().isoformat()
        memory = self.get_memory()
        memory.append(data)
        with open(self.path, "w") as f:
            json.dump(memory, f, indent=4)
        self._append_to_csv(data)

    def get_memory(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            with open(self.path, "w") as f:
                json.dump([], f)
            return []

    def _append_to_csv(self, data):
        flat = {
            "source": data.get("source", ""),
            "type": data.get("type", ""),
            "intent": data.get("intent", ""),
            "timestamp": data.get("timestamp", ""),
            "meta": json.dumps(data.get("json_data") or data.get("email_meta") or {})
        }
        write_header = not os.path.exists(self.csv_path)
        with open(self.csv_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flat.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(flat)
