from azure_client import (
    client,
    DEPLOYMENT
)

import json


REQUIRED_FIELDS = {
    "question",
    "options",
    "answer",
    "difficulty",
    "topic"
}

VALID_DIFFICULTIES = {
    "Easy",
    "Medium",
    "Hard"
}


def validate_questions(questions):
    if not isinstance(questions, list):
        return []

    valid_questions = []

    for question in questions:
        if not isinstance(question, dict):
            continue

        if not REQUIRED_FIELDS.issubset(question):
            continue

        options = question["options"]

        if not isinstance(options, list) or len(options) != 4:
            continue

        question_text = str(question["question"]).strip()
        answer = str(question["answer"]).strip()
        difficulty = str(question["difficulty"]).strip().capitalize()
        topic = str(question["topic"]).strip()
        options = [
            str(option).strip()
            for option in options
        ]

        if answer not in options:
            continue

        if difficulty not in VALID_DIFFICULTIES:
            continue

        if not question_text or not topic:
            continue

        valid_questions.append({
            "question": question_text,
            "options": options,
            "answer": answer,
            "difficulty": difficulty,
            "topic": topic
        })

    return valid_questions


def fallback_questions(skill):
    skill_name = skill.strip() or "the selected skill"

    return [
        {
            "question":
                f"What is a core purpose of {skill_name} in technical work?",

            "options": [
                "Solving relevant technical problems",
                "Replacing all documentation",
                "Avoiding testing",
                "Removing the need for debugging"
            ],

            "answer":
                "Solving relevant technical problems",

            "difficulty":
                "Easy",

            "topic":
                "Core Concepts"
        },
        {
            "question":
                f"Why is practical experience important when learning {skill_name}?",

            "options": [
                "It helps apply concepts to real problems",
                "It removes the need to understand basics",
                "It guarantees perfect answers",
                "It avoids all errors"
            ],

            "answer":
                "It helps apply concepts to real problems",

            "difficulty":
                "Easy",

            "topic":
                "Practice"
        },
        {
            "question":
                f"What should you do first when debugging a {skill_name} issue?",

            "options": [
                "Identify and reproduce the problem",
                "Delete the project",
                "Ignore logs",
                "Change random settings"
            ],

            "answer":
                "Identify and reproduce the problem",

            "difficulty":
                "Easy",

            "topic":
                "Debugging"
        },
        {
            "question":
                f"What makes an answer about {skill_name} stronger in an interview?",

            "options": [
                "Explaining tradeoffs with examples",
                "Using only buzzwords",
                "Avoiding details",
                "Changing the topic"
            ],

            "answer":
                "Explaining tradeoffs with examples",

            "difficulty":
                "Medium",

            "topic":
                "Interview Communication"
        },
        {
            "question":
                f"When designing with {skill_name}, what should guide your choice of approach?",

            "options": [
                "Requirements, constraints, and maintainability",
                "Only personal preference",
                "The longest possible solution",
                "Avoiding documentation"
            ],

            "answer":
                "Requirements, constraints, and maintainability",

            "difficulty":
                "Medium",

            "topic":
                "Design Decisions"
        },
        {
            "question":
                f"What is a good way to show proficiency in {skill_name}?",

            "options": [
                "Discuss a project and the decisions you made",
                "Say you know everything",
                "Avoid examples",
                "Only list definitions"
            ],

            "answer":
                "Discuss a project and the decisions you made",

            "difficulty":
                "Medium",

            "topic":
                "Experience"
        },
        {
            "question":
                f"What should be considered before optimizing a {skill_name} solution?",

            "options": [
                "Measure the current behavior first",
                "Optimize without evidence",
                "Remove tests",
                "Ignore user impact"
            ],

            "answer":
                "Measure the current behavior first",

            "difficulty":
                "Medium",

            "topic":
                "Optimization"
        },
        {
            "question":
                f"What is a common risk in advanced {skill_name} work?",

            "options": [
                "Making the solution too complex to maintain",
                "Writing clear tests",
                "Documenting decisions",
                "Reviewing requirements"
            ],

            "answer":
                "Making the solution too complex to maintain",

            "difficulty":
                "Hard",

            "topic":
                "Architecture"
        },
        {
            "question":
                f"How should you handle uncertainty in a difficult {skill_name} interview question?",

            "options": [
                "State assumptions and reason step by step",
                "Pretend to know everything",
                "Give no answer",
                "Memorize unrelated facts"
            ],

            "answer":
                "State assumptions and reason step by step",

            "difficulty":
                "Hard",

            "topic":
                "Problem Solving"
        },
        {
            "question":
                f"What separates senior-level {skill_name} usage from basic usage?",

            "options": [
                "Balancing correctness, maintainability, and tradeoffs",
                "Using the newest tool without reason",
                "Avoiding collaboration",
                "Skipping validation"
            ],

            "answer":
                "Balancing correctness, maintainability, and tradeoffs",

            "difficulty":
                "Hard",

            "topic":
                "Senior Judgment"
        }
    ]


def fallback_hard_questions(skill):
    hard_questions = [
        question
        for question in fallback_questions(skill)
        if question["difficulty"] == "Hard"
    ]

    skill_name = skill.strip() or "the selected skill"

    hard_questions.extend([
        {
            "question":
                f"In a high-impact {skill_name} system, how should you choose between a quick fix and a deeper redesign?",
            "options": [
                "Compare risk, deadline, root cause, and long-term maintenance cost",
                "Always choose the fastest change",
                "Always rewrite the full system",
                "Ignore production impact"
            ],
            "answer":
                "Compare risk, deadline, root cause, and long-term maintenance cost",
            "difficulty":
                "Hard",
            "topic":
                "Engineering Tradeoffs"
        },
        {
            "question":
                f"What is the strongest way to validate an advanced {skill_name} solution before release?",
            "options": [
                "Test critical paths, edge cases, performance, and rollback behavior",
                "Only check that the happy path works once",
                "Skip validation if the code looks clean",
                "Ask users to find issues after release"
            ],
            "answer":
                "Test critical paths, edge cases, performance, and rollback behavior",
            "difficulty":
                "Hard",
            "topic":
                "Production Readiness"
        }
    ])

    return hard_questions[:5]


def parse_model_questions(response_text):
    text = response_text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return validate_questions(json.loads(text))


def generate_mcqs(skill):
    """
    Generate 10 interview MCQs for a selected skill.
    """

    prompt = f"""
    Generate exactly 10 interview MCQs for {skill}.

    Requirements:

    - 3 Easy questions
    - 4 Medium questions
    - 3 Hard questions

    Cover different topics.

    Return ONLY valid JSON.

    Format:

    [
      {{
        "question":"What is JVM?",
        "options":[
          "Java Virtual Machine",
          "Java Vendor Machine",
          "Joint Virtual Memory",
          "None of the above"
        ],
        "answer":"Java Virtual Machine",
        "difficulty":"Easy",
        "topic":"JVM"
      }}
    ]

    Rules:

    - Exactly 4 options
    - One correct answer
    - No explanations
    - No markdown
    - No extra text
    """

    try:

        response = client.responses.create(
            model=DEPLOYMENT,
            input=prompt
        )

        valid_questions = parse_model_questions(response.output_text)

        if not valid_questions:
            raise ValueError("Model returned no valid MCQs")

        return valid_questions

    except Exception as e:

        print(
            f"MCQ Generation Error: {e}"
        )

        return fallback_questions(skill)


def generate_hard_mcqs(skill):
    """
    Generate 5 hard interview MCQs for the Go Beyond challenge.
    """

    prompt = f"""
    Generate exactly 5 hard interview MCQs for {skill}.

    Requirements:

    - All questions must be Hard difficulty
    - Cover advanced scenarios, tradeoffs, debugging, design, and edge cases
    - Return ONLY valid JSON

    Format:

    [
      {{
        "question":"What is the best way to diagnose a complex issue?",
        "options":[
          "Reproduce it and isolate the root cause",
          "Change random settings",
          "Ignore logs",
          "Skip tests"
        ],
        "answer":"Reproduce it and isolate the root cause",
        "difficulty":"Hard",
        "topic":"Debugging"
      }}
    ]

    Rules:

    - Exactly 4 options
    - One correct answer
    - No explanations
    - No markdown
    - No extra text
    """

    try:

        response = client.responses.create(
            model=DEPLOYMENT,
            input=prompt
        )

        valid_questions = parse_model_questions(response.output_text)
        hard_questions = [
            question
            for question in valid_questions
            if question["difficulty"] == "Hard"
        ]

        if len(hard_questions) < 5:
            raise ValueError("Model returned fewer than 5 hard MCQs")

        return hard_questions[:5]

    except Exception as e:

        print(
            f"Hard MCQ Generation Error: {e}"
        )

        return fallback_hard_questions(skill)
