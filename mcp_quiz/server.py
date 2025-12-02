from fastmcp import FastMCP
from .supabase import client as sb

from .handlers import (
    create_quiz,
    get_quiz,
    delete_quiz
)

server = FastMCP("Quiz MCP")

@server.tool
def healthz() -> str:
    return f"Quiz MCP!"

#dev only, at least we need to restrict the listed quizzes with auth but it is not implemented
@server.tool
def list_quizzes():
    """
    Get all quizzes.
    """
    return sb.table("quizzes").select("*").execute()

server.tool(create_quiz)
server.tool(get_quiz)
server.tool(delete_quiz)
