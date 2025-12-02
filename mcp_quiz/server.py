from fastmcp import FastMCP

from .handlers import (
    list_quizzes,
    create_quiz,
    get_quiz,
    delete_quiz
)

server = FastMCP("Quiz MCP")

@server.tool
def healthz() -> str:
    return f"Quiz MCP!"

#dev only, at least we need to restrict the listed quizzes with auth but it is not implemented
server.tool(list_quizzes)

server.tool(create_quiz)
server.tool(get_quiz)
server.tool(delete_quiz)
