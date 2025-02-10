"""Feature engineering module for processing mouse and keyboard events."""

import logging
from typing import Dict, List, Any, Optional

from .mouse_events import MouseMovementProcessor
from .mouse_events import MouseDownUpProcessor
from .keyboard_events import KeyboardEventsProcessor
from .checkboxes import CheckboxEventProcessor, SessionProcessor
from .config import FeatureEngineerConfig

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Coordinates the processing of all mouse and keyboard features."""

    def __init__(self, config: Optional[FeatureEngineerConfig] = None):
        """Initialize feature engineering processors.

        Args:
            config: Configuration for feature engineering. If None, uses defaults.
        """
        self.config = config or FeatureEngineerConfig()

        self.mouse_movement_processor = MouseMovementProcessor(
            config=self.config.mouse_movement
        )
        self.mouse_down_up_processor = MouseDownUpProcessor(
            config=self.config.mouse_down_up
        )
        # self.keyboard_processor = KeyboardEventsProcessor(config=self.config.keyboard)
        self.checkbox_processor = CheckboxEventProcessor(config=self.config.checkbox)
        self.session_processor = SessionProcessor(config=self.config.session)

    def __call__(self, data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Process input data and engineer features.

        Args:
            data: Dictionary containing mouse and keyboard event data

        Returns:
            Dictionary containing engineered features
        """
        try:
            mouse_movement_results = self.mouse_movement_processor(
                data.get(self.config.mouse_movement.input_field, []),
                data.get(self.config.mouse_movement.click_field, []),
            )
            # keyboard_data = {
            #     field_name: data.get(field_path, [])
            #     for field_name, field_path in self.config.keyboard.input_fields.items()
            # }
            # keyboard_results = self.keyboard_processor(keyboard_data)
            checkbox_results = self.checkbox_processor(data)
            mouse_down_up_results = self.mouse_down_up_processor(data)
            session_results = self.session_processor(data)
            return {
                **mouse_movement_results,
                **mouse_down_up_results,
                # **keyboard_results,
                **checkbox_results,
                **session_results,
                **{
                    f"{self.config.mouse_movement.click_field}": data.get(
                        self.config.mouse_movement.click_field, []
                    )
                },
            }

        except Exception as e:
            logger.error(f"Error processing features: {str(e)}", exc_info=True)
            return {}
