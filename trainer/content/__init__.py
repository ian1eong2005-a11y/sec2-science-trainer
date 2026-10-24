"""Question content registry. Importing the chapter modules registers their templates."""
from . import ch09, ch10, ch11, ch12, ch13, ch14, ch15, ch16  # noqa: F401  (registration side effects)
from .base import TEMPLATES, Question, Template

__all__ = ["TEMPLATES", "Question", "Template"]
