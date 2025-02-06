from pydantic import BaseModel, Field


class MouseMovementProcessingConfig(BaseModel):
    """Processing-specific configuration for mouse movement analysis."""

    input_field: str = Field(
        default="mouse_movements", description="Field name for mouse movement data"
    )
    click_field: str = Field(
        default="mouse_clicks", description="Field name for mouse movement data"
    )
    min_movements_required: int = Field(
        default=10,
        description="Minimum number of movements required to compute velocity",
    )
    fields: dict = Field(
        default={"x": "x", "y": "y", "timestamp": "timestamp"},
        description="Field names in the movement data",
    )
    velocity_std: str = Field(
        default="mouse_movement_stddev_velocity",
        description="STD of movement velocities. Abnormal if too low or too high",
    )
    velocity_avg: str = Field(
        default="mouse_movement_avg_velocity",
        description="STD of movement velocities. Abnormal if too low or too high",
    )
    pixel_per_movement: str = Field(
        default="pixel_per_movement",
        description="Mouse movements count per traveled distance. calculated by traveled_distance / (movement_count * sampling_rate). Abnormal if too low or too high",
    )
    movement_cont: str = Field(
        default="mouse_movement_count",
        description="Number of mouse movements. Abnormal if too low or too high",
    )

    class Config:
        """Pydantic configuration."""

        frozen = True


class MouseDownUpConfig(BaseModel):
    """Complete configuration for mouse down/up module."""

    down_field: str = Field(default="mouse_mouseDowns")
    mouse_movements: str = Field(default="mouse_movements")

    within_tolerance: int = Field(default=2)
    output_field: str = Field(
        default="mouse_down_up_features",
        description="Field name for the extracted features",
    )

    class Config:
        """Pydantic configuration."""

        frozen = True
