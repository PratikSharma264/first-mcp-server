from django.db import models


class Todo(models.Model):
    """A task saved by an MCP tool call."""

    # Store the task text and when it first entered the list
    task = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.task


