"""
Module: data.py
Author: Billy Presume
Created: 2025-05-30
Modified: 2025-05-30
Description: Builds and returns the data for the different sections of the website.
"""

from typing import Any
from .models import (Bio, Education, Aspirations, Job, TechStack, ImpactStat, RecognitionHighlight)

# ------------------------------
# BIO SECTION
# ------------------------------


def build_bio() -> Bio:
    """
    Builds the user's bio, including education and aspirations.

    Returns:
        Bio: Structured personal information object.
    """
    education = [
        Education(
            institution="Johns Hopkins Univeristy",
            degree="M.Sc in Engineering Management",
            graduated="Expected Fall 2026",
            location="Baltimore, MD",
            awards="",
            extracurriculars="",
            relevant_courses=""
        ),
        Education(
            institution="Franciscan Univeristy of Steubenville",
            degree="B.Sc. in Computer Science",
            graduated="Graduated May 2022",
            location="Steubenville, Ohio",
            awards="Mentors Found Scholarship, Dean’s List, 1st Team All-Conf. (PAC), 4-Year Scholar Athlete",
            extracurriculars="#3 Singles & #1 Doubles Tennis Player, SWE Club, Cyber Security Club, Chess Club",
            relevant_courses="OOP, Calculus I & II, Matrix Theory I & II, Discrete Math, Database Systems., Linux & Scripting, Web Dev., Software Q.A., Software Arch."

        )
    ]

    aspirations = [
        Aspirations(
            job_title="Director of Engineering",
            impact="Bridge engineering and leadership through scalable, sustainable systems.",
            progress="Leading backend teams while advancing in data science and technical strategy."
        ),
        Aspirations(
            job_title="VP of Engineering",
            impact="Build future-ready teams and systems rooted in ethical, sustainable engineering.",
            progress="Driving org-wide impact and mentoring emerging engineering leaders."
        )
    ]

    return Bio(
        name="Billy Presume",
        current_position="Senior Data Analyst and Web Developer at Hilton",
        location="Northern Virginia",
        passions=[
            "Engineering/Tinkering", "Chess/Outdoors", "Sports", "Food", "Learning new things"
        ],
        fun_fact="I'm petrified of frogs and I love ranch (the salad dressing).",
        education=education,
        aspirations=aspirations
    )


# ------------------------------
# EXPERIENCE SECTION
# ------------------------------


def build_jobs() -> list[Job]:
    """
    Builds the list of professional experiences.

    Returns:
        list[Job]: A list of Job instances.
    """
    return [
        Job(
            title="Software Engineer",
            company="Google",
            years="2021–Present",
            description=
            "Lead backend development for real-time data pipelines powering analytics across products."
        ),
        Job(
            title="Software Engineering Intern",
            company="Amazon",
            years="Summer 2020",
            description=
            "Worked on serverless architecture optimizations for internal Lambda services."
        )
    ]


def build_tech_stack() -> TechStack:
    """
    Builds the tech stack of languages, tools, and frameworks.

    Returns:
        TechStack: The developer's tech stack.
    """
    return TechStack(
        languages=["JavaScript", "Python", "C/C++", "Swift", "Some VBA"],
        tools=["Docker", "Git", "PostgreSQL/MSSQL/T-SQL", ""],
        frameworks=["Flask", "FastAPI", "SvelteKit", ".NET"]
    )


def build_impact_stats() -> list[ImpactStat]:
    """
    Builds a list of career-related impact statistics.

    Returns:
        list[ImpactStat]: List of quantifiable impact items.
    """
    return [
        ImpactStat(label="Projects", value="15+"),
        ImpactStat(label="Users Impacted", value="100,000+"),
        ImpactStat(label="Open Source Contributions", value="40+")
    ]


# ------------------------------
# RECOGNITION SECTION
# ------------------------------


def build_recognition() -> list[RecognitionHighlight]:
    """
    Builds the list of recognitions and career highlights.

    Returns:
        list[RecognitionHighlight]: Awards and public highlights.
    """
    return [
        RecognitionHighlight(
            title="Top 10 Under 30",
            subtitle="TechWorld",
            year_or_detail="2023",
            description="Recognized for open source leadership and innovation."
        ),
        RecognitionHighlight(
            title="TEDx Speaker",
            subtitle="TEDxCambridge",
            year_or_detail="2022",
            description="Spoke on ethical frameworks in AI systems."
        ),
        RecognitionHighlight(
            title="Featured in Wired",
            subtitle="Wired Magazine",
            year_or_detail="2021",
            description="Profiled for building accessible civic tech tools."
        )
    ]


# ------------------------------
# MAIN DATA AGGREGATOR
# ------------------------------


def get_portfolio_data() -> dict[str, Any]:
    """
    Aggregates all homepage portfolio data.

    Returns:
        dict[str, Any]: Dictionary of homepage data for rendering.
    """
    return {
        "bio": build_bio(), "jobs": build_jobs(), "tech_stack": build_tech_stack(),
        "impact_stats": build_impact_stats(), "recognition_highlights": build_recognition()
    }
