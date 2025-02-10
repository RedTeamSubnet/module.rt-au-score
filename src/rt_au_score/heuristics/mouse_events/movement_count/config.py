"""Configuration for movement count analysis."""

from pydantic import BaseModel, Field


class MovementCountConfig(BaseModel):
    class Config:
        frozen = True

    pixel_per_movement: str = Field(default="pixel_per_movement")
    mouse_movement_count: str = Field(default="mouse_movement_count")

    min_pixel_count: int = Field(default=8)
    min_pixel_count_too_low: int = Field(default=4)
    max_pixel_count: int = Field(default=30)

    min_movement_count: int = Field(default=150)
    min_movement_count_too_low: int = Field(default=10)
    max_movement_count: int = Field(default=500)

