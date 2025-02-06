"""Configuration for feature engineering module."""

from pydantic import BaseModel, Field

from .keyboard_events import KeyboardConfig
from .mouse_events import MouseDownUpConfig, MouseMovementProcessingConfig
from .checkboxes import CheckboxFeatureConfig,SessionConfig


class FeatureEngineerConfig(BaseModel):
    """Main configuration for feature engineering."""

    mouse_movement: MouseMovementProcessingConfig = Field(
        default_factory=MouseMovementProcessingConfig,
        description="Mouse movement processing configuration",
    )
    mouse_down_up: MouseDownUpConfig = Field(
        default_factory=MouseDownUpConfig,
        description="Mouse down/up processing configuration",
    )
    keyboard: KeyboardConfig = Field(
        default_factory=KeyboardConfig,
        description="Keyboard events processing configuration",
    )
    checkbox: CheckboxFeatureConfig = Field(
        default_factory=CheckboxFeatureConfig,
        description="Checkbox events processing configuration",
    )
    session: SessionConfig = Field(
        default_factory=SessionConfig,
        description="Session events processing configuration",
    )

    class Config:
        """ Pydantic configuration."""
        frozen = True
