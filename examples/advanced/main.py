#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging
from pathlib import Path

from rt_hb_score import MetricsProcessor

logger = logging.getLogger(__name__)

argument = {
    "actions": [
        {"args": {"location": {"x": 1281, "y": 176}}, "id": 0, "type": "click"},
        {"args": {"location": {"x": 1167, "y": 271}}, "id": 1, "type": "click"},
        {"args": {"location": {"x": 825, "y": 220}}, "id": 2, "type": "click"},
        {"args": {"location": {"x": 294, "y": 222}}, "id": 3, "type": "click"},
        {"args": {"location": {"x": 59, "y": 354}}, "id": 4, "type": "click"},
    ]
}
if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    _data_dir_path = Path(__file__).parent.parent.parent / "data"
    _raw_json_data_path = _data_dir_path / "raw" / "raw.json"
    _processed_json_data_path = _data_dir_path / "processed" / "processed.json"

    _raw_json_data_path.parent.mkdir(parents=True, exist_ok=True)
    _processed_json_data_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Reading data from: {_raw_json_data_path}")
    try:
        with open(_raw_json_data_path, "r") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in input file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error(f"Input file not found: {_raw_json_data_path}")
        sys.exit(1)

    logger.info("Processing metrics data...")
    processor = MetricsProcessor(config=argument)
    results = processor(raw_data)

    if not results["success"]:
        logger.error(f"Processing failed at {results['stage']}: {results['error']}")
        sys.exit(1)

    logger.info(f"Writing results to: {_processed_json_data_path}")
    with open(_processed_json_data_path, "w") as f:
        json.dump(results, f, indent=2)

    # Log summary of results
    analysis = results["analysis"]
    logger.info("Analysis Results:")
    logger.info(f"Score: {analysis['score']}")

    logger.info("Done!")
