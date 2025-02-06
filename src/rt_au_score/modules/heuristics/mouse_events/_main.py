"""Mouse event analysis module."""

import logging
from typing import Dict, Any, Optional

from .config import MouseEventConfig
from .velocity import VelocityAnalyzer
from .movement_count import MovementCountAnalyzer
from .checkbox_path import CheckboxPathAnalyzer
from .compare import ArgCompare

logger = logging.getLogger(__name__)


class MouseEventAnalyzer:
    """Analyzes mouse events for bot-like behavior."""

    def __init__(self, config: Optional[MouseEventConfig] = None):
        """Initialize mouse event analyzers."""
        self.config = config or MouseEventConfig()

        self.velocity_analyzer = VelocityAnalyzer(config=self.config.velocity)
        self.movement_count_analyzer = MovementCountAnalyzer(
            config=self.config.movement_count
        )
        self.checkbox_path_analyzer = CheckboxPathAnalyzer(
            config=self.config.checkbox_path
        )
        self.args_comparer = ArgCompare(config=self.config.args_comparer)

    def __call__(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mouse features for bot detection."""
        try:
            arg_score = self.args_comparer(features)
            if arg_score == 0:
                logger.info("Bot did not complied")
                return {
                    "bot_behavior": {"score": 1.0, "weight": 1.0},
                }
            velocity_score: dict = self.velocity_analyzer(features)
            movement_count_score: dict = self.movement_count_analyzer(features)
            checkbox_path_score: dict = self.checkbox_path_analyzer(features)

            checkbox_getter = features.get("checkbox")
            mouse_down_getter = features.get(self.config.mouse_down_check, 1)

            if checkbox_getter is None:
                return {
                    "bot_behavior": {"score": 1.0, "weight": 1.0},
                }
            return {
                self.config.velocity_std: {
                    "score": velocity_score.get(self.config.velocity_std, 1.0),
                    "weight": self.config.velocity_std_weight,
                },
                self.config.velocity_avg: {
                    "score": velocity_score.get(self.config.velocity_avg, 1.0),
                    "weight": self.config.velocity_avg_weight,
                },
                self.config.distance_count: {
                    "score": movement_count_score.get(self.config.distance_count, 1.0),
                    "weight": self.config.distance_weight,
                },
                self.config.mouse_movement_count: {
                    "score": movement_count_score.get(
                        self.config.mouse_movement_count, 1.0
                    ),
                    "weight": self.config.movement_count_weight,
                },
                # self.config.session_time: {
                #     "score": checkbox_path_score.get(self.config.session_time, 1.0),
                #     "weight": self.config.session_time_weight,
                # },
                self.config.checkbox_path_score: {
                    "score": checkbox_path_score.get(
                        self.config.checkbox_path_score, 1.0
                    ),
                    "weight": self.config.checkbox_path_weight,
                },
                self.config.mouse_down_check: {
                    "score": mouse_down_getter,
                    "weight": self.config.mouse_down_weight,
                },
            }

        except Exception as e:
            logger.error(f"Error in mouse event analysis: {str(e)}")
            return {
                "error_score": {"score": 1.0, "weight": 1.0},
            }
