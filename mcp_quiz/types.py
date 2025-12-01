"""
Type definitions for quiz data structures.

This module contains TypedDict classes for type-safe quiz question data.
"""
from typing import TypedDict, List, Dict, Literal, Union

class FillBlankData(TypedDict):
    text_with_blanks: str
    blanks: List[str]

class ColumnMatchData(TypedDict):
    left_column: List[str]
    right_column: List[str]
    correct_pairs: Dict[int, int]

class MultipleChoiceData(TypedDict):
    options: List[str]
    correct_index: int

class Question(TypedDict):
    question_type: Literal['fill_blank', 'column_match', 'multiple_choice']
    question_text: str
    question_data: Union[FillBlankData, ColumnMatchData, MultipleChoiceData]
    order_index: int

class QuizResult(TypedDict):
    quiz_id: str
    success: bool
