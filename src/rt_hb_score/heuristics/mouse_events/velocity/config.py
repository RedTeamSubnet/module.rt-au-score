"""Configuration for velocity-based analysis."""

from pydantic import BaseModel, Field


class VelocityConfig(BaseModel):
    class Config:
        """Pydantic configuration."""

        frozen = True

    velocity_std: str = Field(default="mouse_movement_stddev_velocity")
    velocity_avg: str = Field(default="mouse_movement_avg_velocity")

    min_velocity_variation: float = Field(
        default=499.75,
        description="Minimum expected velocity standard deviation",
    )
    max_velocity_variation: float = Field(
        default=1799.972,
        description="Maximum expected velocity standard deviation",
    )
    min_velocity_avg: float = Field(
        default=389.37,
        description="Minimum expected velocity average",
    )
    max_velocity_avg: float = Field(
        default=911.57,
        description="Maximum expected velocity average",
    )

    weight_stddev: float = Field(
        default=0.5, description="Weight for velocity standard deviation analysis"
    )
    weight_avg: float = Field(
        default=0.5, description="Weight for velocity average analysis"
    )
