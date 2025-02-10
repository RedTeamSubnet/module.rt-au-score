"""Configuration for checkbox event feature engineering."""

from pydantic import BaseModel, Field


class CheckboxFeatureConfig(BaseModel):
    """Configuration for checkbox feature engineering."""

    input_field: str = Field(default="mouse_clicks")
    output_validation: str = Field(default="is_valid")
    output_avg_angle_degrees: str = Field(default="avg_angle_degrees")
    output_angle_consistency: str = Field(default="angle_consistency")
    output_straightness: str = Field(default="straightness")
    output_main: str = Field(default="between_path")

    type: str = Field(default="click", description="Type of event")
    argument_key: str = Field(default="args", description="Key for arguments")
    metrics: dict[str, dict] = Field(
        default={"location": {"x": "x", "y": "y"}}, description="Metrics for location"
    )
    tolerance: int = Field(default=15, description="Tolerance for location matching")
    actions: list[dict] = Field(
        default=[
            {"id": "1", "type": "click", "args": {"location": {"x": 100, "y": 200}}},
        ],
        description="List of actions to be performed in the pipeline",
    )

class SessionConfig(BaseModel):
    """Configuration for checkbox feature engineering."""

    input_field: str = Field(
        default="mouse_movements", description="Field name for session time count"
    )
    output_filed: str = Field(
        default="session_time", description="Field name for session time count"
    )

    class Config:
        """Pydantic configuration."""

        frozen = True
