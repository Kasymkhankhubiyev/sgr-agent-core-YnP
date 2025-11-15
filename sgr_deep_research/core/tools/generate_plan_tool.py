from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from sgr_deep_research.core.base_tool import BaseTool

if TYPE_CHECKING:
    from sgr_deep_research.core.models import ResearchContext


class GeneratePlanTool(BaseTool):
    """Generate research plan.

    Useful to split complex request into manageable steps.
    """

    reasoning: str = Field(description="Justification for research approach")
    research_goal: str = Field(description="Primary research objective")
    planned_steps: list[str] = Field(description="List of 3-4 planned steps")
    search_strategies: list[str] = Field(description="Information search strategies")

    async def __call__(self, context: ResearchContext) -> str:
        return self.model_dump_json(
            indent=2,
            exclude={
                "reasoning",
            },
        )
