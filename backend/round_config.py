# Round Configuration for Multi-Round Interview System

ROUND_DEFINITIONS = {
    1: {
        "name": "Technical",
        "description": "Technical screening and problem-solving",
        "min_questions": 5,
        "max_questions": 10,
        "pass_score": 6.0,
        "applicable_roles": "all"
    },
    2: {
        "name": "Behavioral",
        "description": "HR and behavioral assessment",
        "min_questions": 5,
        "max_questions": 8,
        "pass_score": 6.5,
        "applicable_roles": "all"
    },
    3: {
        "name": "System Design",
        "description": "Architecture and scalability discussion",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 7.0,
        "applicable_roles": ["Engineering & Tech"]
    },
    4: {
        "name": "Managerial",
        "description": "Leadership and team management",
        "min_questions": 4,
        "max_questions": 6,
        "pass_score": 7.0,
        "applicable_roles": ["Business & Management", "Engineering & Tech"]
    },
    5: {
        "name": "Final",
        "description": "Director/VP level discussion",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 7.5,
        "applicable_roles": "all"
    }
}

# Determine which rounds apply based on role and difficulty
def get_applicable_rounds(role_category: str, difficulty_level: int):
    """
    Returns list of round numbers applicable for this interview
    
    Args:
        role_category: e.g., "Engineering & Tech", "Healthcare & Medical"
        difficulty_level: 1 (Junior), 2 (Mid), 3 (Senior)
    
    Returns:
        List of round numbers: [1, 2, 3, 4, 5]
    """
    rounds = [1, 2]  # Everyone gets Technical + Behavioral
    
    # Add System Design for technical roles (Mid and Senior)
    if role_category == "Engineering & Tech" and difficulty_level >= 2:
        rounds.append(3)
    
    # Add Managerial round for Senior level
    if difficulty_level == 3:
        rounds.append(4)
    
    # Add Final round for Senior level
    if difficulty_level == 3:
        rounds.append(5)
    
    return rounds

def get_next_round(current_round: int, role_category: str, difficulty_level: int):
    """
    Determines the next round number
    
    Returns:
        Next round number or None if interview is complete
    """
    applicable_rounds = get_applicable_rounds(role_category, difficulty_level)
    
    if current_round in applicable_rounds:
        current_index = applicable_rounds.index(current_round)
        if current_index + 1 < len(applicable_rounds):
            return applicable_rounds[current_index + 1]
    
    return None  # No more rounds

def should_proceed_to_next_round(score: float, current_round: int):
    """
    Determines if candidate passed current round
    
    Args:
        score: Score achieved in current round (0-10)
        current_round: Round number (1-5)
    
    Returns:
        Boolean: True if passed, False if failed
    """
    round_config = ROUND_DEFINITIONS.get(current_round)
    if not round_config:
        return False
    
    return score >= round_config["pass_score"]
