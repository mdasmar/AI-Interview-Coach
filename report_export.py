from app_utils import format_seconds, parse_skills


def build_downloadable_report(
        session_state,
        candidate_name,
        skill,
        score,
        total,
        stats,
        readiness_score,
        elapsed_time,
        report):

    return f"""
# AI Interview Coach Report

Candidate: {candidate_name}
Interview Skill: {skill}
Interview Time: {format_seconds(elapsed_time)}

## Dashboard

- Resume Skills: {len(parse_skills(session_state.get("skills_text", "")))}
- Questions Attempted: {len(session_state.get("history", []))}
- Correct: {score}
- Accuracy: {stats["percentage"]}%
- Strong Topics: {len(stats["strong_topics"])}
- Weak Topics: {len(stats["weak_topics"])}
- Interview Readiness Score: {readiness_score}%

## AI Career Analysis

{report}
"""
