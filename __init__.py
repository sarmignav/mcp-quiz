"""
MCP Quiz - A package for quiz management.
"""

from .types import Question, QuizResult
from .handlers import create_quiz, list_quizzes, get_quiz
from .server import server

__all__ = [
    'Question',
    'QuizResult', 
    'create_quiz',
    'list_quizzes',
    'get_quiz',
    'server',
]
