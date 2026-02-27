import json
import os
from datetime import datetime

class MemoryService:
    def __init__(self, registry_path="data/stealth_registry.json"):
        # Use absolute path based on project root if needed
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.registry_path = os.path.join(base_dir, registry_path)
        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, 'w') as f:
                json.dump({}, f)

    def _load_registry(self):
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_registry(self, data):
        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=4)

    async def learn_from_session(self, session_data: dict, evaluation_data: dict):
        """
        Learns from a finished session. 
        Implements Witness vs Expert logic:
        - Structural Data: Trusted from persistent users (Strugglers).
        - Quality Data: Trusted from high-performers (Experts).
        """
        company_name = session_data.get("target_company")
        if not company_name or company_name.lower() in ["none", "na", "null", ""]:
            return

        registry = self._load_registry()
        
        # Normailze key
        key = company_name.strip().title()
        
        if key not in registry:
            registry[key] = {
                "name": key,
                "hit_count": 0,
                "domain": session_data.get("role_category"),
                "interview_style": "Undetermined",
                "cultural_values": [],
                "interview_rounds": {},
                "last_updated": datetime.now().isoformat(),
                "consensus_score": 0.0,
                "vetted": False
            }

        entry = registry[key]
        entry["hit_count"] += 1
        
        # 1. Structural Learning (Rounds) - Trusted if consistent
        current_rounds = session_data.get("rounds_completed", [])
        if current_rounds:
            # Simple consensus: Keep the longest observed sequence or merge
            # For now, we update the roadmap if we find a more detailed one
            entry["interview_rounds_sequence"] = current_rounds
            
        # 2. Performance Feedback (Expert Logic)
        score = session_data.get("score", 0)
        vibe_score = evaluation_data.get("vibe_analysis", {}).get("confidence_score", 5)
        
        # If user is a "High Performer", update the values and style
        if score >= 7.5 and vibe_score >= 7:
            entry["interview_style"] = evaluation_data.get("feedback", entry["interview_style"])[:100] # Snippet
            # Add cultural tokens if found in feedback
            if "culture" in evaluation_data.get("feedback", "").lower():
                entry["cultural_values"].append("High Performance")
                
        # 3. Frequency Update
        entry["last_updated"] = datetime.now().isoformat()
        
        # Promotion Logic: If hit count > 5, mark as "Vetted Candidate Intel"
        if entry["hit_count"] >= 5:
            entry["vetted"] = True
            
        registry[key] = entry
        self._save_registry(registry)
        print(f"LOG: MemoryService learned new details for {key}")

    async def get_stealth_intelligence(self, company_name: str):
        """Retrieves user-contributed intelligence if available."""
        registry = self._load_registry()
        key = company_name.strip().title()
        return registry.get(key)

# Singleton
_memory_instance = None

def get_memory_service():
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryService()
    return _memory_instance
