# ============================================================
# Domain-Aware Round Configuration — InterviewAI v2.3
# ============================================================
# Each domain has its own round sequence per difficulty level.
# Rounds are referenced by NAME (string), not integers.
# ============================================================

# --- Round Type Definitions ---
# Each entry defines properties for a round type.
ROUND_DEFINITIONS = {
    "Technical": {
        "description": "Coding, algorithms, data structures, and technical problem-solving.",
        "min_questions": 5,
        "max_questions": 10,
        "pass_score": 6.0,
    },
    "System Design": {
        "description": "Software architecture, scalability, distributed systems, trade-offs.",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 7.0,
    },
    "Domain Knowledge": {
        "description": "Role-specific theoretical and practical knowledge assessment.",
        "min_questions": 4,
        "max_questions": 8,
        "pass_score": 6.0,
    },
    "Case Study": {
        "description": "Structured problem analysis, business/legal/financial case discussion.",
        "min_questions": 2,
        "max_questions": 4,
        "pass_score": 6.5,
    },
    "Situational": {
        "description": "Scenario-based questions testing real-world judgment and decision-making.",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 6.0,
    },
    "Role Play": {
        "description": "Simulated client pitch, negotiation, or sales interaction.",
        "min_questions": 2,
        "max_questions": 4,
        "pass_score": 6.0,
    },
    "Practical Assessment": {
        "description": "Hands-on task, demo lesson, site assessment, or skills test.",
        "min_questions": 2,
        "max_questions": 4,
        "pass_score": 6.5,
    },
    "Portfolio Review": {
        "description": "Walkthrough and discussion of creative work, design portfolio, or past projects.",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 6.0,
    },
    "Technical Presentation": {
        "description": "Research methodology presentation or scientific approach discussion.",
        "min_questions": 2,
        "max_questions": 4,
        "pass_score": 6.5,
    },
    "Behavioral": {
        "description": "STAR-method HR and behavioral assessment — soft skills, culture fit.",
        "min_questions": 4,
        "max_questions": 8,
        "pass_score": 6.5,
    },
    "Managerial": {
        "description": "Leadership, team management, conflict resolution, and strategic thinking.",
        "min_questions": 3,
        "max_questions": 5,
        "pass_score": 7.0,
    },
    "Final": {
        "description": "Director/VP/Partner-level vision, long-term thinking, and culture alignment.",
        "min_questions": 2,
        "max_questions": 4,
        "pass_score": 7.5,
    },
}

# --- Domain Round Sequences ---
# Maps: domain → difficulty_level → ordered list of round names
# difficulty_level: 1=Junior, 2=Mid-level, 3=Senior
DOMAIN_ROUND_SEQUENCES = {

    "Engineering & Tech": {
        1: ["Technical", "Behavioral"],
        2: ["Technical", "System Design", "Behavioral"],
        3: ["Technical", "System Design", "Behavioral", "Managerial", "Final"],
    },

    "Finance & Accounting": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Case Study", "Behavioral"],
        3: ["Domain Knowledge", "Case Study", "Behavioral", "Managerial", "Final"],
    },

    "Business & Management": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Case Study", "Behavioral"],
        3: ["Domain Knowledge", "Case Study", "Behavioral", "Managerial", "Final"],
    },

    "Legal": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Case Study", "Behavioral"],
        3: ["Domain Knowledge", "Case Study", "Behavioral", "Managerial", "Final"],
    },

    "Healthcare & Medical": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Situational", "Behavioral"],
        3: ["Domain Knowledge", "Situational", "Behavioral", "Managerial", "Final"],
    },

    "Sales & Marketing": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Role Play", "Behavioral"],
        3: ["Domain Knowledge", "Role Play", "Behavioral", "Managerial", "Final"],
    },

    "Education & Training": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Practical Assessment", "Behavioral"],
        3: ["Domain Knowledge", "Practical Assessment", "Behavioral", "Managerial", "Final"],
    },

    "Creative & Design": {
        1: ["Portfolio Review", "Behavioral"],
        2: ["Portfolio Review", "Practical Assessment", "Behavioral"],
        3: ["Portfolio Review", "Practical Assessment", "Behavioral", "Managerial", "Final"],
    },

    "Science & Research": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Technical Presentation", "Behavioral"],
        3: ["Domain Knowledge", "Technical Presentation", "Behavioral", "Managerial", "Final"],
    },

    "Hospitality & Tourism": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Situational", "Behavioral"],
        3: ["Domain Knowledge", "Situational", "Behavioral", "Managerial", "Final"],
    },

    "Construction & Trades": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Practical Assessment", "Behavioral"],
        3: ["Domain Knowledge", "Practical Assessment", "Behavioral", "Managerial", "Final"],
    },

    "Social Services": {
        1: ["Domain Knowledge", "Behavioral"],
        2: ["Domain Knowledge", "Situational", "Behavioral"],
        3: ["Domain Knowledge", "Situational", "Behavioral", "Managerial", "Final"],
    },

    # Fallback — used if domain is unrecognised
    "default": {
        1: ["Technical", "Behavioral"],
        2: ["Technical", "Behavioral"],
        3: ["Technical", "Behavioral", "Managerial", "Final"],
    },
}


# ============================================================
# Helper Functions
# ============================================================

def get_round_sequence(role_category: str, difficulty_level: int) -> list:
    """
    Returns the ordered list of round NAMES for a given domain and difficulty.
    Falls back to 'default' if domain is not recognised.
    """
    domain_map = DOMAIN_ROUND_SEQUENCES.get(role_category, DOMAIN_ROUND_SEQUENCES["default"])
    # Clamp difficulty to 1-3
    level = max(1, min(3, difficulty_level))
    return domain_map.get(level, domain_map[1])


def get_first_round(role_category: str, difficulty_level: int) -> str:
    """Returns the name of the first round for this domain + difficulty."""
    return get_round_sequence(role_category, difficulty_level)[0]


def get_next_round(current_round_name: str, role_category: str, difficulty_level: int):
    """
    Returns the name of the next round, or None if the interview is complete.
    """
    sequence = get_round_sequence(role_category, difficulty_level)
    if current_round_name in sequence:
        idx = sequence.index(current_round_name)
        if idx + 1 < len(sequence):
            return sequence[idx + 1]
    return None  # No more rounds — interview complete


def get_round_config(round_name: str) -> dict:
    """
    Returns the configuration dict for a given round name.
    Falls back to 'Technical' defaults if round name is unrecognised.
    """
    return ROUND_DEFINITIONS.get(round_name, ROUND_DEFINITIONS["Technical"])


def should_proceed_to_next_round(score: float, current_round_name: str) -> bool:
    """
    Returns True if the candidate's score meets the pass threshold for this round.
    """
    config = get_round_config(current_round_name)
    return score >= config["pass_score"]


def get_applicable_rounds(role_category: str, difficulty_level: int) -> list:
    """
    Returns the full ordered list of round names.
    Kept for backward compatibility and utility.
    """
    return get_round_sequence(role_category, difficulty_level)
