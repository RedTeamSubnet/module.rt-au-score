"""Mouse down/up processor for extracting timing features."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from dateutil.parser import parse
import bisect
from .._base import BaseFeatureEngineer
from .config import MouseDownUpConfig

logger = logging.getLogger(__name__)


class MouseDownUpProcessor(BaseFeatureEngineer):
    def __init__(self, config: Optional[MouseDownUpConfig] = None):

        self.config = config or MouseDownUpConfig()

    def __call__(self, mouse_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        try:
            mouse_downs = mouse_data.get(self.config.down_field, [])
            mouse_movement_ = mouse_data.get(self.config.mouse_movements, [])
            sorted_mouse_downs = sorted(
                mouse_downs,
                key=lambda x: datetime.fromisoformat(x["timestamp"].rstrip("Z")),
            )
            sorted_mouse_movements = sorted(
                mouse_movement_,
                key=lambda x: datetime.fromisoformat(x["timestamp"].rstrip("Z")),
            )
            mouse_down_timestamps = [
                datetime.fromisoformat(x["timestamp"].rstrip("Z"))
                for x in sorted_mouse_downs
            ]
            mouse_movement_timestamps = [
                datetime.fromisoformat(x["timestamp"].rstrip("Z"))
                for x in sorted_mouse_movements
            ]
            results = self.find_first_gte_multiple(
                sorted_mouse_downs,
                mouse_down_timestamps,
                sorted_mouse_movements,
                mouse_movement_timestamps,
            )
            logger.debug(
                f"Mouse down/up analysis finished: \n\n{self.config.output_field.upper()}: {results}\n\n"
            )
            if results > 0:
                results = 1
            return {self.config.output_field: results}

        except Exception as e:
            logger.error(
                f"Error processing mouse down/up events \n{self.config.output_field.upper()} NaN: {str(e)}"
            )
            return {self.config.output_field: 1}

    def is_within_range(self, mouse_down, mouse_event, tolerance=2):
        return (
            mouse_down["x"] - tolerance
            <= mouse_event["x"]
            <= mouse_down["x"] + tolerance
            and mouse_down["y"] - tolerance
            <= mouse_event["y"]
            <= mouse_down["y"] + tolerance
        )

    def find_first_gte_multiple(self, query_data, query_timestamps, data, timestamps):
        results = 0

        for index, query in enumerate(query_timestamps):
            target_time = query
            idx = bisect.bisect_left(timestamps, target_time)

            mouse_event = data[idx - 1]
            mouse_down = query_data[index]
            if not self.is_within_range(
                mouse_down, mouse_event, self.config.within_tolerance
            ):
                results += 1

        return results / len(query_data)
