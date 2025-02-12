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
            if features.get(self.config.input_validation):
                for feature in features[self.config.input_main]:
                    angle_std = feature.get(self.config.input_angle_std)
                    straightness = feature.get(self.config.input_straightness)
                    angular_consistency = feature.get(
                        self.config.input_angular_consistency
                    )
                    if (
                        straightness == self.config.bot_straightness
                        or angle_std == self.config.bot_angle_std
                        or angular_consistency == self.config.bot_angular_consistency
                    ):
                        max_suspicion_score == 1
                        continue

                    if all(
                        v is not None
                        for v in [angle_std, straightness, angular_consistency]
                    ):
                        angle_std_score = self._analyze_angle_std(angle_std)
                        straightness_score = self._analyze_straightness(straightness)
                        angular_consistency_score = self._analyze_angular_consistency(
                            angular_consistency
                        )

                        pair_score = (
                            (self.config.weight_angle_std * angle_std_score)
                            + (self.config.weight_straightness * straightness_score)
                            + (
                                self.config.weight_angular_consistency
                                * angular_consistency_score
                            )
                        )
                        max_suspicion_score = max(max_suspicion_score, pair_score)
                        pairs_analyzed += 1

                if pairs_analyzed == 0:
                    return 1.0

                return min(1.0, max_suspicion_score)
            else:
                return 1.0

        except Exception as e:
            logger.error(f"Error in check path analysis: {str(e)}")
            return 0.0

    def _analyze_angle_std(self, angle_consistency_value: float) -> float:
        score = self.scoring_function(
            value=angle_consistency_value,
            min_value=self.config.min_angle_std,
            max_value=self.config.max_angle_std,
            min_score=0.9,
            max_score=0.7,
            min_of_min=0.91,
            max_of_max=1.18,
        )

        return self.clamp_score_zero_to_one(score)

    def _analyze_straightness(self, straightness_value: float) -> float:
        score = self.scoring_function(
            value=straightness_value,
            min_value=self.config.min_straightness,
            max_value=self.config.max_straightness,
            min_score=0.6,
            max_score=0.9,
            min_of_min=0.8211,
            max_of_max=1.00922431,
        )

        return self.clamp_score_zero_to_one(score)

    def _analyze_angular_consistency(self, angular_consistency: float) -> float:
        score = self.scoring_function(
            value=angular_consistency,
            min_value=self.config.min_angular_consistency,
            max_value=self.config.max_angular_consistency,
            min_score=0.8,
            max_score=0.5,
            min_of_min=0.9472,
            max_of_max=1.02239035,
        )

        return self.clamp_score_zero_to_one(score)
