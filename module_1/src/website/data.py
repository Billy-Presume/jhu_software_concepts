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
            awards=
            "Mentors Found Scholarship, Dean’s List, 1st Team All-Conference (PAC), 4-Year Scholar Athlete",
            extracurriculars=
            "#3 Singles & #1 Doubles Tennis Player, SWE Club, Cyber Security Club, Chess Club",
            relevant_courses=
            "OOP, Calculus I & II, Matrix Theory I & II, Discrete Math, Database Systems., Linux & Scripting, Web Dev., Software Q.A., Software Architecture"
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
            impact=
            "Build future-ready teams and systems rooted in ethical, sustainable engineering.",
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
            title="Senior Data Analyst & Web Developer",
            company="Hilton, Inc.",
            years="Jan 2023 – Present",
            description=
            "Lead development for real-time data pipelines and automations powering analytics across orgs. Worked on serverless architecture optimizations for internal revenue managament consumtion needs.",
            location="Remote, USA",
            highlights=[
                "Single-handedly developed a full-stack IDP authenticated web analytics platform using JavaScript, Python (Pandas & NumPy), Node & Express.js and T-SQL which leveraged predictive modeling, data visualization, and machine learning, improving revenue management for Hilton\u2019s 8,400+ hotels. Achieved 100% satisfaction, saving over $3.6 million annually and reducing analysis time by 1,500 hours.",
                "Redesigned a Revenue Management toolkit with VBA, ensuring 100% compatibility with Hilton\u2019s global hotel portfolio and saving over 6,000 hours per week in data balancing tasks across 8,400+ hotels company wide.",
                "Created advanced data transformation models using SQL, Python with NumPy and Pandas to process and clean over 13 billion records, resulting in a 57% reduction in data processing time and delivering actionable insights that improved decision-making efficiency across Hilton\u2019s 24+ brands and market segments.",
                "Facilitated Node.js deployments on IIS with iisnode, increasing web performance by 23%."
            ]
        )
    ]


def build_tech_stack() -> TechStack:
    """
    Builds the tech stack of languages, tools, and frameworks.

    Returns:
        TechStack: The developer's tech stack.
    """
    return TechStack(
        languages=[
            "JavaScript", "Python", "C/C++", "Swift", "VBA", "HTML", "CSS", "SQL", "T-SQL",
            "Shell Script", "Batch Script"
        ],
        tools=[
            # Data Engineering & ETL
            ["Alteryx", "Apache Spark", "Apache Kafka", "Databricks", "SSIS Packages"],
            # BI & Visualization
            ["Tableau", "Power BI", "Excel", "Google Data Studio"],
            # DevOps & CI/CD
            ["Docker", "Kubernetes", "Jenkins", "Git", "GitHub Actions", "Bamboo", "Azure DevOps"],
            # Web Dev & Frontend/Backend Tools
            ["Postman", "Fiddler", "Chrome DevTools", "Webpack", "Vite", "NPM", "Yarn"],
            # Database & Query Tools
            [
                "PostgreSQL", "MSSQL", "MySQL", "T-SQL", "Oracle DB", "MongoDB", "Redis",
                "DBVisualizer", "DBeaver", "SQL Server Management Studio (SSMS)"
            ],
            # Cloud & Server Management
            ["AWS Management Console", "IIS", "Remote Desktop", "Apache HTTP Server", "NGINX"],
            # Security & Governance
            ["Checkmarx SCA", "SonarQube"],
            # Project & Process Management
            ["Jira", "Confluence", "ServiceNow", "Draw.io", "Visio", "SharePoint"]
        ],
        frameworks=[
            "React", "React Native", "SvelteKit", "Flask", "FastAPI", ".NET", "Node.js",
            "Express.js", "Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Seaborn", "Plotly"
        ]
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
            title="From My Org. VP",
            subtitle="Driving innovation & harnessing efficiency.",
            company="Hilton, Inc.",
            location="Remote, USA",
            year_or_detail="Apr. 2025",
            description=
            "Billy, I heard you recently recreated the new analytics website and the feedback is really great now that reporting is all in one place. Thank you for your efforts."
        ),
        RecognitionHighlight(
            title="From My Manager",
            subtitle="Interactive, insightful, & redefined visualizations.",
            company="Hilton, Inc.",
            location="Remote, USA",
            year_or_detail="Jan. 2025",
            description=
            "Thank you, Billy, for your innovative design of the revenue management monitoring website. Your efforts resulted in an invaluable tool that enhances our ability to monitor and visualize metrics in an enhanced, user-friendly interface. This will help empower our team and stakeholders with valuable information and has eliminated several hours of manual reporting. You have set a new standard, and we are already receiving positive feedback. Keep up the great work!"
        ),
        RecognitionHighlight(
            title="From My Coworker",
            subtitle="Mentoring with purpose, growing with impact.",
            company="Hilton, Inc.",
            location="Remote, USA",
            year_or_detail="Dec. 2024",
            description=
            "Thank you Billy for helping me understand Python and fixing our automation pipeline. You make things easier to understand."
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
