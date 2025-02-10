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
            if (
                pixel_count < self.config.min_pixel_count_too_low
                or movement_count < self.config.min_movement_count_too_low
            ):
                return {
                self.config.pixel_per_movement: 1,
                self.config.mouse_movement_count: 1,
            }
            score_pixel = self.scoring_function(
                value=pixel_count,
                min_value=self.config.min_pixel_count,
                max_value=self.config.max_pixel_count,
                min_score=0.6,
                max_score=0.65,
                min_of_min=0.2,
                max_of_max=1.5,
            )
            score_movement = self.scoring_function(
                value=movement_count,
                min_value=self.config.min_movement_count,
                max_value=self.config.max_movement_count,
                min_score=0.6,
                max_score=0.65,
                min_of_min=0.2,
                max_of_max=1.5,
            )

            return {
                self.config.pixel_per_movement: score_pixel,
                self.config.mouse_movement_count: score_movement,
            }
        except Exception as e:
            logger.error(f"Error in check movement count analysis: {str(e)}")
            return {
                self.config.pixel_per_movement: 1,
                self.config.mouse_movement_count: 1,
            }
