import streamlit as st

from mcq_generator import generate_mcqs


def get_weak_area_mcqs(weak_topics, skill):
    topics = weak_topics or [skill]
    cache_key = "|".join(topics)

    if (
        st.session_state.get("weak_area_mcq_key") == cache_key
        and "weak_area_mcqs" in st.session_state
    ):
        return st.session_state.weak_area_mcqs

    weak_area_mcqs = []

    for topic in topics:
        weak_area_mcqs.extend(generate_mcqs(topic))

        if len(weak_area_mcqs) >= 5:
            break

    st.session_state.weak_area_mcq_key = cache_key
    st.session_state.weak_area_mcqs = weak_area_mcqs[:5]

    return st.session_state.weak_area_mcqs


def start_weak_area_practice(weak_topics, skill):
    st.session_state.weak_area_mcqs = get_weak_area_mcqs(weak_topics, skill)
    st.session_state.show_weak_area_practice = True
    st.session_state.weak_area_current = 0
    st.session_state.weak_area_score = 0
    st.session_state.weak_area_history = []
    st.session_state.weak_area_answer_submitted = False


def render_weak_area_practice(weak_topics, skill):
    if not st.session_state.get("show_weak_area_practice"):
        return

    practice_mcqs = st.session_state.get("weak_area_mcqs", [])

    st.subheader("Weak Area Practice")

    if not practice_mcqs:
        st.info("No weak area MCQs were generated.")
        return

    weak_current = st.session_state.get("weak_area_current", 0)
    weak_total = len(practice_mcqs)

    if weak_current >= weak_total:
        render_practice_summary(weak_topics, skill, weak_total)
        return

    weak_question = practice_mcqs[weak_current]

    st.progress(weak_current / weak_total)
    st.write(f"Question {weak_current + 1} / {weak_total}")
    st.write(weak_question["question"])

    weak_answer = st.radio(
        "Choose Your Answer",
        weak_question["options"],
        key=f"weak_q_{weak_current}"
    )

    if st.session_state.get("weak_area_answer_submitted"):
        render_submitted_answer()
        return

    if st.button("Submit Answer"):
        save_practice_answer(weak_question, weak_answer)
        st.rerun()


def save_practice_answer(question, selected_answer):
    is_correct = selected_answer == question["answer"]

    if is_correct:
        st.session_state.weak_area_score += 1

    st.session_state.weak_area_history.append({
        "question": question["question"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "selected": selected_answer,
        "correct": question["answer"],
        "is_correct": is_correct
    })

    st.session_state.weak_area_answer_submitted = True


def render_submitted_answer():
    last_answer = st.session_state.weak_area_history[-1]

    if last_answer["is_correct"]:
        st.success("Correct")
    else:
        st.error("Incorrect")
        st.write(f"Correct Answer: {last_answer['correct']}")

    if st.button("Next Practice Question"):
        st.session_state.weak_area_current += 1
        st.session_state.weak_area_answer_submitted = False
        st.rerun()


def render_practice_summary(weak_topics, skill, weak_total):
    st.success("Weak area practice completed.")
    st.metric(
        "Practice Score",
        f"{st.session_state.get('weak_area_score', 0)}/{weak_total}"
    )

    with st.expander("Weak Practice Review"):
        for index, item in enumerate(
            st.session_state.get("weak_area_history", []),
            start=1
        ):
            st.write(f"Question {index}")
            st.write(item["question"])
            st.write(f"Your Answer: {item['selected']}")
            st.write(f"Correct Answer: {item['correct']}")

            if item["is_correct"]:
                st.success("Correct")
            else:
                st.error("Incorrect")

            st.divider()

    if st.button("Practice Weak Areas Again"):
        start_weak_area_practice(weak_topics, skill)
        st.rerun()
