from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator
from .modules.preprocessing import PreprocessorConfig
from .modules.heuristics import HeuristicConfig


class MetricsProcessorConfig(BaseModel):
    """Configuration for metrics processing pipeline."""

    actions: list[dict] = Field(
        default=[
            {"id": "1", "type": "click", "args": {"location": {"x": 1867, "y": 19}}},
            {"id": "3", "type": "click", "args": {"location": {"x": 25, "y": 869}}},
        ],
        description="List of actions to be performed in the pipeline",
    )
    preprocessor: PreprocessorConfig = Field(
        default_factory=PreprocessorConfig,
        description="Configuration for preprocessing",
    )
    heuristics: HeuristicConfig = Field(
        default_factory=HeuristicConfig,
        description="Configuration for heuristic analysis",
    )

    class Config:
        frozen = True

    @model_validator(mode="after")
    def validate_after(self) -> Self:
        actions = self.model_dump()["actions"]
        self.heuristics.mouse_events.args_comparer.actions = actions
        return self


__all__ = ["MetricsProcessorConfig"]
