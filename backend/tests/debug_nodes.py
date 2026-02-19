import os
import json
import asyncio
from services.intelligence_service import get_intelligence_service

async def debug_agent():
    print("DEBUG: Starting...")
    service = get_intelligence_service()
    
    # Check singleton
    print(f"DEBUG: Service initialized: {service is not None}")
    
    # State initialization
    state = {
        "company_name": "OpenAI",
        "industry": None,
        "research_data": "OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence benefits all of humanity.",
        "generated_profile": None,
        "is_valid": False,
        "iterations": 0,
        "error": None
    }
    
    print("DEBUG: Testing architect_node...")
    try:
        arch_state = await service.architect_node(state)
        print(f"DEBUG: Generated Profile keys: {list(arch_state['generated_profile'].keys()) if arch_state['generated_profile'] else None}")
    except Exception as e:
        print(f"DEBUG: architect_node failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_agent())
