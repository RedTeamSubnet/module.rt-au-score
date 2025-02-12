from pydantic import BaseModel, Field


class ArgCompareConfig(BaseModel):
    type: str = Field(default="click", description="Type of event")
    argument_key: str = Field(default="args", description="Key for arguments")
    metrics: dict[str, dict] = Field(
        default={"location": {"x": "x", "y": "y"}}, description="Metrics for location"
    )
    tolerance: float = Field(default=15, description="Tolerance for location matching")
    mouse_clicks: str = Field(
        default="mouse_clicks", description="Key for mouse clicks"
    )
    actions: list[dict] = Field(
        default=[
            {"id": "1", "type": "click", "args": {"location": {"x": 100, "y": 200}}},
        ],
        description="List of actions to be performed in the pipeline",
    )
