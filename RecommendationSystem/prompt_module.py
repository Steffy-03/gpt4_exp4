def construct_prompt(profile, analysis):

    prompt = f"""
You are a personalized recommendation assistant.

User Profile:
Name: {profile['name']}
Background: {profile['background']}
Interests: {profile['interests']}
Skill Level: {profile['skill_level']}
Preferred Category: {profile['preference']}
Goal: {profile['goal']}

Preference Analysis:
Primary Interest: {analysis['primary_interest']}
Secondary Interest: {analysis['secondary_interest']}
Skill Level: {analysis['skill_level']}
Goal: {analysis['goal']}
Preference: {analysis['preference']}

Generate exactly {profile['num_recommendations']} personalized learning recommendations.

IMPORTANT:
Use EXACTLY this format for every recommendation:

1. NAME: Python for Data Analysis
SCORE: 95
REASON: Suitable for the user's interests and learning goal.

2. NAME: Java Programming
SCORE: 90
REASON: Matches the user's programming background.

Rules:
- SCORE must be a whole number from 0 to 100.
- Give a different suitable score for each recommendation.
- Do not use percentages.
- Keep each reason under 25 words.
- Return only the recommendations.
"""

    return prompt


def display_prompt(prompt):

    print("\nGPT/Ollama PROMPT")
    print("-" * 65)
    print(prompt)