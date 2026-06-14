import hashlib
import time

import streamlit as st

from app_utils import (
    extract_candidate_name,
    format_seconds,
    get_elapsed_time,
    parse_skills
)
from constants import APP_CSS, DEMO_RESUME_TEXT, DEMO_SKILLS_TEXT
from mcq_generator import generate_mcqs
from resume_parser import extract_resume_text
from session_state import clear_interview_state, clear_practice_state
from skill_extractor import extract_skills
from ui_results import render_results


def render_app():
    render_header()
    render_sidebar()
    render_resume_setup()
    render_interview()
    render_results()


def render_header():
    st.set_page_config(
        page_title="AI Interview Coach",
        layout="wide"
    )
    st.title("AI Interview Coach")
    st.write("Upload your resume and take an AI-powered interview.")
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        demo_mode = st.toggle(
            "Demo Mode",
            value=st.session_state.get("demo_mode", False)
        )
        st.session_state.demo_mode = demo_mode

        st.header("Interview Panel")
        st.write(
            st.session_state.get("candidate_name", "Candidate")
            or "Candidate name not entered"
        )

        if "questions" not in st.session_state:
            st.info("Upload a resume or use Demo Mode.")
            return

        total_questions = len(st.session_state.questions)
        attempted = len(st.session_state.get("history", []))

        st.metric("Questions", f"{attempted}/{total_questions}")
        st.metric("Score", st.session_state.get("score", 0))
        st.metric("Timer", format_seconds(get_elapsed_time(st.session_state)))

        if st.session_state.get("skill"):
            st.write("Selected Skill:", st.session_state.skill)


def render_resume_setup():
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if st.session_state.get("demo_mode") and not uploaded_file:
        load_demo_resume()

    if not uploaded_file and not st.session_state.get("demo_mode"):
        return

    if uploaded_file:
        process_uploaded_resume(uploaded_file)

    render_skill_selector()


def load_demo_resume():
    if st.session_state.get("last_file_hash") == "demo":
        return

    st.session_state.last_file_hash = "demo"
    clear_interview_state(st)
    st.session_state.resume_text = DEMO_RESUME_TEXT
    st.session_state.skills_text = DEMO_SKILLS_TEXT
    st.session_state.candidate_name = extract_candidate_name(DEMO_RESUME_TEXT)

    st.info(
        "Demo Mode is running with a sample resume, sample skills, "
        "and offline fallbacks."
    )


def process_uploaded_resume(uploaded_file):
    file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()

    if st.session_state.get("last_file_hash") == file_hash:
        return

    st.session_state.last_file_hash = file_hash
    clear_interview_state(st)
    st.session_state.resume_text = extract_resume_text(uploaded_file)

    if st.session_state.resume_text.startswith("Error"):
        st.error(st.session_state.resume_text)
        st.stop()

    st.session_state.candidate_name = extract_candidate_name(
        st.session_state.resume_text
    )

    with st.spinner("Extracting skills"):
        st.session_state.skills_text = extract_skills(
            st.session_state.resume_text
        )


def render_skill_selector():
    st.text_input(
        "Candidate Name",
        value=st.session_state.get("candidate_name", "Candidate"),
        disabled=True
    )

    skills = parse_skills(st.session_state.get("skills_text", ""))

    if not skills:
        st.warning(
            "No technical skills were found automatically. "
            "Demo skills are being used."
        )
        skills = parse_skills(DEMO_SKILLS_TEXT)
        st.session_state.skills_text = DEMO_SKILLS_TEXT

    if "selected_skill" not in st.session_state:
        st.session_state.selected_skill = skills[0]
    elif st.session_state.selected_skill not in skills:
        st.session_state.selected_skill = skills[0]

    selected_skill = st.selectbox(
        "Select Skill for Interview",
        options=skills,
        key="selected_skill"
    )

    st.write("Selected Skill:", selected_skill)
    st.caption(f"Resume skills detected: {len(skills)}")
    st.info("Get a surprise after getting all right.")

    if st.button("Start Interview"):
        start_interview(selected_skill)


def start_interview(selected_skill):
    with st.spinner("Generating Interview Questions..."):
        questions = generate_mcqs(selected_skill)

    if not questions:
        st.error("Could not generate valid interview questions. Please try again.")
        st.stop()

    st.session_state.skill = selected_skill
    st.session_state.questions = questions
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.pop("report", None)
    clear_practice_state(st)
    st.session_state.interview_started_at = time.time()
    st.session_state.pop("interview_finished_at", None)
    st.rerun()


def render_interview():
    if "questions" not in st.session_state:
        return

    questions = st.session_state.questions
    current = st.session_state.current
    total = len(questions)

    if total == 0:
        st.error("No interview questions are available. Please start a new interview.")

        if st.button("Restart Interview"):
            clear_interview_state(st)
            st.rerun()

        return

    if current >= total:
        return

    question = questions[current]

    st.progress(current / total)
    st.subheader(f"Question {current + 1} / {total}")
    st.write(question["question"])

    answer = st.radio(
        "Choose Your Answer",
        question["options"],
        key=f"q_{current}"
    )

    if st.button("Next Question"):
        save_interview_answer(question, answer)
        st.rerun()


def save_interview_answer(question, answer):
    is_correct = answer == question["answer"]

    if is_correct:
        st.session_state.score += 1

    st.session_state.history.append({
        "question": question["question"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "selected": answer,
        "correct": question["answer"],
        "is_correct": is_correct
    })

    st.session_state.current += 1

    if st.session_state.current >= len(st.session_state.questions):
        st.session_state.interview_finished_at = time.time()
