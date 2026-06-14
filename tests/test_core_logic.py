import unittest

from analytics import generate_statistics
from mcq_generator import validate_questions


class AnalyticsTests(unittest.TestCase):
    def test_empty_history_returns_zeroed_stats(self):
        stats = generate_statistics([])

        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["correct"], 0)
        self.assertEqual(stats["percentage"], 0)
        self.assertEqual(stats["weak_topics"], [])

    def test_history_generates_topic_and_difficulty_stats(self):
        history = [
            {
                "topic": "Python",
                "difficulty": "Easy",
                "is_correct": True
            },
            {
                "topic": "Python",
                "difficulty": "Medium",
                "is_correct": False
            },
            {
                "topic": "SQL",
                "difficulty": "Hard",
                "is_correct": True
            }
        ]

        stats = generate_statistics(history)

        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["correct"], 2)
        self.assertEqual(stats["percentage"], 66.67)
        self.assertEqual(stats["easy"], (1, 1))
        self.assertEqual(stats["medium"], (0, 1))
        self.assertEqual(stats["hard"], (1, 1))
        self.assertEqual(stats["topics"]["Python"]["accuracy"], 50.0)
        self.assertIn("Python", stats["weak_topics"])
        self.assertIn("SQL", stats["strong_topics"])


class MCQValidationTests(unittest.TestCase):
    def test_validate_questions_accepts_valid_question(self):
        questions = validate_questions([
            {
                "question": "What is Python?",
                "options": [
                    "A programming language",
                    "A database",
                    "A cloud service",
                    "A markup language"
                ],
                "answer": "A programming language",
                "difficulty": "easy",
                "topic": "Python"
            }
        ])

        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]["difficulty"], "Easy")

    def test_validate_questions_rejects_invalid_answer(self):
        questions = validate_questions([
            {
                "question": "What is Python?",
                "options": ["A", "B", "C", "D"],
                "answer": "E",
                "difficulty": "Easy",
                "topic": "Python"
            }
        ])

        self.assertEqual(questions, [])


if __name__ == "__main__":
    unittest.main()
