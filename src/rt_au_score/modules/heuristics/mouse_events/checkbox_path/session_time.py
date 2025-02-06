"""Checkbox path analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .config import SessionTimeConfig
from .._base import BaseHeuristicCheck

logger = logging.getLogger(__name__)


class SessionTimeAnalyze(BaseHeuristicCheck):

    def __init__(self, config: Optional[SessionTimeConfig] = None):

        self.config = config or SessionTimeConfig()

    def __call__(self, features: Dict[str, Any]) -> float:
        try:
            session_key = self.config.session_time
            session_time = features.get(session_key)
            score = self.scoring_function(
                value=session_time,
                min_value=self.config.min_session_time,
                max_value=self.config.max_session_time,
                min_score=0.8,
                max_score=0.5,
                min_of_min=0.65,  # min_linearity_threshold(0.75) * 0.6  = 0.45
                max_of_max=1.04,  # max_linearity_threshold(0.95) * 1.04 = 0.988
            )
            return score
        except Exception as e:
            logger.error(f"Error in checkbox path analysis: {str(e)}", exc_info=True)
            return 1.0
