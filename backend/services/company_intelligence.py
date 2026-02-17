"""
Company Intelligence Service
Loads and provides company-specific interview intelligence from curated database
"""

import json
import os
from typing import Optional, Dict, Any, Tuple
from difflib import SequenceMatcher

class CompanyIntelligenceService:
    def __init__(self):
        self.company_data = {}
        self.company_aliases = {}  # Common name variations
        self.load_company_profiles()
        self._build_aliases()
    
    def load_company_profiles(self):
        """Load company profiles from JSON database"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', 'data', 'company_profiles.json')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.company_data = data.get('companies', {})
                print(f"INFO: Loaded {len(self.company_data)} company profiles")
        except FileNotFoundError:
            print("WARNING: Company profiles database not found. Using AI fallback only.")
            self.company_data = {}
        except Exception as e:
            print(f"ERROR: Error loading company profiles: {e}")
            self.company_data = {}
    
    def _build_aliases(self):
        """Build common company name aliases for better matching"""
        self.company_aliases = {
            # Common variations
            "fb": "Meta",
            "facebook": "Meta",
            "meta platforms": "Meta",
            "google deepmind": "Google DeepMind",
            "deep mind": "Google DeepMind",
            "openai": "OpenAI",
            "open ai": "OpenAI",
            "anthropic ai": "Anthropic",
            "claude": "Anthropic",
            "stability": "Stability AI",
            "stable diffusion": "Stability AI",
            "huggingface": "Hugging Face",
            "hugging face": "Hugging Face",
            "hf": "Hugging Face",
            "character ai": "Character.AI",
            "characterai": "Character.AI",
            "perplexity": "Perplexity AI",
            "scale": "Scale AI",
            "scaleai": "Scale AI",
            "jpmorgan": "JPMorgan Chase",
            "jp morgan": "JPMorgan Chase",
            "goldman": "Goldman Sachs",
            "morgan stanley": "Morgan Stanley",
            "ms": "Morgan Stanley",
            "gs": "Goldman Sachs",
            "mckinsey": "McKinsey & Company",
            "bcg": "Boston Consulting Group",
            "bain": "Bain & Company",
            "pwc": "PwC (PricewaterhouseCoopers)",
            "pricewaterhousecoopers": "PwC (PricewaterhouseCoopers)",
            "kpmg": "KPMG",
            "ey": "Deloitte",  # Placeholder, add EY if needed
            "tata consultancy": "TCS",
            "tata consultancy services": "TCS",
            "wipro technologies": "Wipro",
            "infosys technologies": "Infosys",
            "hashicorp": "HashiCorp",
            "grafana": "Grafana Labs",
            "grafana labs": "Grafana Labs",
        }
    
    def _normalize_company_name(self, name: str) -> str:
        """Normalize company name for matching"""
        if not name:
            return ""
        
        # Remove common suffixes and normalize
        normalized = name.lower().strip()
        
        # Remove common company suffixes
        suffixes = [" inc", " inc.", " corp", " corp.", " ltd", " ltd.", 
                   " llc", " llc.", " company", " co.", " co"]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()
        
        # Remove special characters but keep spaces
        normalized = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in normalized)
        normalized = ' '.join(normalized.split())  # Remove extra spaces
        
        return normalized
    
    def _fuzzy_match_score(self, str1: str, str2: str) -> float:
        """Calculate fuzzy match score between two strings (0.0 to 1.0)"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def get_company_profile(self, company_name: str) -> Optional[Dict[str, Any]]:
        """
        Get company profile by name with fuzzy matching
        
        Handles:
        - Case variations: "google", "GOOGLE", "Google"
        - Typos: "gogle", "googel" 
        - Spacing: "open ai", "openai"
        - Common aliases: "fb" -> "Meta", "claude" -> "Anthropic"
        
        Args:
            company_name: Name of the company
        
        Returns:
            Company profile dict or None if not found
        """
        if not company_name:
            return None
        
        # Normalize input
        normalized_input = self._normalize_company_name(company_name)
        
        # 1. Try exact match first (fastest)
        if company_name in self.company_data:
            return self.company_data[company_name]
        
        # 2. Try alias lookup
        if normalized_input in self.company_aliases:
            canonical_name = self.company_aliases[normalized_input]
            if canonical_name in self.company_data:
                return self.company_data[canonical_name]
        
        # 3. Try case-insensitive exact match
        company_name_lower = company_name.lower()
        for key, value in self.company_data.items():
            if key.lower() == company_name_lower:
                return value
        
        # 4. Try normalized exact match
        for key, value in self.company_data.items():
            if self._normalize_company_name(key) == normalized_input:
                return value
        
        # 5. Try partial match (e.g., "Facebook" in "Meta")
        for key, value in self.company_data.items():
            key_lower = key.lower()
            if normalized_input in key_lower or key_lower in normalized_input:
                return value
        
        # 6. Fuzzy match (for typos) - find best match above threshold
        best_match = None
        best_score = 0.0
        threshold = 0.75  # 75% similarity required
        
        for key in self.company_data.keys():
            score = self._fuzzy_match_score(normalized_input, self._normalize_company_name(key))
            if score > best_score and score >= threshold:
                best_score = score
                best_match = key
        
        if best_match:
            print(f"INFO: Fuzzy matched '{company_name}' to '{best_match}' (score: {best_score:.2f})")
            return self.company_data[best_match]
        
        return None
    
    def get_interview_context(self, company_name: str, round_name: str = "Technical") -> str:
        """
        Generate rich interview context for AI prompt
        
        Args:
            company_name: Target company name
            round_name: Interview round (Technical, Behavioral, System Design, etc.)
        
        Returns:
            Formatted context string for AI prompt
        """
        profile = self.get_company_profile(company_name)
        
        if not profile:
            return f"Simulate a professional {round_name} interview for {company_name}."
        
        # Build rich context
        context_parts = []
        
        # Company overview
        context_parts.append(f"COMPANY: {profile['name']} ({profile['industry']}, {profile['size']})")
        context_parts.append(f"INTERVIEW DIFFICULTY: {profile['difficulty_level']}")
        context_parts.append(f"INTERVIEW STYLE: {profile['interview_style']}")
        
        # Cultural values
        if profile.get('cultural_values'):
            values_str = ", ".join(profile['cultural_values'][:3])  # Top 3 values
            context_parts.append(f"CORE VALUES: {values_str}")
        
        # Round-specific intelligence
        round_info = profile.get('interview_rounds', {}).get(round_name, {})
        if round_info:
            context_parts.append(f"\n{round_name.upper()} ROUND FOCUS:")
            context_parts.append(f"- Primary Focus: {round_info.get('focus', 'General assessment')}")
            
            if round_info.get('common_topics'):
                topics = ", ".join(round_info['common_topics'][:3])
                context_parts.append(f"- Common Topics: {topics}")
            
            if round_info.get('style'):
                context_parts.append(f"- Interview Style: {round_info['style']}")
            
            if round_info.get('tips'):
                context_parts.append(f"- Key Tips: {round_info['tips']}")
            
            if round_info.get('common_questions'):
                context_parts.append(f"- Example Questions: {round_info['common_questions'][0]}")
        
        # Red flags
        if profile.get('red_flags'):
            flags = ", ".join(profile['red_flags'][:2])
            context_parts.append(f"\nRED FLAGS TO WATCH: {flags}")
        
        return "\n".join(context_parts)
    
    def get_behavioral_questions(self, company_name: str) -> list:
        """Get company-specific behavioral questions"""
        profile = self.get_company_profile(company_name)
        if not profile:
            return []
        
        behavioral_round = profile.get('interview_rounds', {}).get('Behavioral', {})
        return behavioral_round.get('common_questions', [])
    
    def get_cultural_values(self, company_name: str) -> list:
        """Get company's cultural values"""
        profile = self.get_company_profile(company_name)
        if not profile:
            return []
        
        return profile.get('cultural_values', [])
    
    def is_company_in_database(self, company_name: str) -> bool:
        """Check if company exists in database"""
        return self.get_company_profile(company_name) is not None
    
    def get_all_companies(self) -> list:
        """Get list of all companies in database"""
        return list(self.company_data.keys())
    
    def get_company_count(self) -> int:
        """Get total number of companies in database"""
        return len(self.company_data)


# Singleton instance
_company_intelligence = None

def get_company_intelligence() -> CompanyIntelligenceService:
    """Get singleton instance of CompanyIntelligenceService"""
    global _company_intelligence
    if _company_intelligence is None:
        _company_intelligence = CompanyIntelligenceService()
    return _company_intelligence
