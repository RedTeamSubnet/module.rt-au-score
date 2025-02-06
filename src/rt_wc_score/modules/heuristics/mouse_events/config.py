"""Configuration for mouse events analysis."""

from pydantic import BaseModel, Field

from .velocity import VelocityConfig
from .movement_count import MovementCountConfig
from .checkbox_path import CheckboxPathConfig
from .compare import ArgCompareConfig

class MouseEventConfig(BaseModel):
    """Configuration for mouse event analysis."""

    class Config:
        """Pydantic configuration."""

        frozen = True

    velocity_std: str = Field(default="mouse_movement_stddev_velocity")
    velocity_avg: str = Field(default="mouse_movement_avg_velocity")
    distance_count: str = Field(default="pixel_per_movement")
    mouse_movement_count: str = Field(default="mouse_movement_count")
    session_time: str = Field(default="session_time")
    checkbox_path_score: str = Field(default="checkbox_path_score")
    mouse_down_check: str = Field(default="mouse_down_up_features")

    velocity: VelocityConfig = Field(
        default_factory=VelocityConfig, description="Velocity analysis configuration"
    )
    movement_count: MovementCountConfig = Field(
        default_factory=MovementCountConfig,
        description="Movement count analysis configuration",
    )
    checkbox_path: CheckboxPathConfig = Field(
        default_factory=CheckboxPathConfig,
        description="Checkbox path analysis configuration",
    )

    args_comparer: ArgCompareConfig = Field(
        default_factory=ArgCompareConfig,
        description="Arguments comparer configuration",
    )
    velocity_std_weight: float = Field(default=0.5)
    velocity_avg_weight: float = Field(default=0.5)
    distance_weight: float = Field(default=2)
    movement_count_weight: float = Field(default=1)
    session_time_weight: float = Field(default=2)
    checkbox_path_weight: float = Field(default=3)
    mouse_down_weight: float = Field(default=3)
