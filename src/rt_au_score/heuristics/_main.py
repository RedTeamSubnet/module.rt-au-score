"""Main module for heuristic analysis."""
import logging
from typing import Dict, Any, Optional

from .config import HeuristicConfig
from .mouse_events import MouseEventAnalyzer


logger = logging.getLogger(__name__)


class HeuristicAnalyzer:
    """Main class for analyzing features using heuristics."""

    def __init__(self, config: Optional[HeuristicConfig] = None):
        """Initialize analyzers with configuration.

        Args:
            config: Configuration for heuristic analysis
        """
        self.config = config or HeuristicConfig()
        self.mouse_analyzer = MouseEventAnalyzer(config=self.config.mouse_events)

    def __call__(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze features to detect bot-like behavior.

        Args:
            features: Dictionary of engineered features

        Returns:
            Dictionary containing detection results and scores
        """
        try:
            mouse_scores = self.mouse_analyzer(features)
            final_score = round(1 - self._calculate_final_score(mouse_scores), 5)
            return {
                "score": final_score,
            }

        except Exception as e:
            logger.error(f"Error in heuristic analysis: {str(e)}", exc_info=True)
            return {
                "score": 0.0,
                "error": str(e),
            }

    def _calculate_final_score(self, scores: Dict[str, Dict[str, float]]) -> float:
        """Calculate weighted average score.

        Args:
            scores: Dictionary containing scores and weights

        Returns:
            Final weighted score
        """

        total_weight = 0
        weighted_sum = 0
        for keys, analyzer_scores in scores.items():
            score = analyzer_scores.get("score", 0)
            weight = analyzer_scores.get("weight", 0)
            if score == 0:
                weight = 0.5
            weighted_sum += score * weight
            total_weight += weight
            logger.debug(f"{keys}: {score} (weight: {weight})")
        if total_weight == 0:
            return 0.0

        logger.debug(f"Final botness score: {weighted_sum / total_weight}.\nMetrics:")

        return weighted_sum / total_weight
