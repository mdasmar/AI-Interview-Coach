# Project Description: AI Interview Coach

## Overview

AI Interview Coach is an AI-powered technical interview preparation app that creates a personalized interview from a candidate's resume. Instead of giving generic practice questions, it reads the candidate's resume, extracts relevant skills, generates an interview for a selected skill, evaluates the candidate's answers, and provides targeted feedback.

## Problem Solved

Many candidates list technical skills on their resumes but struggle to verify whether they can explain those skills in an interview. Existing preparation tools are often generic and disconnected from the candidate's actual resume. This project solves that gap by converting resume content into a focused interview experience and showing where the candidate is strong, weak, or ready for deeper questions.

## Features

- Resume upload: Candidates can upload a PDF resume.
- Skill extraction: The app extracts technical skills from resume text.
- Demo Mode: Judges and users can test the app instantly without uploading a resume.
- Skill-based interview: Users select one skill and receive a 10-question MCQ interview.
- Automatic scoring: The app tracks selected answers, correct answers, score, and accuracy.
- Candidate dashboard: Shows score, attempted questions, strong topics, weak topics, topic performance, difficulty performance, and interview readiness.
- Gap analysis: Compares resume skills with tested topics and highlights areas that need more validation.
- AI career report: Generates a structured interview analysis and learning plan.
- Downloadable report: Exports the analysis as a Markdown report.
- Weak-area practice: If the candidate misses questions, the app offers targeted follow-up practice.
- Perfect-score challenge: If the candidate scores 10/10, a congratulatory popup unlocks a Go Beyond challenge with 5 hard questions.
- Stable fallbacks: The app includes fallback questions and reports so the demo remains functional even if the AI service is unavailable.

## Functionality

1. The user uploads a PDF resume or enables Demo Mode.
2. Resume text is extracted and technical skills are identified.
3. The user selects a skill for the interview.
4. The app generates 10 MCQs for that skill.
5. The user answers each question interactively.
6. The app calculates score, accuracy, topic performance, weak topics, strong topics, and readiness.
7. The user can review answers and download the report.
8. Based on performance:
   - Below perfect score: the user receives a Practice Weak Areas flow.
   - Perfect score: the user receives a centered congratulatory popup and unlocks the Go Beyond hard-question challenge.

## Technology Used

- Python for backend logic and app structure.
- Streamlit for the interactive web UI.
- Azure AI Foundry project client for connecting to the AI project.
- Azure OpenAI-compatible Responses API for question generation, skill extraction, and reporting.
- Azure Identity for authentication through `DefaultAzureCredential`.
- pypdf for extracting text from uploaded resume PDFs.
- python-dotenv for local environment variable loading.
- Markdown for downloadable report output.

## Impact

AI Interview Coach helps candidates prepare more efficiently by focusing practice on the exact skills they claim on their resumes. It gives immediate feedback, identifies weak areas, rewards mastery with harder questions, and creates a polished report that candidates can use as a study plan.
