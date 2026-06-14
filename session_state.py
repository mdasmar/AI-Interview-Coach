INTERVIEW_STATE_KEYS = [
    "skill",
    "questions",
    "current",
    "score",
    "history",
    "report",
    "weak_area_mcqs",
    "weak_area_mcq_key",
    "show_weak_area_practice",
    "weak_area_current",
    "weak_area_score",
    "weak_area_history",
    "weak_area_answer_submitted",
    "beyond_mcqs",
    "beyond_mcq_key",
    "show_beyond_practice",
    "beyond_current",
    "beyond_score",
    "beyond_history",
    "beyond_answer_submitted",
    "show_beyond_first",
    "show_weak_area_first",
    "perfect_score_popup_dismissed",
    "interview_started_at",
    "interview_finished_at"
]

PRACTICE_STATE_KEYS = [
    "weak_area_mcqs",
    "weak_area_mcq_key",
    "show_weak_area_practice",
    "weak_area_current",
    "weak_area_score",
    "weak_area_history",
    "weak_area_answer_submitted",
    "beyond_mcqs",
    "beyond_mcq_key",
    "show_beyond_practice",
    "beyond_current",
    "beyond_score",
    "beyond_history",
    "beyond_answer_submitted",
    "show_beyond_first",
    "show_weak_area_first",
    "perfect_score_popup_dismissed"
]


def ensure_defaults(st):
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = "Candidate"


def clear_interview_state(st):
    for key in INTERVIEW_STATE_KEYS:
        st.session_state.pop(key, None)


def clear_practice_state(st):
    for key in PRACTICE_STATE_KEYS:
        st.session_state.pop(key, None)
