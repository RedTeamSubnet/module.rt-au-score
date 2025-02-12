"""Configuration for checkbox path analysis."""

from pydantic import BaseModel, Field


class CheckboxSequenceConfig(BaseModel):
    input_field: str = Field(default="mouse_clicks")
    input_main: str = Field(default="between_path")
    input_validation: str = Field(default="is_valid")
    input_angle_std: str = Field(default="angle_std")
    input_angular_consistency: str = Field(default="angular_consistency")
    input_straightness: str = Field(default="straightness")
    output_field: str = Field(default="checkbox_path_score")

    min_angular_consistency: float = Field(default=0.84455)
    max_angular_consistency: float = Field(default=0.9781)

    min_angle_std: float = Field(default=0.1)
    max_angle_std: float = Field(default=16.8335)

    min_straightness: float = Field(default=0.6048)
    max_straightness: float = Field(default=0.99086)

    bot_straightness: float = Field(
        default=1.0,
        description="If straightness is 1.0, it is 100 percent bot",
    )

    bot_angle_std: float = Field(
        default=0,
        description="If angle std is 1.0, it is 100 percent bot",
    )
    bot_angular_consistency: float = Field(
        default=1,
        description="If angle std is 1.0, it is 100 percent bot",
    )

    weight_angle_std: float = Field(default=0.4)
    weight_angular_consistency: float = Field(default=0.4)
    weight_straightness: float = Field(default=0.2)


class SessionTimeConfig(BaseModel):
    session_time: str = Field(default="session_time")

    min_session_time: float = Field(default=8)

    max_session_time: float = Field(default=15)


class CheckboxPathConfig(BaseModel):
    checkbox_sequence: CheckboxSequenceConfig = Field(default=CheckboxSequenceConfig())
    session_time: SessionTimeConfig = Field(default=SessionTimeConfig())

    weight: float = Field(
        default=1.5,
        description="Weight for checkbox path analysis",
    )
