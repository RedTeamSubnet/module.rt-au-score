"""Configuration for checkbox path analysis."""

from pydantic import BaseModel, Field


class CheckboxSequenceConfig(BaseModel):
    input_field: str = Field(default="mouse_clicks")
    input_main: str = Field(default="between_path")
    input_validation: str = Field(default="is_valid")
    input_avg_angle_degrees: str = Field(default="avg_angle_degrees")
    input_angle_consistency: str = Field(default="angle_consistency")
    input_straightness: str = Field(default="straightness")

    output_field: str = Field(default="checkbox_path_score")

    min_avg_angle_degrees: float = Field(
        default=0.025, description="Min average angle between movements"
    )
    max_avg_angle_degrees: float = Field(
        default=0.12, description="Max average angle between movements"
    )

    min_angle_consistency: float = Field(
        default=0.88, description="Threshold for suspiciously linear paths"
    )
    max_angle_consistency: float = Field(
        default=0.98, description="Threshold for suspiciously linear paths"
    )

    min_straightness: float = Field(
        default=0.80, description="Threshold for suspiciously linear paths"
    )
    max_straightness: float = Field(
        default=0.99, description="Threshold for suspiciously linear paths"
    )

    bot_straightness: float = Field(
        default=1.0,
        description="If straightness is 1.0, it is 100 percent bot",
    )
    bot_angle_consistency: float = Field(
        default=1.0,
        description="If angle consistency is 1.0, it is 100 percent bot",
    )
    bot_avg_angle: float = Field(
        default=0.0,
        description="If average angle is 0.0, it is 100 percent bot",
    )

    weight_angle_consistency: float = Field(default=0.4)
    weight_straightness: float = Field(default=0.3)
    weight_avg_angle: float = Field(default=0.3)


class SessionTimeConfig(BaseModel):
    session_time: str = Field(default="session_time")

    min_session_time: float = Field(
        default=8, description="Threshold for suspiciously linear paths"
    )

    max_session_time: float = Field(
        default=15, description="Threshold for suspiciously linear paths"
    )


class CheckboxPathConfig(BaseModel):
    checkbox_sequence: CheckboxSequenceConfig = Field(default=CheckboxSequenceConfig())
    session_time: SessionTimeConfig = Field(default=SessionTimeConfig())

    weight: float = Field(
        default=1.5,
        description="Weight for checkbox path analysis",
    )
