from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from sgr_deep_research.core.base_tool import BaseTool

if TYPE_CHECKING:
    from sgr_deep_research.core.models import ResearchContext


class ClarificationTool(BaseTool):
    """Ask clarifying questions when facing ambiguous request.

    Keep all fields concise - brief reasoning, short terms, and clear questions.
    """

    reasoning: str = Field(
        description="Why clarification is needed (1-2 sentences MAX)"
    )
    unclear_terms: list[str] = Field(
        description="List of unclear terms (brief, 1-3 words each)"
    )
    assumptions: list[str] = Field(
        description="Possible interpretations (short, 1 sentence each)"
    )
    questions: list[str] = Field(
        description="3 specific clarifying questions (short and direct)"
    )

    async def __call__(self, context: ResearchContext) -> str:
        return "\n".join(self.questions)
