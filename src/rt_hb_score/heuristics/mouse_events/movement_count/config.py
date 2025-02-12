"""Configuration for movement count analysis."""

from pydantic import BaseModel, Field


class MovementCountConfig(BaseModel):
    class Config:
        frozen = True

    pixel_per_movement: str = Field(default="pixel_per_movement")
    mouse_movement_count: str = Field(default="mouse_movement_count")
    mouse_angle_std: str = Field(default="overall_session_angle_std")

    min_pixel_count: float = Field(default=6.75)
    min_pixel_count_too_low: float = Field(default=3)
    max_pixel_count: float = Field(default=16.862)

    min_movement_count: float = Field(default=250)
    min_movement_count_too_low: float = Field(default=50)
    max_movement_count: float = Field(default=750)

    min_total_angle_std: float = Field(
        default=17.523,
        description="Minimum expected velocity average",
    )
    min_total_angle_std_too_low: float = Field(default=10)
    max_total_angle_std: float = Field(
        default=23.512,
        description="Maximum expected velocity average",
    )
