"""Checkbox path analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .config import CheckboxSequenceConfig
from .._base import BaseHeuristicCheck

logger = logging.getLogger(__name__)


class CheckboxPathSequence(BaseHeuristicCheck):
    def __init__(self, config: Optional[CheckboxSequenceConfig] = None):
        self.config = config or CheckboxSequenceConfig()

    def __call__(self, features: Dict[str, Any]) -> float:
        try:
            max_suspicion_score = 0.0
            pairs_analyzed = 0
            if features.get("is_valid"):
                for feature in features["checkbox"]:
                    avg_angle_degrees = feature.get(self.config.avg_angle_degrees)
                    angle_consistency = feature.get(self.config.angle_consistency)
                    straightness = feature.get(self.config.straightness)
                    if (
                        straightness == self.config.bot_straightness
                        or angle_consistency == self.config.bot_angle_consistency
                        or avg_angle_degrees == self.config.bot_avg_angle
                    ):
                        max_suspicion_score == 1
                        continue

                    if all(
                        v is not None
                        for v in [angle_consistency, straightness, avg_angle_degrees]
                    ):
                        angle_consistency_score = self._analyze_angle_consistency(
                            angle_consistency
                        )
                        straightness_score = self._analyze_straightness(straightness)
                        avg_angle_score = self._analyze_avg_angle(avg_angle_degrees)

                        pair_score = (
                            (
                                self.config.weight_angle_consistency
                                * angle_consistency_score
                            )
                            + (self.config.weight_straightness * straightness_score)
                            + (self.config.weight_avg_angle * avg_angle_score)
                        )

                        max_suspicion_score = max(max_suspicion_score, pair_score)

                if pairs_analyzed == 0:
                    return 1.0

                return min(1.0, max_suspicion_score)
            else:

                return 1.0

        except Exception as e:
            logger.error(f"Error in checkbox path analysis: {str(e)}")
            return 0.0

    def _analyze_angle_consistency(self, angle_consistency_value: float) -> float:
        score = self.scoring_function(
            value=angle_consistency_value,
            min_value=self.config.min_angle_consistency,
            max_value=self.config.max_angle_consistency,
            min_score=0.8,
            max_score=0.5,
            min_of_min=0.65,  # min_linearity_threshold(0.75) * 0.6  = 0.45
            max_of_max=1.04,  # max_linearity_threshold(0.95) * 1.04 = 0.988
        )

        return self.clamp_score_zero_to_one(score)

    def _analyze_straightness(self, straightness_value: float) -> float:
        score = self.scoring_function(
            value=straightness_value,
            min_value=self.config.min_straightness,
            max_value=self.config.max_straightness,
            min_score=0.8,
            max_score=0.5,
            min_of_min=0.6,
            max_of_max=1.03,
        )

        return self.clamp_score_zero_to_one(score)

    def _analyze_avg_angle(self, avf_angle_value: float) -> float:
        score = self.scoring_function(
            value=avf_angle_value,
            min_value=self.config.min_avg_angle_degrees,
            max_value=self.config.max_avg_angle_degrees,
            min_score=0.5,
            max_score=0.8,
            min_of_min=0.5,
            max_of_max=1.5,
        )
        return self.clamp_score_zero_to_one(score)
