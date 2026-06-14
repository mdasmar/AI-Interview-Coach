import streamlit as st

from mcq_generator import generate_hard_mcqs


BEYOND_QUESTION_COUNT = 5


def get_beyond_mcqs(skill):
    cache_key = f"beyond|{skill}"

    if (
        st.session_state.get("beyond_mcq_key") == cache_key
        and "beyond_mcqs" in st.session_state
    ):
        return st.session_state.beyond_mcqs

    beyond_mcqs = generate_hard_mcqs(skill)

    st.session_state.beyond_mcq_key = cache_key
    st.session_state.beyond_mcqs = beyond_mcqs[:BEYOND_QUESTION_COUNT]

    return st.session_state.beyond_mcqs


def start_beyond_practice(skill):
    st.session_state.beyond_mcqs = get_beyond_mcqs(skill)
    st.session_state.show_beyond_practice = True
    st.session_state.beyond_current = 0
    st.session_state.beyond_score = 0
    st.session_state.beyond_history = []
    st.session_state.beyond_answer_submitted = False


def render_beyond_practice(skill):
    if not st.session_state.get("show_beyond_practice"):
        return

    beyond_mcqs = st.session_state.get("beyond_mcqs", [])

    st.subheader("Go Beyond Challenge")

    if not beyond_mcqs:
        st.info("No hard challenge questions were generated.")
        return

    beyond_current = st.session_state.get("beyond_current", 0)
    beyond_total = len(beyond_mcqs)

    if beyond_current >= beyond_total:
        render_beyond_summary(beyond_total)
        return

    beyond_question = beyond_mcqs[beyond_current]

    st.progress(beyond_current / beyond_total)
    st.write(f"Hard Question {beyond_current + 1} / {beyond_total}")
    st.write(beyond_question["question"])

    beyond_answer = st.radio(
        "Choose Your Answer",
        beyond_question["options"],
        key=f"beyond_q_{beyond_current}"
    )

    if st.session_state.get("beyond_answer_submitted"):
        render_beyond_submitted_answer()
        return

    if st.button("Submit Hard Answer"):
        save_beyond_answer(beyond_question, beyond_answer)
        st.rerun()


def save_beyond_answer(question, selected_answer):
    is_correct = selected_answer == question["answer"]

    if is_correct:
        st.session_state.beyond_score += 1

    st.session_state.beyond_history.append({
        "question": question["question"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "selected": selected_answer,
        "correct": question["answer"],
        "is_correct": is_correct
    })

    st.session_state.beyond_answer_submitted = True


def render_beyond_submitted_answer():
    last_answer = st.session_state.beyond_history[-1]

    if last_answer["is_correct"]:
        st.success("Correct")
    else:
        st.error("Incorrect")
        st.write(f"Correct Answer: {last_answer['correct']}")

    if st.button("Next Hard Question"):
        st.session_state.beyond_current += 1
        st.session_state.beyond_answer_submitted = False
        st.rerun()


def render_beyond_summary(beyond_total):
    st.success("Go Beyond challenge completed.")
    st.metric(
        "Hard Challenge Score",
        f"{st.session_state.get('beyond_score', 0)}/{beyond_total}"
    )

    with st.expander("Hard Challenge Review"):
        for index, item in enumerate(
            st.session_state.get("beyond_history", []),
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

    if st.button("Try Go Beyond Again"):
        start_beyond_practice(st.session_state.get("skill", ""))
        st.rerun()
