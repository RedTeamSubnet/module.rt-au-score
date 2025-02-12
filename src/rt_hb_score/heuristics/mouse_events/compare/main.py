
from .config import ArgCompareConfig
from typing_extensions import Union, Dict, Any, IntVar
import logging
from dateutil.parser import parse

logger = logging.getLogger(__name__)


class ArgCompare:
    def __init__(self, config: Union[ArgCompareConfig, None]):
        self.config = config or ArgCompareConfig()

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self._check_clicks(data)

            return result
        except Exception as e:
            logger.error(f"Error in check mouse event compare: {str(e)}", exc_info=True)
            return 0

    def _check_clicks(self, data: Dict[str, Any]) -> int:
        user_clicks = data.get(self.config.mouse_clicks, [])

        sorted_user_clicks = sorted(user_clicks, key=lambda x: parse(x["timestamp"]))
        clicks = [
            location["args"]["location"]
            for location in self.config.actions
            if location.get("type") == self.config.type
        ]
        within_clicks = []
        for click in clicks:
            matched_click = next(
                (
                    user_click
                    for user_click in sorted_user_clicks
                    if self._is_within(user_click, click, self.config.tolerance)
                ),
                None,
            )
            if matched_click:
                within_clicks.append(matched_click)
        if len(within_clicks) != len(clicks):
            return 0

        number_clicks = len(clicks)
        for index, user_click in enumerate(within_clicks):
            if not self._is_within(user_click, clicks[index], self.config.tolerance):
                number_clicks -= 1
                logger.warning(f"Click {index} was clicked but in wrong order")
                return 0    
            else:
                logger.debug(f"Click {index} matched with given coordinates")

        if number_clicks:
            return 1

    def _is_within(
        self, user_click: Dict[str, Any], click: Dict[str, Any], tolerance: IntVar = 2
    ) -> bool:
        truth_value = (
            abs(user_click["x"] - click["x"]) <= tolerance
            and abs(user_click["y"] - click["y"]) <= tolerance
        )
        return truth_value
