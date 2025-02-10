"""session event feature engineering."""

import logging
from typing import Dict, List, Optional
from dateutil.parser import parse


from .._base import BaseFeatureEngineer
from .config import SessionConfig

logger = logging.getLogger(__name__)


class SessionProcessor(BaseFeatureEngineer):
    """Processes session interactions to extract features."""

    def __init__(self, config: Optional[SessionConfig] = None):
        """Initialize the processor."""
        self.config = config or SessionConfig()

    def __call__(self, data: Dict[str, List[Dict]]) -> Dict[str, float]:
        """Process session events and extract features.

        Args:
            data: Dictionary containing mouse movement data

        Returns:
            Dictionary containing extracted features
        """
        try:
            mouse_events = data.get(self.config.input_field, [])

            if not mouse_events:
                return {
                    self.config.output_filed: 0
                }  # Return 0 if no session events are found

            sorted_mouse_events = sorted(
                mouse_events, key=lambda x: parse(x["timestamp"])
            )
            session_time = (
                parse(sorted_mouse_events[-1]["timestamp"])
                - parse(sorted_mouse_events[0]["timestamp"])
            ).total_seconds()
            return {self.config.output_filed: session_time}
        except Exception as e:
            logger.warning(
                f"Error processing session events:{self.config.output_filed.upper()} 0 Error message: {str(e)}"
            )
            return {self.config.output_filed: 0}
