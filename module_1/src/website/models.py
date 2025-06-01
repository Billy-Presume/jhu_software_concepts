"""
Module: models.py
Author: Billy Presume
Created: 2025-05-30
Modified: 2025-05-30
Description: Defines the data structures for the defferent sections of the website.
"""

from dataclasses import dataclass

# ------------------------------
# Bio, Education, Aspirations
# ------------------------------


@dataclass
class Education:
    """Represents an educational credential."""
    institution: str
    degree: str
    graduated: str  # e.g. "2021", "Expected 2025", or "In progress"
    location: str
    awards: str
    extracurriculars: str
    relevant_courses: str


@dataclass
class Aspirations:
    """Represents a career aspiration."""
    job_title: str
    impact: str
    progress: str  # Explanation of current progress toward aspiration


@dataclass
class Bio:
    """Contains personal information and background."""
    name: str
    current_position: str
    location: str
    passions: list[str]
    fun_fact: str
    education: list[Education]
    aspirations: list[Aspirations]


# ------------------------------
# Experience Section
# ------------------------------


@dataclass
class Job:
    """Professional experience entry."""
    title: str
    company: str
    years: str
    description: str


@dataclass
class TechStack:
    """Technical skills overview."""
    languages: list[str]
    tools: list[str]
    frameworks: list[str]


@dataclass
class ImpactStat:
    """Measurable impact or career stats."""
    label: str
    value: str


# ------------------------------
# Recognition & Highlights
# ------------------------------


@dataclass
class RecognitionHighlight:
    """Award, public recognition, or notable career milestone."""
    title: str
    subtitle: str
    year_or_detail: str
    description: str
