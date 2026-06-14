from azure_client import (
    client,
    DEPLOYMENT
)


def generate_fallback_report(
        skill,
        score,
        total,
        stats,
        error=None):

    strong_topics = stats.get("strong_topics", [])
    weak_topics = stats.get("weak_topics", [])
    percentage = stats.get("percentage", 0)

    if percentage >= 90:
        confidence = "Excellent"
    elif percentage >= 75:
        confidence = "Strong"
    elif percentage >= 60:
        confidence = "Average"
    else:
        confidence = "Needs Improvement"

    strong_text = (
        ", ".join(strong_topics)
        if strong_topics
        else "No strong topics identified yet."
    )

    weak_text = (
        ", ".join(weak_topics)
        if weak_topics
        else "No weak topics identified yet."
    )

    return f"""
# Interview Summary

You scored **{score}/{total}** in the **{skill}** interview with **{percentage}%** accuracy.

# Strong Topics

{strong_text}

# Weak Topics

{weak_text}

# Confidence Level

**{confidence}**

# Recommended Resources

- YouTube channels: freeCodeCamp, Programming with Mosh
- Practice platforms: LeetCode, HackerRank

# Four Week Learning Plan

Week 1: Revise fundamentals of {skill}.

Week 2: Practice topic-wise interview questions.

Week 3: Build one small project using {skill}.

Week 4: Take mock interviews and review mistakes.

# Final Recommendation

Focus on your weak topics first, then practice explaining your answers clearly with examples.

_AI service was unavailable, so this polished offline report was generated for the demo._
"""


def generate_report(
        skill,
        score,
        total,
        history,
        stats):

    prompt = f"""
    You are an expert technical interviewer
    and career coach.

    Candidate Skill:
    {skill}

    Interview Score:
    {score}/{total}

    Accuracy:
    {stats['percentage']}%

    Strong Topics:
    {stats['strong_topics']}

    Weak Topics:
    {stats['weak_topics']}

    Interview History:
    {history}

    Generate a professional report with
    the following sections:

    # Interview Summary

    Give a concise performance summary.

    # Strong Topics

    Explain areas where the candidate
    performed well in short points.

    # Weak Topics

    Explain areas requiring improvement in short points.

    # Confidence Level

    Classify candidate as:

    - Excellent
    - Strong
    - Average
    - Needs Improvement

    # Recommended Resources

    Suggest 2 resources:
    - YouTube channels
    - Practice platforms

    # Four Week Learning Plan

    Week 1:
    Topics

    Week 2:
    Topics

    Week 3:
    Topics

    Week 4:
    Topics

    # Final Recommendation

    Provide career guidance in short.

    Format the report using Markdown.
    """

    try:

        response = client.responses.create(
            model=DEPLOYMENT,
            input=prompt
        )

        return response.output_text

    except Exception as e:

        return generate_fallback_report(
            skill,
            score,
            total,
            stats,
            str(e)
        )
