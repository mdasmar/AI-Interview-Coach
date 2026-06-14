import streamlit as st

from analytics import generate_statistics
from app_utils import (
    calculate_readiness_score,
    get_elapsed_time,
    get_performance_level,
    parse_skills
)
from report_export import build_downloadable_report
from report_generator import generate_report
from session_state import clear_interview_state
from go_beyond import render_beyond_practice, start_beyond_practice
from weak_practice import (
    render_weak_area_practice,
    start_weak_area_practice
)


def render_results():
    if "questions" not in st.session_state:
        return

    if not st.session_state.questions:
        return

    if st.session_state.current < len(st.session_state.questions):
        return

    score = st.session_state.score
    total = len(st.session_state.questions)
    attempted = len(st.session_state.history)
    stats = generate_statistics(st.session_state.history)
    readiness_score = calculate_readiness_score(
        stats["percentage"],
        attempted,
        total,
        stats["weak_topics"]
    )

    if should_show_perfect_score_popup(score, total):
        render_perfect_score_popup()
        st.stop()

    if st.session_state.get("show_beyond_first"):
        render_beyond_first_view()
        st.stop()

    if st.session_state.get("show_weak_area_first"):
        render_weak_area_first_view(stats)
        st.stop()

    st.success(f"Final Score: {score}/{total}")
    st.info(f"Performance Level: {get_performance_level(stats['percentage'])}")

    render_result_dashboard(score, attempted, stats, readiness_score)
    render_gap_analysis(stats)
    render_report_and_download(score, total, stats, readiness_score)
    render_interview_review()
    render_result_actions(score, total, stats)


def should_show_perfect_score_popup(score, total):
    return (
        total == 10
        and score == total
        and not st.session_state.get("perfect_score_popup_dismissed")
        and not st.session_state.get("show_beyond_practice")
    )


def render_perfect_score_popup():
    if hasattr(st, "dialog"):
        st.dialog("Congratulations!")(render_perfect_score_dialog)()
        return

    st.markdown(
        """
        <div style="max-width: 520px; margin: 48px auto; text-align: center;">
            <h2>Congratulations!</h2>
            <p>You scored 10/10 and unlocked the Go Beyond challenge.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    render_perfect_score_popup_actions()


def render_perfect_score_dialog():
    st.write("You scored 10/10 and unlocked the Go Beyond challenge.")
    render_perfect_score_popup_actions()


def render_perfect_score_popup_actions():
    action_cols = st.columns(2)

    with action_cols[0]:
        if st.button("Go Beyond", key="perfect_score_go_beyond"):
            st.session_state.perfect_score_popup_dismissed = True
            st.session_state.show_beyond_first = True
            start_beyond_practice(st.session_state.skill)
            st.rerun()

    with action_cols[1]:
        if st.button("Go to Analysis Report", key="perfect_score_analysis"):
            st.session_state.perfect_score_popup_dismissed = True
            st.rerun()


def render_beyond_first_view():
    render_beyond_practice(st.session_state.skill)

    if st.button("Go to Analysis Report", key="beyond_first_analysis"):
        st.session_state.show_beyond_first = False
        st.rerun()


def render_weak_area_first_view(stats):
    render_weak_area_practice(
        stats["weak_topics"],
        st.session_state.skill
    )

    if st.button("Go to Analysis Report", key="weak_area_first_analysis"):
        st.session_state.show_weak_area_first = False
        st.rerun()


def render_result_dashboard(score, attempted, stats, readiness_score):
    resume_skills_count = len(parse_skills(st.session_state.get("skills_text", "")))

    st.subheader("Candidate Dashboard")
    dashboard_cols = st.columns(3)

    with dashboard_cols[0]:
        st.metric("Resume Skills", resume_skills_count)
        st.metric("Correct", score)

    with dashboard_cols[1]:
        st.metric("Questions Attempted", attempted)
        st.metric("Accuracy", f"{stats['percentage']}%")

    with dashboard_cols[2]:
        st.metric("Strong Topics", len(stats["strong_topics"]))
        st.metric("Weak Topics", len(stats["weak_topics"]))

    st.subheader("Interview Readiness Score")
    st.metric("Readiness", f"{readiness_score}%")
    st.progress(min(max(readiness_score, 0), 100) / 100)

    render_difficulty_analysis(stats)
    render_topic_performance(stats)


def render_difficulty_analysis(stats):
    st.subheader("Difficulty Analysis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Easy", f"{stats['easy'][0]}/{stats['easy'][1]}")

    with col2:
        st.metric("Medium", f"{stats['medium'][0]}/{stats['medium'][1]}")

    with col3:
        st.metric("Hard", f"{stats['hard'][0]}/{stats['hard'][1]}")


def render_topic_performance(stats):
    st.subheader("Topic Performance")

    for topic, data in stats["topics"].items():
        accuracy = data["accuracy"]
        st.write(f"{topic}: {accuracy}%")
        st.progress(accuracy / 100)


def render_gap_analysis(stats):
    st.subheader("Resume vs Knowledge Gap Analysis")

    resume_skills = parse_skills(st.session_state.get("skills_text", ""))
    practiced_topics = set(stats["topics"].keys())
    untested_skills = [
        skill
        for skill in resume_skills
        if skill != st.session_state.skill and skill not in practiced_topics
    ]

    if stats["weak_topics"]:
        st.write(
            "Your resume shows relevant skills, but your answers need more practice in:"
        )

        for topic in stats["weak_topics"]:
            st.write(f"- {topic}")
    else:
        st.write(
            "Your interview answers are aligned well with the selected resume skill."
        )

    if untested_skills:
        st.write("Additional resume skills to validate next:")
        st.write(", ".join(untested_skills[:6]))


def render_report_and_download(score, total, stats, readiness_score):
    if "report" not in st.session_state:
        with st.spinner("Generating AI Analysis..."):
            st.session_state.report = generate_report(
                st.session_state.skill,
                score,
                total,
                st.session_state.history,
                stats
            )

    with st.expander("Show Full AI Career Analysis Report"):
        st.markdown(st.session_state.report)

    downloadable_report = build_downloadable_report(
        st.session_state,
        st.session_state.get("candidate_name", "Candidate"),
        st.session_state.skill,
        score,
        total,
        stats,
        readiness_score,
        get_elapsed_time(st.session_state),
        st.session_state.report
    )

    st.download_button(
        "Download Report",
        data=downloadable_report,
        file_name="ai_interview_report.md",
        mime="text/markdown"
    )


def render_interview_review():
    with st.expander("Interview Review"):
        for index, item in enumerate(st.session_state.history, start=1):
            st.write(f"Question {index}")
            st.write(item["question"])
            st.write(f"Your Answer: {item['selected']}")
            st.write(f"Correct Answer: {item['correct']}")

            if item["is_correct"]:
                st.success("Correct")
            else:
                st.error("Incorrect")

            st.divider()


def render_result_actions(score, total, stats):
    action_cols = st.columns(2)

    with action_cols[0]:
        if score == total:
            if st.button("Go Beyond"):
                st.session_state.show_beyond_first = True
                start_beyond_practice(st.session_state.skill)
                st.rerun()
        else:
            if st.button("Practice Weak Areas"):
                st.session_state.show_weak_area_first = True
                start_weak_area_practice(
                    stats["weak_topics"],
                    st.session_state.skill
                )
                st.rerun()

    with action_cols[1]:
        if st.button("Restart Interview"):
            clear_interview_state(st)
            st.rerun()

    render_weak_area_practice(
        stats["weak_topics"],
        st.session_state.skill
    )
    render_beyond_practice(st.session_state.skill)
