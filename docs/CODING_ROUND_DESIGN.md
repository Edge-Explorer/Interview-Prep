# 🧠 Coding Round Intelligence — Feature Design Document

**Authored by: Karan Shelar**
**Status: Planning Phase (v3.0 Roadmap)**
**Date: February 2026**

---

## 📖 Overview

This document outlines the complete design for the **Coding Round Intelligence System** — a new module that transforms the platform from a "question-answer chat" into a **real-world coding interview simulation**. 

The core philosophy is **simplicity with depth**: No complex execution engines. Just you, your code, your explanation, and an AI that "thinks" alongside you like a Senior Engineer would.

---

## 🎯 The Core Vision: "Whiteboard Mode"

> *"In a real interview, you don't have a compiler. You have a whiteboard, a marker, and a pair of eyes watching your every move."*

Instead of building a LeetCode-style compiler (which is expensive, complex, and teaches users to "guess and check"), we implement a **Whiteboard-First Philosophy**:

1. **The AI asks** a targeted coding problem.
2. **The user writes** their solution in a code editor (no run button).
3. **The user explains** their logic to the AI in plain text.
4. **The AI "Dry Runs"** the code manually in its reasoning and critiques it.

This is the **exact process used in top-tier companies** like Google and Stripe. It tests understanding of code, not just the ability to run it.

---

## 🏗️ System Architecture: How It All Fits Together

```
[AI Generates a Problem Spec]
          |
          ▼
[User Sees: Problem + Constraints + Sample Test Cases (Visible)]
          |
          ▼
[User writes code in the editor and types out their explanation]
          |
          ▼
[User hits "Submit for Review" (NOT "Run")]
          |
          ▼
[AI Dry-Runs the submission → Evaluates Logic, Style, Efficiency]
          |
     ┌────┴────┐
     ▼         ▼
[PASS]      [FAIL → Tiered Hint System]
     |              |
     ▼              ▼
[Score + Review] [Retry with Nudge]
     |
     ▼
[Interaction logged to JSON Learning Ledger]
```

---

## 🔢 Section 1: The Problem Specification Format

When the AI generates a coding problem, it will produce a **Structured Problem Spec** — not just a plain paragraph. This allows the frontend to render a clean, professional coding panel.

### Example Problem Spec (AI-Generated JSON):
```json
{
  "problem_id": "cp_204",
  "title": "Two Sum (Company Variant)",
  "difficulty": "Medium",
  "company_context": "Commonly asked in Shastra Solutions Round 1 (Technical Screening)",
  "problem_statement": "Given an array of integers 'nums' and a target 'target', return the indices of two numbers that add up to the target. Each input has exactly one solution. You may not use the same element twice.",
  "constraints": [
    "2 ≤ nums.length ≤ 10^4",
    "−10^9 ≤ nums[i] ≤ 10^9",
    "Only one valid answer exists"
  ],
  "sample_test_cases": [
    { "input": "nums = [2, 7, 11, 15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9" },
    { "input": "nums = [3, 2, 4], target = 6", "output": "[1, 2]", "explanation": "nums[1] + nums[2] = 2 + 4 = 6" }
  ],
  "hidden_test_cases_count": 5,
  "hint_topics": ["Hash Map", "Time Complexity", "Edge Cases: Empty Array"]
}
```

### Key Design Choices:
- **Sample test cases are VISIBLE** so the user can mentally trace through them.
- **Hidden test cases exist** (count is shown, not the data) to keep the challenge authentic.
- **`hint_topics`** is stored internally and used to generate *targeted* nudges—never shown to the user directly.

---

## 🗣️ Section 2: The "Explanation Gate"

After the user writes their code, they **must** provide a written explanation before submitting. This is non-negotiable and is the heart of the Whiteboard Mode.

### The Explanation Gate interface:
```
┌──────────────────────────────────────────────────┐
│  Your Code           │  Your Explanation          │
│                      │                            │
│  def twoSum(nums,    │  "I'm using a hash map     │
│    target):          │  to store seen values.     │
│    seen = {}         │  On each iteration, I      │
│    for i, n in       │  check if the complement   │
│      enumerate(nums):│  (target - n) already      │
│      comp = target-n │  exists. This gives me     │
│      if comp in seen:│  O(n) time and O(n) space  │
│        return [...]  │  complexity."              │
│      seen[n] = i     │                            │
└──────────────────────────────────────────────────┘
          [  Submit for Review  ]
```

**Why force an explanation?**
- A user can copy code from memory. They **cannot** fake an explanation.
- The AI uses the explanation to detect if the user truly understands or is pattern-matching from memory.
- If the explanation contradicts the code, the AI flags it as a "Logic Misalignment."

---

## 💡 Section 3: The Tiered Hint System

When the AI Dry-Run detects a failure, it enters **Progressive Nudge Mode**. Each unsuccessful attempt unlocks the next tier of nudge.

| Tier | Name | What the AI says | What it reveals |
| :--- | :--- | :--- | :--- |
| **0** | No Hint | The user gets it right first try | — |
| **1** | Conceptual Nudge | *"Have you considered the time complexity of your current approach?"* | Nothing. Just a question. |
| **2** | Structural Hint | *"Think about a data structure that provides O(1) lookups."* | Points to Hash Map (without naming it). |
| **3** | Edge Case Warning | *"Your current solution works for positive numbers. What happens if the target is `0` or `nums` contains `-1`?"* | Reveals the edge case category. |
| **4** | Partial Reveal | *"Try storing the index alongside the value as you iterate."* | A direct implementation clue. |

**CRITICAL RULE**: The AI **never gives the full solution**. Even at Tier 4, the user still has to connect the dots themselves. The full solution only appears in the **Post-Round Review**.

### Hint Scoring Impact:
```
Solved with 0 Hints → Score: 10.0 (Elite)
Solved with 1 Hint  → Score: 8.5  (Strong)
Solved with 2 Hints → Score: 7.0  (Competent)
Solved with 3 Hints → Score: 5.5  (Developing)
Solved with 4 Hints → Score: 4.0  (Needs Work)
Not Solved          → Score: 0.0  (Fail)
```

---

## 🤖 Section 4: The AI "Dry Run" — How It Works

When the user submits their code + explanation, the AI performs a **Mental Code Execution** step-by-step.

### What the AI checks:
1. **Logic Correctness**: Does the code produce the right output for the visible test cases?
2. **Hidden Edge Cases**: Does the code handle `null`, empty arrays, single elements, negatives, and large inputs?
3. **Time Complexity**: Is an O(n²) loop being used where O(n) is possible?
4. **Space Complexity**: Is memory being wasted unnecessarily?
5. **Explanation vs. Code Alignment**: Does what the user *said* match what the code *actually does*?
6. **Code Quality**: Are variable names meaningful? Is the logic readable?

### Example Dry-Run Output (stored in the JSON Ledger, never shown raw):
```json
{
  "dry_run_result": "PARTIAL_PASS",
  "passed_visible_cases": 2,
  "failed_hidden_cases": ["input: [], target: 0 → IndexError"],
  "logic_correctness": true,
  "explanation_alignment": true,
  "time_complexity_detected": "O(n)",
  "space_complexity_detected": "O(n)",
  "critical_flaw": "Missing guard for empty array input",
  "code_quality_notes": "Clean and readable. Variable naming is excellent.",
  "recommended_hint_tier": 3
}
```

---

## 📂 Section 5: The JSON Learning Ledger

Every single coding interaction is stored as a **Structured Interaction Record**. This is the engine that enables two major features:
1. **User Progress Tracking**: See how you've improved over time.
2. **AI-Driven Personalization**: The AI looks at past sessions to avoid repeating topics you've mastered and targets your known weak spots.

### The Ledger Entry Format:
```json
{
  "session_id": "sess_20260221_001",
  "user_id": "karan_shelar",
  "company_context": "Shastra Solutions",
  "round": "Technical",
  "problem": {
    "id": "cp_204",
    "title": "Two Sum (Company Variant)",
    "difficulty": "Medium",
    "topic_tags": ["Hash Map", "Arrays", "Two Pointers"]
  },
  "attempts": [
    {
      "attempt_number": 1,
      "timestamp": "2026-02-21T11:32:00",
      "code_snapshot": "def twoSum(nums, target):\n  for i in range(len(nums)):\n    for j ...",
      "explanation_given": "I'm iterating through all pairs...",
      "dry_run_result": "FAIL",
      "flaw_detected": "O(n^2) time complexity",
      "hint_given": "Tier 1: Conceptual Nudge — Time Complexity",
      "hint_text": "Have you considered the time complexity of your current approach?"
    },
    {
      "attempt_number": 2,
      "timestamp": "2026-02-21T11:35:00",
      "code_snapshot": "def twoSum(nums, target):\n  seen = {}\n  for i, n in enumerate(nums)...",
      "explanation_given": "I'm using a hash map to store seen values...",
      "dry_run_result": "PARTIAL_PASS",
      "flaw_detected": "Missing empty array guard",
      "hint_given": "Tier 3: Edge Case Warning",
      "hint_text": "What happens if the input array is empty?"
    },
    {
      "attempt_number": 3,
      "timestamp": "2026-02-21T11:37:00",
      "code_snapshot": "def twoSum(nums, target):\n  if not nums: return []\n  seen = {} ...",
      "explanation_given": "Added a guard for empty array first, then hash map...",
      "dry_run_result": "FULL_PASS",
      "flaw_detected": null,
      "hint_given": null
    }
  ],
  "final_score": 7.0,
  "hints_used": 2,
  "total_time_minutes": 5,
  "ai_final_review": "Strong understanding of Hash Maps. Weakness is anticipating edge cases without prompting. Recommend practicing boundary-condition exercises.",
  "topic_mastery_update": {
    "Hash Map": "IMPROVED",
    "Edge Cases": "NEEDS_WORK"
  }
}
```

---

## 🔀 Section 6: Simulation vs. Mentorship Mode

Following the agreed design philosophy, the platform has two distinct modes:

| Feature | 🔴 Simulation Mode (Adinath) | 🟢 Mentorship Mode (Veda) |
| :--- | :--- | :--- |
| **Hints** | ❌ None. Total silence. | ✅ Full Tiered Nudge System. |
| **Explanation Gate** | ✅ Mandatory | ✅ Mandatory |
| **AI Dry Run** | ✅ (Results shown post-round) | ✅ (Results shown live) |
| **Pressure Mode** | ✅ Active (questioning your approach) | ❌ Off |
| **Learning Ledger** | ✅ Logged | ✅ Logged |
| **Use Case** | Final Mock, Hard Mode | Daily Practice, Weak Topic Drilling |

---

## 🔮 Section 7: The Personalization Loop (Long-Term AI Learning)

After every session, the AI reads the **Learning Ledger** and updates your **Topic Mastery Profile**:

```
Past Weakness (stored in Ledger): "Edge Cases in Array Problems"
           |
           ▼
Next Session (AI picks problem): "Rotated Sorted Array Search"
(A problem specifically chosen because it has a famous edge case:
 the pivot could be at any point, including index 0)
           |
           ▼
If you pass → Mastery Level: IMPROVED → AI moves to next weak area.
If you fail → AI gives Tier 1 Hint → Stores result → Tries again next session.
```

This creates an **"Infinite Practice Loop"** that adapts to exactly where you are, not a generic curriculum.

---

## 📋 Summary: What We Are Building (Priority Order)

| Priority | Feature | Description |
| :---: | :--- | :--- |
| **1** | Whiteboard Code Editor UI | A split-pane: Code editor (left) + Explanation text area (right). |
| **2** | Problem Spec Generator | AI generates structured JSON problem specs per company context. |
| **3** | AI Dry Run Engine | The core Gemini prompt that "mentally executes" and critiques code + explanation. |
| **4** | Tiered Hint System | Progressive, non-revealing nudges based on dry-run failure type. |
| **5** | JSON Learning Ledger | Backend endpoint to save every interaction snapshot per user. |
| **6** | Personalization Engine | AI reads the ledger to select the next problem based on weak topics. |
| **7** | Simulation vs. Mentorship Toggle | UI toggle to switch modes (Adinath cold mode vs. Veda guided mode). |

---

## 🎭 Section 8: The Persona Architecture — "The Secret Sauce"

> *"We don't just ask questions. We simulate Human Personalities that test different parts of your brain."*

The Coding Round is not delivered by a generic AI bot. It is delivered by one of two **distinct, deeply-characterized personas**, each designed to pressure-test a completely different dimension of your ability.

---

### 🔴 Adinath — "The Primal Sage"

**Core Drive**: Find the exact boundary of your knowledge and push past it.

**Personality Profile**:
- Cold and direct. Zero emotional feedback.
- Minimal acknowledgment of correct answers. He simply moves deeper.
- Asks **"Why?"** after every answer, regardless of whether it's right or wrong.
- Never compliments. Never encourages. Every silence is intentional pressure.

**In the Coding Round, Adinath will:**
- Read your Resume before the session and identify **"hooks"** — technologies or projects you've claimed expertise in.
- Target those hooks first. If you wrote "Built a scalable API," he will ask you to code a Rate Limiter from scratch.
- After you submit your code and explanation, he will **not just run the dry pass.** He will ask follow-up interrogation questions:
  *"You said your solution is O(n). Walk me through the exact memory allocation when the input is 10,000 items."*
- At Turn 6+, he enters **Pressure Mode**: He will challenge your own explanation against your own code. *"Line 4 of your code contradicts what you said in your explanation. Which one is correct?"*

**Hint Policy**: ❌ **ZERO HINTS.** Total silence. You find out where you went wrong in the Post-Round Review.

**Use Case**: Final Mock Interviews, Hard Difficulty, Pre-Placement Rehearsals.

---

### 🟢 Veda — "The Eternal Wisdom"

**Core Drive**: Guide you to the solution through strategic questions that build your thinking from the ground up.

**Personality Profile**:
- Warm but precise. She acknowledges effort but never accepts mediocrity.
- Focuses on the **"Big Picture" first** — she wants to see your architectural instinct before your code.
- Does not ask "Why?" She asks **"What if?"** — pushing you to explore edge cases and alternate paths.
- Mentors actively. She is interested in your growth, not your failure.

**In the Coding Round, Veda will:**
- Before you write a single line of code, ask you to **verbally explain your approach** in plain English. This forces you to think before you type.
- If your approach is flawed, she gives a **Tier 1 Conceptual Nudge** immediately — she won't let you waste 10 minutes coding a broken solution.
- After your explanation, she asks **"What's the bottleneck?"** before you ever submit. This develops the habit of complexity analysis.
- If your Dry Run fails, she walks through the failure **collaboratively**: *"Let's trace this together — what is the value of `seen` after the third iteration?"*

**Hint Policy**: ✅ **Full Tiered Hint System** (See Section 3). Progressive, specific, and never gives the answer directly.

**Use Case**: Daily Practice, Weak Topic Drilling, Concept Building, Freshman Mode.

---

### ⚡ The Persona Decision Matrix

| Scenario | Who takes over? | Why? |
| :--- | :--- | :--- |
| User selects "Hard" difficulty | **Adinath** | Maximum pressure. No safety net. |
| User selects "Practice" mode | **Veda** | Guided, iterative learning. |
| User fails Round 1 with Adinath | **Veda** (for retry) | Failure diagnosed by Adinath, healed by Veda. |
| User's Learning Ledger shows "Edge Cases: Weak" | **Veda** | She targets the weak area with precision nudges. |
| User has 7+ sessions with strong scores | **Adinath** (auto-upgraded) | The system escalates pressure as mastery grows. |

---

### 🧲 The "Resume Hooks" Mechanism (Planned)

Both personas will, at the start of the session, make a **silent pass over the user's resume** and JD. They extract "hooks" — claimed skills or projects — and build their question strategy around them.

**Example:**
> Resume claims: *"Implemented a Redis caching layer that reduced API response time by 40%."*

- **Adinath's Hook**: *"Write me a simple LRU Cache from scratch. No library calls."*
- **Veda's Hook**: *"Before we code anything — what's the difference between an LRU and LFU Cache? Which one did you use and why?"*

The hooks ensure **no two sessions are identical** and no user can "rehearse" their way through a fixed question bank.

---

## 🗓️ Section 9: Implementation Timeline (Next 2–3 Days)

This is the planned execution order for shipping the Coding Round Intelligence feature.

### **Day 1 — The Backend Brain**
- [ ] Build the **Problem Spec Generator** prompt in `gemini_service.py`. The AI takes a company name + round context and outputs a structured JSON problem.
- [ ] Build the **AI Dry Run prompt** — the core Gemini call that reads `(code + explanation)` and outputs a `dry_run_result` JSON.
- [ ] Create a new FastAPI endpoint: `POST /interview/coding-submit` that accepts code + explanation and returns the Dry Run result.
- [ ] Create the **Learning Ledger** endpoint: `POST /interview/coding-log` that saves the full interaction record to the user's session in the database.

### **Day 2 — The Hint Engine + Personas**
- [ ] Build the **Tiered Hint Generator** — a function that takes the `dry_run_result.critical_flaw` and generates the appropriate tier-level nudge (not a generic hint, but a targeted one based on the flaw type).
- [ ] Wire **Adinath's Pressure Mode** into the prompt: If `chat_history > 6` turns, inject the "contradict your own explanation" challenge.
- [ ] Wire **Veda's Verbalization Gate**: Before the Coding editor opens, Veda requires the user to type out their plain-English approach.
- [ ] Build the **"Resume Hook" extractor**: A pre-session step that parses the user's resume and identifies 2-3 "targets" for interrogation.

### **Day 3 — The Frontend & Wiring**
- [ ] Build the **Whiteboard UI**: A clean split-pane component (Code Editor left, Explanation textarea right).
- [ ] Add the **"Submit for Review"** button that calls `/interview/coding-submit`.
- [ ] Build the **Persona Selector toggle**: "Simulation Mode (Adinath)" vs. "Mentorship Mode (Veda)."
- [ ] Render the **Dry Run feedback panel**: Shows Pass/Fail, Complexity detected, and the next hint (if in Veda mode).
- [ ] Render the **Post-Round Code Review Report**: Full breakdown of all attempts, hints used, final score, and AI notes.

---

## ✍️ Author Notes

> This design avoids sandbox code execution entirely, which eliminates infrastructure costs and security risks of running user-submitted code on a server. The AI's ability to reason about code logic is more than sufficient for interview preparation — and arguably *better* at catching conceptual flaws than a compiler ever could.

> The Persona Architecture is what separates this platform from every other interview prep tool. LeetCode gives you problems. We give you a **Personality** that thinks, challenges, and adapts to exactly who you are.

**Karan Shelar** — Architect of the Intelligent Interview System.
