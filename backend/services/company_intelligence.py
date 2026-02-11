"""
Company Intelligence Service
Loads and provides company-specific interview intelligence from curated database
"""

import json
import os
from typing import Optional, Dict, Any

class CompanyIntelligenceService:
    def __init__(self):
        self.company_data = {}
        self.load_company_profiles()
    
    def load_company_profiles(self):
        """Load company profiles from JSON database"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', 'data', 'company_profiles.json')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.company_data = data.get('companies', {})
                print(f"✅ Loaded {len(self.company_data)} company profiles")
        except FileNotFoundError:
            print("⚠️ Company profiles database not found. Using AI fallback only.")
            self.company_data = {}
        except Exception as e:
            print(f"⚠️ Error loading company profiles: {e}")
            self.company_data = {}
    
    def get_company_profile(self, company_name: str) -> Optional[Dict[str, Any]]:
        """
        Get company profile by name (case-insensitive)
        
        Args:
            company_name: Name of the company (e.g., "Google", "google", "GOOGLE")
        
        Returns:
            Company profile dict or None if not found
        """
        if not company_name:
            return None
        
        # Try exact match first
        if company_name in self.company_data:
            return self.company_data[company_name]
        
        # Try case-insensitive match
        company_name_lower = company_name.lower()
        for key, value in self.company_data.items():
            if key.lower() == company_name_lower:
                return value
        
        # Try partial match (e.g., "Facebook" matches "Meta (Facebook)")
        for key, value in self.company_data.items():
            if company_name_lower in key.lower() or key.lower() in company_name_lower:
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
