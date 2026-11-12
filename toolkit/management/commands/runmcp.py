from django.core.management.base import BaseCommand
from mcp.server import MCPServer
from typing import Literal
import random
from toolkit.models import *

# Register every project tool on one MCP server
mcp = MCPServer("Django Toolkit")


class Command(BaseCommand):
    """Run the local MCP server through Django."""

    help = "Run the Django Toolkit MCP server over stdio"

    def handle(self, *args, **options):
        # Keep the process open while the host communicates over stdio
        mcp.run()


# Registering a Calculator that can perform basic operation through the MCP Server.
@mcp.tool() #For registering the calculate() function with the server.
def calculate(
    operation: Literal["add", "subtract", "multiply", "divide"],
    a: float,
    b: float,
) -> str:
    """Perform a math operation on two numbers."""
    # Select the requested operation after MCP validates the inputs
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    else:
        if b == 0:
            return "Cannot divide by zero."
        result = a / b

    return f"{a} {operation} {b} = {result}"

# Registering a random number generator that can generate a random integer between two numbers through the MCP Server.
@mcp.tool()
def random_number(minimum: int, maximum: int) -> str:
    """Generate a random integer inside an inclusive range."""
    # Reject a reversed range with a message the model can explain
    if minimum > maximum:
        return "The minimum must be less than or equal to the maximum."

    result = random.randint(minimum, maximum)
    return f"Random number between {minimum} and {maximum}: {result}"

#Registering a to-do list tool that can add a task to the Django to-do list through the MCP Server.
@mcp.tool()
def add_todo(task: str) -> str:
    """Save a task in the Django to-do list."""
    # Persist the task so it survives MCP server restarts
    todo = Todo.objects.create(task=task)
    return f'Added "{todo.task}" as task {todo.pk}.'

#Registering a to-do list tool that can list all tasks in the Django to-do list through the MCP Server.
@mcp.tool()
def list_todos() -> str:
    """List every task saved in the Django database."""
    # Read a stable sequence so the displayed numbers stay predictable
    todos = Todo.objects.order_by("created_at", "pk")
    if not todos.exists():
        return "The to-do list is empty."

    return "\n".join(
        f"{position}. {todo.task}"
        for position, todo in enumerate(todos, start=1)
    )


@mcp.resource(
    "todo://list",
    name="todo_list",
    title="To-Do List",
    mime_type="text/plain",
)
def todo_resource() -> str:
    """Every task saved in the Django database."""
    # Return the same durable rows as read-only resource content
    todos = Todo.objects.order_by("created_at", "pk")
    if not todos.exists():
        return "The to-do list is empty."

    return "\n".join(
        f"{position}. {todo.task}"
        for position, todo in enumerate(todos, start=1)
    )