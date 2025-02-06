"""Configuration for checkbox event feature engineering."""

from pydantic import BaseModel, Field


class CheckboxFeatureConfig(BaseModel):
    """Configuration for checkbox feature engineering."""

    input_field: str = Field(
        default="mouse_clicks", description="Field name for checkbox interactions"
    )

    class Config:
        """ Pydantic configuration."""
        frozen = True

class SessionConfig(BaseModel):
    """Configuration for checkbox feature engineering."""

    input_field: str = Field(
        default="mouse_movements", description="Field name for session time count"
    )
    output_filed: str = Field(
        default="session_time", description="Field name for session time count"
    )

    class Config:
        """ Pydantic configuration."""
        frozen = True
