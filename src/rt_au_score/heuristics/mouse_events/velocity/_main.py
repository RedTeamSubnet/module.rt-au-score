"""Velocity analysis for mouse events."""

import logging

from typing import Dict, Any, Optional

from .._base import BaseHeuristicCheck
from .config import VelocityConfig


logger = logging.getLogger(__name__)


class VelocityAnalyzer(BaseHeuristicCheck):
    """Analyzes mouse velocity patterns for bot detection."""

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze velocity features for bot detection."""
        try:

            stddev_velocity = features.get(self.config.velocity_std, 0.0)
            avg_velocity = features.get(self.config.velocity_avg, 0.0)

            stddev_score = round(
                self.scoring_function(
                    value=stddev_velocity,
                    min_value=self.config.min_velocity_variation,
                    max_value=self.config.max_velocity_variation,
                    min_score=0.6,
                    max_score=0.4,
                    min_of_min=0.3,
                    max_of_max=1.5,
                ),
                5,
            )
            avg_score = round(
                self.scoring_function(
                    value=avg_velocity,
                    min_value=self.config.min_velocity_avg,
                    max_value=self.config.max_velocity_avg,
                    min_score=0.6,
                    max_score=0.4,
                    min_of_min=0.3,
                    max_of_max=1.5,
                ),
                5,
            )
            return {
                self.config.velocity_std: stddev_score,
                self.config.velocity_avg: avg_score,
            }

        except Exception as e:
            logger.error(f"Error in  check velocity analysis: {str(e)}")
            return {
                self.config.velocity_std: 1,
                self.config.velocity_avg: 1,
            }

    def __init__(self, config: Optional[VelocityConfig] = None):
        """Initialize velocity analyzer."""
        self.config = config or VelocityConfig()
