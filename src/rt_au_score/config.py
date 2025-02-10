from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator
from .preprocessing import PreprocessorConfig
from .heuristics import HeuristicConfig


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
    
    @model_validator(mode="after")
    def validate_after(self) -> Self:
        actions = self.model_dump()["actions"]
        self.heuristics.mouse_events.args_comparer.actions = actions
        self.preprocessor.feature_engineer.checkbox.actions = actions
        return self


__all__ = ["MetricsProcessorConfig"]
