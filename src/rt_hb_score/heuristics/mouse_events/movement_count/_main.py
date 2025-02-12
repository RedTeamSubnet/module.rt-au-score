"""Movement count analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .._base import BaseHeuristicCheck

from .config import MovementCountConfig

logger = logging.getLogger(__name__)


class MovementCountAnalyzer(BaseHeuristicCheck):
    """Analyzes mouse movement count for bot detection."""

    def __init__(self, config: Optional[MovementCountConfig] = None):
        """Initialize movement count analyzer."""
        self.config = config or MovementCountConfig()

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze movement count for bot detection."""
        try:

            pixel_count = features.get(self.config.pixel_per_movement, 0)
            movement_count = features.get(self.config.mouse_movement_count, 0)
            mouse_angle_std = features.get(self.config.mouse_angle_std, 0)
            if (
                pixel_count < self.config.min_pixel_count_too_low
                or movement_count < self.config.min_movement_count_too_low
                or mouse_angle_std < self.config.min_total_angle_std_too_low
            ):
                return {
                    self.config.pixel_per_movement: 1,
                    self.config.mouse_movement_count: 1,
                    self.config.mouse_angle_std: 1,
                }
            score_pixel = self.scoring_function(
                value=pixel_count,
                min_value=self.config.min_pixel_count,
                max_value=self.config.max_pixel_count,
                min_score=0.7,
                max_score=0.7,
                min_of_min=0.74,
                max_of_max=1.0674,
            )
            score_movement = self.scoring_function(
                value=movement_count,
                min_value=self.config.min_movement_count,
                max_value=self.config.max_movement_count,
                min_score=0.6,
                max_score=0.9,
                min_of_min=0.8,
                max_of_max=1.06,
            )
            score_angle_std = self.scoring_function(
                value=mouse_angle_std,
                min_value=self.config.min_total_angle_std,
                max_value=self.config.max_total_angle_std,
                min_score=0.6,
                max_score=0.9,
                min_of_min=0.856,
                max_of_max=1.063,
            )

            return {
                self.config.pixel_per_movement: score_pixel,
                self.config.mouse_movement_count: score_movement,
                self.config.mouse_angle_std: score_angle_std,
            }
        except Exception as e:
            logger.error(f"Error in check movement count analysis: {str(e)}")
            return {
                self.config.pixel_per_movement: 1,
                self.config.mouse_movement_count: 1,
            }
