from azure_client import (
    client,
    DEPLOYMENT
)
import re


KNOWN_TECHNICAL_SKILLS = [
    "Python",
    "C",
    "C++",
    "C#",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Next.js",
    "Node.js",
    "Express",
    "Django",
    "Flask",
    "FastAPI",
    "Streamlit",
    "HTML",
    "CSS",
    "Tailwind CSS",
    "Bootstrap",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Firebase",
    "Azure",
    "AWS",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Linux",
    "REST API",
    "GraphQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "OpenCV",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Power BI",
    "Tableau"
]


def extract_skills_offline(resume_text):
    normalized_resume_text = re.sub(
        r"\s+",
        " ",
        resume_text
    )
    matches = []

    for skill in sorted(KNOWN_TECHNICAL_SKILLS, key=len, reverse=True):
        escaped_skill = re.escape(skill)
        pattern = rf"(?<![A-Za-z0-9+#]){escaped_skill}(?![A-Za-z0-9+#])"

        for match in re.finditer(pattern, normalized_resume_text, flags=re.I):
            if any(
                match.start() < end and match.end() > start
                for start, end, _ in matches
            ):
                continue

            matches.append((match.start(), match.end(), skill))

    skills = [
        skill
        for _, _, skill in sorted(matches, key=lambda item: item[0])
    ]

    if skills:
        return ", ".join(dict.fromkeys(skills))

    return ""


def extract_skills(resume_text):

    prompt = f"""
    You are an expert technical recruiter.

    Extract ONLY technical skills from the resume.

    Rules:
    - Include programming languages
    - Include frameworks
    - Include databases
    - Include cloud technologies
    - Include developer tools
    - Include AI/ML technologies
    - Remove duplicates
    - Return ONLY comma-separated skills
    - No explanation
    - No numbering

    Resume:

    {resume_text}
    """

    try:

        response = client.responses.create(
            model=DEPLOYMENT,
            input=prompt
        )

        return response.output_text.strip()

    except Exception as e:

        print(f"Skill Extraction Error: {e}")
        return extract_skills_offline(resume_text)
