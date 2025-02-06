"""Checkbox path analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .config import CheckboxPathConfig
from .._base import BaseHeuristicCheck
from .checkbox_sequence import CheckboxPathSequence
from .session_time import SessionTimeAnalyze

logger = logging.getLogger(__name__)


class CheckboxPathAnalyzer(BaseHeuristicCheck):
    """Analyzes checkbox interaction patterns for bot detection."""

    def __init__(self, config: Optional[CheckboxPathConfig] = None):
        """Initialize checkbox path analyzer."""
        self.config = config or CheckboxPathConfig()
        self.checkbox_sequence = CheckboxPathSequence(
            config=self.config.checkbox_sequence
        )
        self.session_time = SessionTimeAnalyze(config=self.config.session_time)

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze checkbox interaction features for bot detection.

        Args:
            features: Dictionary containing checkbox interaction features

        Returns:
            Score indicating likelihood of bot behavior (0-1, higher = more bot-like)
        """
        try:
            sequence_score = self.checkbox_sequence(features)
            session_time_score = self.session_time(features)
            return {
                self.config.checkbox_sequence.output_field: sequence_score,
                self.config.session_time.session_time: session_time_score
            }
        except Exception as e:
            logger.error(f"Error in checkbox path analysis: {str(e)}", exc_info=True)
            return {
                self.config.checkbox_sequence.output_field: 1,
                self.config.session_time.session_time: 1
            }
