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
        Get company profile with Smart Tiered Matching:
        Tier 1: Exact Match (Case-insensitive)
        Tier 2: Alias/Acronym Lookup
        Tier 3: Anchor Match (Name starts with input)
        Tier 4: Strict Fuzzy Match (Score > 0.85)
        
        Prevents "Substring Parasitism" (e.g., 'AZ' matching 'Amazon')
        """
        if not company_name:
            return None
        
        normalized_input = self._normalize_company_name(company_name)
        company_name_lower = company_name.lower()

        # --- TIER 1: EXACT MATCHES ---
        # Direct check
        if company_name in self.company_data:
            return self.company_data[company_name]
        
        # Case-insensitive check
        for key, value in self.company_data.items():
            if key.lower() == company_name_lower:
                return value

        # --- TIER 2: ALIAS & ACRONYM LOOKUP ---
        if normalized_input in self.company_aliases:
            canonical_name = self.company_aliases[normalized_input]
            if canonical_name in self.company_data:
                print(f"INFO: Alias match '{company_name}' -> '{canonical_name}'")
                return self.company_data[canonical_name]

        # --- TIER 3: ANCHOR MATCH (Starts With) ---
        # For small strings (AZ, HP), Anchor match is the safer minimum
        for key, value in self.company_data.items():
            norm_key = self._normalize_company_name(key)
            # Match if database name starts with input (e.g. 'Micro' -> 'Microsoft')
            # But ONLY if input is at least 3 chars OR it's a very clear anchor
            if norm_key.startswith(normalized_input):
                # Length Safety: Don't match 'AZ' to 'Amazon' (2 chars to 6 chars)
                # Max 2x length difference for anchor matches
                if len(norm_key) <= len(normalized_input) * 2 or len(normalized_input) >= 4:
                    print(f"INFO: Anchor match '{company_name}' to '{key}'")
                    return value

        # --- TIER 4: STRICT FUZZY MATCH ---
        # Skip for very short strings (under 3 chars) to avoid noise
        if len(normalized_input) >= 3:
            best_match = None
            best_score = 0.0
            threshold = 0.85 # Strict 85% for internal DB
            
            for key in self.company_data.keys():
                score = self._fuzzy_match_score(normalized_input, self._normalize_company_name(key))
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = key
            
            if best_match:
                print(f"INFO: Fuzzy matched '{company_name}' to '{best_match}' (score: {best_score:.2f})")
                return self.company_data[best_match]
        
        # TIER 5: LAST RESORT - SUBSTRING (Filtered for quality)
        # Only allow if the input is a large part of the result name
        # Fixes the AZ vs Amazon issue completely
        if len(normalized_input) >= 4: # Minimum length for substring matching
            for key, value in self.company_data.items():
                norm_key = self._normalize_company_name(key)
                if normalized_input in norm_key:
                    # Match only if input covers > 60% of the name
                    if len(normalized_input) / len(norm_key) >= 0.6:
                        return value
        
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
