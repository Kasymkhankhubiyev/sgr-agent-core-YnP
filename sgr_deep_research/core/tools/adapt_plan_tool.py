from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from sgr_deep_research.core.base_tool import BaseTool

if TYPE_CHECKING:
    from sgr_deep_research.core.models import ResearchContext


class AdaptPlanTool(BaseTool):
    """Adapt research plan based on new findings."""

    reasoning: str = Field(description="Why plan needs adaptation based on new data")
    original_goal: str = Field(description="Original research goal")
    new_goal: str = Field(description="Updated research goal")
    plan_changes: list[str] = Field(description="Specific changes made to plan")
    next_steps: list[str] = Field(description="Updated remaining steps")

    async def __call__(self, context: ResearchContext) -> str:
        return self.model_dump_json(
            indent=2,
            exclude={
                "reasoning",
            },
        )
