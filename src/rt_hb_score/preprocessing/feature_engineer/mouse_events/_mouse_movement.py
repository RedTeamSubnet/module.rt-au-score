"""Mouse movement processor for extracting velocity features."""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
from dateutil.parser import parse

from .._base import BaseFeatureEngineer
from .config import MouseMovementProcessingConfig

logger = logging.getLogger(__name__)


class MouseMovementProcessor(BaseFeatureEngineer):
    """Processes mouse movement data to extract velocity features."""

    def __init__(self, config: Optional[MouseMovementProcessingConfig] = None):
        """Initialize the processor with configuration."""
        self.config = config or MouseMovementProcessingConfig()

    def __call__(
        self, mouse_movement_data: List[Dict], click_data: List[Dict]
    ) -> Dict[str, float]:
        """Process mouse movement data and compute velocity features."""
        try:

            velocities = self._compute_velocity(mouse_movement_data)
            velocity_std = np.std(velocities) if velocities else 0
            velocity_avg = np.average(velocities) if velocities else 0
            px_ms = self.detect_bot_movements(mouse_movement_data, click_data)
            mouse_angle_std = self._get_angle_std(mouse_movement_data)
            mouse_movement_count = len(mouse_movement_data)

            return {
                self.config.velocity_std: velocity_std,
                self.config.velocity_avg: velocity_avg,
                self.config.pixel_per_movement: px_ms,
                self.config.movement_cont: mouse_movement_count,
                self.config.mouse_angle_std: mouse_angle_std,
            }
        except Exception as e:
            logger.error(
                f"Error computing mouse movement features: \n\n{self.config.velocity_std.upper()}: 0 {str(e)}\n\n"
            )
            return {
                self.config.velocity_std: 0,
                self.config.velocity_avg: 0,
                self.config.pixel_per_movement: 0,
                self.config.movement_cont: 0,
            }

    def _parse_timestamp(self, timestamp_str: str) -> float:
        """Parse timestamp string to float."""
        try:
            if isinstance(timestamp_str, (int, float)):
                return float(timestamp_str)
            return parse(timestamp_str).timestamp()
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing timestamp : {str(e)}")
            return np.nan

    def _get_angle_std(self, mouse_movements: List[Dict]) -> float:
        """Calculate the standard deviation of the angles between consecutive points."""
        if not mouse_movements:
            logger.warning(
                "Empty mouse movement data to compute angle standard deviation"
            )
            return 0
        try:
            valid_movements = [m for m in mouse_movements if m is not None]
            if len(valid_movements) < self.config.min_movements_required:
                return 0
            valid_movements = sorted(
                valid_movements, key=lambda x: parse(x["timestamp"])
            )

            x_coords = np.array(
                [m.get(self.config.fields["x"]) for m in valid_movements]
            )
            y_coords = np.array(
                [m.get(self.config.fields["y"]) for m in valid_movements]
            )

            angles = np.arctan2(y_coords, x_coords) * 180 / np.pi

            return np.nanstd(angles)
        except Exception as e:
            logger.error(f"Error in angle standard deviation computation: {str(e)}")
            return 0

    def _compute_velocity(self, mouse_movements: List[Dict]) -> List[float]:
        """Compute velocities from mouse movement data."""
        # self.x_vel(mouse_movements)
        if not mouse_movements:
            logger.warning("Empty mouse movement data to compute velocity")
            return None

        try:
            valid_movements = [m for m in mouse_movements if m is not None]

            if len(valid_movements) < self.config.min_movements_required:
                return None
            valid_movements = sorted(
                valid_movements, key=lambda x: parse(x["timestamp"])
            )

            x_coords = np.array(
                [m.get(self.config.fields["x"]) for m in valid_movements]
            )
            y_coords = np.array(
                [m.get(self.config.fields["y"]) for m in valid_movements]
            )
            timestamps = np.array(
                [
                    self._parse_timestamp(m.get(self.config.fields["timestamp"]))
                    for m in valid_movements
                ]
            )

            if (
                np.isnan(x_coords).any()
                or np.isnan(y_coords).any()
                or np.isnan(timestamps).any()
            ):
                logger.warning("Invalid values found in movement data")
                return None

            dx = np.diff(x_coords)
            dy = np.diff(y_coords)
            dt = np.diff(timestamps)

            distances = np.sqrt(dx**2 + dy**2)

            # Get count of zero distances
            velocities = np.divide(
                distances, dt, out=np.zeros_like(distances), where=dt != 0
            )

            return velocities.tolist()

        except Exception as e:
            logger.error(f"Error in velocity computation: {str(e)}")
            return []

    def load_mouse_data(self, mouse_movements: List[Dict]) -> List[Dict]:

        mouse_movements.sort(
            key=lambda point: parse(point.get(self.config.fields["timestamp"]))
        )
        return mouse_movements

    def calculate_traveled_distance(
        self, mouse_movements: List[Dict]
    ) -> Tuple[float, bool]:
        valid_movements = [m for m in mouse_movements if m is not None]
        x_coords = np.array([m.get(self.config.fields["x"]) for m in valid_movements])
        y_coords = np.array([m.get(self.config.fields["y"]) for m in valid_movements])

        distances = np.sqrt(np.diff(x_coords) ** 2 + np.diff(y_coords) ** 2)

        total_distance = np.sum(distances)
        is_static = all(d == 0 for d in distances)
        return total_distance, is_static

    # def calculate_sampling_rate(
    #     self, mouse_movements: List[Dict], clicks_length
    # ) -> float:
    #     """Compute the average sampling rate (time difference between consecutive points)"""
    #     time_diffs = []
    #     for i in range(1, len(mouse_movements)):
    #         t1 = datetime.fromisoformat(
    #             mouse_movements[i - 1][
    #                 self.config.fields["timestamp"]
    #             ].replace("Z", "")
    #         )
    #         t2 = datetime.fromisoformat(
    #             mouse_movements[i][self.config.fields["timestamp"]].replace(
    #                 "Z", ""
    #             )
    #         )
    #         time_diffs.append((t2 - t1).total_seconds())

    #     time_diffs = sorted(time_diffs, reverse=True)[clicks_length:]
    #     avg_sampling_rate = np.mean(time_diffs) if time_diffs else 0
    #     return avg_sampling_rate

    def detect_bot_movements(
        self, mouse_movements: List[Dict], click_data: List[Dict]
    ) -> float:
        """Identify bot-like behavior based on movement density"""
        if (
            mouse_movements is None
            or len(mouse_movements) == 0
            or len(click_data) >= len(mouse_movements)
        ):
            logger.warning(
                "No mouse movements or exactly bot-like behavior. Not enough movements or ..."
            )
            return 0
        mouse_movements = self.load_mouse_data(mouse_movements)

        total_distance, is_static = self.calculate_traveled_distance(mouse_movements)
        # avg_sampling_rate = self.calculate_sampling_rate(
        #     mouse_movements, len(click_data)
        # )
        movement_count = len(mouse_movements)
        distance_per_count = (
            total_distance / movement_count
            if movement_count or is_static or total_distance == 0
            else 0
        )

        return distance_per_count
