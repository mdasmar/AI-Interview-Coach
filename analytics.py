def generate_statistics(history):

    total_questions = len(history)

    if total_questions == 0:
        return {
            "total": 0,
            "correct": 0,
            "percentage": 0,
            "easy": (0, 0),
            "medium": (0, 0),
            "hard": (0, 0),
            "topics": {},
            "strong_topics": [],
            "weak_topics": []
        }

    correct_answers = 0

    easy_total = 0
    easy_correct = 0

    medium_total = 0
    medium_correct = 0

    hard_total = 0
    hard_correct = 0

    topics = {}

    for item in history:

        topic = item["topic"]
        difficulty = item["difficulty"]
        is_correct = item["is_correct"]

        if is_correct:
            correct_answers += 1

        if difficulty == "Easy":

            easy_total += 1

            if is_correct:
                easy_correct += 1

        elif difficulty == "Medium":

            medium_total += 1

            if is_correct:
                medium_correct += 1

        elif difficulty == "Hard":

            hard_total += 1

            if is_correct:
                hard_correct += 1

        if topic not in topics:

            topics[topic] = {
                "correct": 0,
                "total": 0,
                "accuracy": 0
            }

        topics[topic]["total"] += 1

        if is_correct:
            topics[topic]["correct"] += 1

    for topic in topics:

        total = topics[topic]["total"]

        correct = topics[topic]["correct"]

        accuracy = round(
            (correct / total) * 100,
            2
        )

        topics[topic]["accuracy"] = accuracy

    strong_topics = []

    weak_topics = []

    for topic, data in topics.items():

        if data["accuracy"] >= 70:

            strong_topics.append(topic)

        else:

            weak_topics.append(topic)

    percentage = round(
        (correct_answers / total_questions) * 100,
        2
    )

    return {

        "total": total_questions,

        "correct": correct_answers,

        "percentage": percentage,

        "easy": (
            easy_correct,
            easy_total
        ),

        "medium": (
            medium_correct,
            medium_total
        ),

        "hard": (
            hard_correct,
            hard_total
        ),

        "topics": topics,

        "strong_topics": strong_topics,

        "weak_topics": weak_topics
    }