import json
import os
from datetime import datetime


class ResearchMemory:

    def __init__(self, file_path="memory/research_history.json"):
        self.file_path = file_path

        os.makedirs("memory", exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def save_session(self, query, report, sources, evaluation):

        session = {
            "query": query,
            "report": report,
            "sources": sources,
            "evaluation": evaluation,
            "timestamp": datetime.utcnow().isoformat()
        }

        with open(self.file_path, "r") as f:
            history = json.load(f)

        history.append(session)

        with open(self.file_path, "w") as f:
            json.dump(history, f, indent=2)

    def load_history(self):

        with open(self.file_path, "r") as f:
            return json.load(f)
        