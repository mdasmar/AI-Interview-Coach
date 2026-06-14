import re
import time


def parse_skills(skills_text):
    if not skills_text or skills_text.startswith("Error"):
        return []

    separator = "," if "," in skills_text else "\n"

    return [
        skill.strip()
        for skill in skills_text.split(separator)
        if skill.strip()
    ]


def extract_candidate_name(resume_text):
    section_headings = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "summary",
        "objective",
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "contact"
    }

    for raw_line in resume_text.splitlines()[:15]:
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"^(name|candidate)\s*[:\-]\s*", "", line, flags=re.I)
        normalized = line.lower().strip()

        if normalized in section_headings:
            continue

        if "@" in line or "http" in normalized or "linkedin" in normalized:
            continue

        if re.search(r"\d{5,}", line):
            continue

        if len(line.split()) > 5:
            continue

        if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,60}", line):
            return " ".join(line.split())

    return "Candidate"


def format_seconds(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"


def get_elapsed_time(session_state):
    started_at = session_state.get("interview_started_at")

    if not started_at:
        return 0

    finished_at = session_state.get("interview_finished_at")
    end_time = finished_at or time.time()

    return max(0, end_time - started_at)


def calculate_readiness_score(accuracy, attempted, total_questions, weak_topics):
    completion_score = (
        attempted / total_questions * 100
        if total_questions
        else 0
    )
    weak_topic_penalty = min(len(weak_topics) * 5, 20)

    return round(
        (accuracy * 0.7) + (completion_score * 0.3) - weak_topic_penalty,
        2
    )


def get_performance_level(percentage):
    if percentage >= 90:
        return "Excellent"

    if percentage >= 75:
        return "Strong"

    if percentage >= 60:
        return "Average"

    return "Needs Improvement"
