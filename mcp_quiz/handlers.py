import logging
from typing import Dict, List, Any, Optional

from .supabase import client as sb
from .types import (
    Question,
    QuizResult
)

# Set up logging
logger = logging.getLogger(__name__)

def list_quizzes():
    """
    Get all quizzes.
    """
    return sb.table("quizzes").select("*").execute()

def _get_user(email: str):
    try:
        return (
            sb.table('user_profiles')
            .select('id')
            .eq('email', email)
            .maybe_single()
            .execute()
        )

    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return None

def _get_quiz(quiz_id: str):
    try:
        return (
            sb.table('quizzes')
            .select('*')
            .eq('id', quiz_id)
            .maybe_single()
            .execute()
        )

    except Exception as e:
        logger.error(f"Error fetching quiz: {e}")
        return None

def _insert_quiz(quiz_data):
    try:
        return (
            sb.table('quizzes')
            .insert(quiz_data)
            .execute()
        )

    except Exception as e:
        logger.error(f"Error creating quiz: {e}")
        return None

def _delete_quiz(quiz_id: str):
    try:
        return (
            sb.table('quizzes')
            .delete()
            .eq('id', quiz_id)
            .execute()
        )

    except Exception as e:
        logger.error(f"Error deleting quiz: {e}")
        return None

def _get_questions(quiz_id: str):
    try:
        return (
            sb.table('questions')
            .select('*')
            .eq('quiz_id', quiz_id)
            .execute()
        )

    except Exception as e:
        logger.error(f"Error fetching questions: {e}")
        return None

def _insert_questions(questions_data):
    try:
        return (
            sb.table('questions')
            .insert(questions_data)
            .execute()
        )

    except Exception as e:
        logger.error(f"Error creating questions: {e}")
        return None

# START MCP HANDLERS

def create_quiz(
    title: str,
    description: str,
    is_public: bool,
    questions: List[Question]
) -> QuizResult:
    """
    Create a new quiz with questions.

    Args:
        title: The title of the quiz
        description: Description of the quiz
        is_public: Whether the quiz should be publicly accessible
        questions: List of Question objects where each contains:
            - question_type: One of 'fill_blank', 'column_match', 'multiple_choice'
            - question_text: The text of the question
            - question_data: Type-specific question data matching the question_type:
                - fill_blank: FillBlankData with text_with_blanks and blanks
                - column_match: ColumnMatchData with left_column, right_column, and correct_pairs
                - multiple_choice: MultipleChoiceData with options and correct_index
            - order_index: The order of the question in the quiz

    Returns:
        Dictionary with quiz_id and success status

    Example:
        >>> create_quiz(
        ...     title="Math Quiz",
        ...     description="Basic mathematics questions",
        ...     is_public=True,
        ...     questions=[
        ...         {
        ...             "question_type": "fill_blank",
        ...             "question_text": "What's the capital of Mexico?",
        ...             "question_data": {
        ...                 "text_with_blanks": "The capital of Mexico is ____",
        ...                 "blanks": ["Mexico City"]
        ...             },
        ...             "order_index": 0
        ...         },
        ...         {
        ...             "question_type": "column_match",
        ...             "question_text": "Match the following mathematical operations",
        ...             "question_data": {
        ...                 "left_column": ["3+1", "5-3", "2*4", "9/3"],
        ...                 "right_column": ["3", "2", "8", "4"],
        ...                 "correct_pairs": { "0": 3, "1": 1, "2": 2, "3": 0 }
        ...             },
        ...             "order_index": 1
        ...         },
        ...         {
        ...             "question_type": "multiple_choice",
        ...             "question_text": "What is 2+2?",
        ...             "question_data": {
        ...                 "options": ["3", "4", "5", "6"],
        ...                 "correct_index": 1
        ...             },
        ...             "order_index": 2
        ...         }
        ...     ]
        ... )
    """
    try:
        # For demo purposes, we'll use a demo user
        demo_email = "mcp@example.com"

        user = _get_user(demo_email)

        if user is None:
            return {"success": False, "error": "User not found"}
        
        # Create the quiz
        quiz_data = {
            "creator_id": user.data['id'],
            "title": title,
            "description": description,
            "is_public": is_public
        }

        quiz = _insert_quiz(quiz_data)

        if quiz is None:
            return {"success": False, "error": "Error creating quiz"}
        
        # Create questions
        questions_to_insert = []
        for question in questions:
            question_data = {
                "quiz_id": quiz_response.data[0]['id'],
                "question_type": question['question_type'],
                "question_text": question['question_text'],
                "question_data": question['question_data'],
                "order_index": question['order_index']
            }
            questions_to_insert.append(question_data)

        questions = _insert_questions(questions_to_insert)

        if questions is None:
            return {"success": False, "error": "Error inserting questions"}

        return {
            "success": True,
            "quiz_id": quiz_id,
            "questions_created": len(questions_to_insert)
        }

    except Exception as e:
        logger.error(f"Unexpected error in create_quiz: {str(e)}")
        return {"success": False, "error": str(e)}

def get_quiz(
    quiz_id: str,
) -> Dict[str, Any]:
    """
    Get a quiz including questions and correct answers.

    Args:
        quiz_id: The ID of the quiz to get

    Returns:
        Dictionary with the quiz, the questions, and the correct answers.
    """
    try:
        quiz = _get_quiz(quiz_id)

        if quiz is None:
            return {"success": False, "error": "Quiz not found"}
            
        # Get the quiz questions
        questions = _get_questions(quiz_id) 

        if questions is None:
            return {"success": False, "error": "No questions found for this quiz"}
    
        return {
            "success": True,
            "quiz_id": quiz_id,
            "quiz": quiz,
            "questions": questions
        }

    except Exception as e:
        logger.error(f"Unexpected error in get_quiz: {str(e)}")
        return {"success": False, "error": str(e)}
    
def delete_quiz(quiz_id: str) -> Dict[str, Any]:
    """
    Delete a quiz and all its questions.
    
    Args:
        quiz_id: The ID of the quiz to delete
    
    Returns:
        Dictionary with success status and details
    """
    try:
        # First, check if the quiz exists
        quiz = _get_quiz(quiz_id)

        if quiz is None:
            return {"success": False, "error": "Quiz not found"}
        
        # Delete the quiz (this will cascade delete questions and answers)
        delete = _delete_quiz(quiz_id)
        
        if delete is None:
            return {"success": False, "error": "Error deleting the quizz"}
        
        return {
            "success": True,
            "message": f"Quiz {quiz_id} and all related data have been deleted"
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in destroy_quiz: {str(e)}")
        return {"success": False, "error": str(e)}
