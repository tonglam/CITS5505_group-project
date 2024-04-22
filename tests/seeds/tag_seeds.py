"""This module seeds the database with initial tag data for testing. """

from app.extensions import db
from app.models.tag import Tag


def create_seed_tag_data() -> list:
    """Create seed tag data."""

    return [
        {"name": "LossRecovery"},
        {"name": "QuestionCreation"},
        {"name": "QuizMaking"},
        {"name": "ProblemSolving"},
        {"name": "CreativeChallenges"},
        {"name": "AnalyticalThinking"},
        {"name": "KnowledgeSeeking"},
        {"name": "LearningJourney"},
        {"name": "TestPreparation"},
        {"name": "BrainTeasers"},
        {"name": "LogicalReasoning"},
        {"name": "DataAnalysis"},
        {"name": "CriticalThinking"},
        {"name": "MemoryEnhancement"},
        {"name": "DecisionMaking"},
        {"name": "ProblemIdentification"},
        {"name": "SkillDevelopment"},
        {"name": "CognitiveTraining"},
        {"name": "ResearchSkills"},
        {"name": "MindMapping"},
    ]


def seed_tag():
    """Seed the database with initial tag data."""

    seed_tag_data = create_seed_tag_data()
    if not seed_tag_data:
        return

    for data in seed_tag_data:
        tag = Tag(
            name=data["name"],
        )
        db.session.add(tag)

    db.session.commit()
