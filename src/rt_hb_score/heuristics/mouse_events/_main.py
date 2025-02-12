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
                logger.warning("Bot did not clicked to all given locations")
                return {
                    "bot_behavior": {"score": 1.0, "weight": 1.0},
                }
            if features[self.config.mouse_movement_count] < self.config.mouse_movements_very_low:
                logger.warning("Bot did not move enough")
                return {
                    "bot_behavior": {"score": 1.0, "weight": 1.0},
                }
            logger.debug("Checking `Velocity` of bot")
            velocity_score: dict = self.velocity_analyzer(features)
            logger.debug("Checking `Movement Count` of bot")
            movement_count_score: dict = self.movement_count_analyzer(features)
            logger.debug("Checking `Clicks`' path of bot")
            checkbox_path_score: dict = self.checkbox_path_analyzer(features)
            logger.debug("Finished Checking")
            mouse_down_getter = features.get(self.config.mouse_down_check, 1)
            scores = {
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
                self.config.checkbox_path_score: {
                    "score": checkbox_path_score.get(
                        self.config.checkbox_path_score, 1.0
                    ),
                    "weight": self.config.checkbox_path_weight,
                },
                self.config.overall_session_angle_std: {
                    "score": movement_count_score.get(
                        self.config.overall_session_angle_std, 1.0
                    ),
                    "weight": self.config.overall_session_angle_std_weight,
                },
            }
            if mouse_down_getter > 0:
                logger.warning("Bot failed in single down check")
                scores[self.config.mouse_down_check] = {
                    "score": 1,  # if bot failed in single mouse down check then get 1 otherwise 0
                    "weight": 1.0,
                }
            return scores

        except Exception as e:
            logger.error(f"Error in checking mouse event analysis: {str(e)}")
            return {
                "error_score": {"score": 1.0, "weight": 1.0},
            }
