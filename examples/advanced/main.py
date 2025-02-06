#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ast import arg
import sys
import json
import logging
from pathlib import Path

from rt_wc_score import MetricsProcessor

logger = logging.getLogger(__name__)

argument = {
    "sessionConfig": {
        "actions": [
            {
                "id": "1",
                "type": "click",
                "args": {
                    "location": {
                        "x": 25,
                        "y": 19,
                    }
                },
            },
            {
                "id": "2",
                "type": "input",
                "args": {
                    "value": "test@example.com",
                    "box": {"top": 190, "right": 400, "bottom": 210, "left": 80},
                },
                "css": {"selector": "input[type='text']"},
                "xpath": {"selector": "//input[@type='text']"},
            },
            {
                "id": "3",
                "type": "click",
                "args": {
                    "location": {
                        "x": 1867,
                        "y": 19,
                    }
                },
            },
        ]
    }
}
if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
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
    processor = MetricsProcessor()
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
