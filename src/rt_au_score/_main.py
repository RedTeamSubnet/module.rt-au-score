import logging
from typing_extensions import Dict, Any, Union

from .config import MetricsProcessorConfig
from .modules.preprocessing import Preprocessor
from .modules.heuristics import HeuristicAnalyzer

logger = logging.getLogger(__name__)




class MetricsProcessor:
    def __init__(self, config: Union[MetricsProcessorConfig,Dict[str,Any],None] = None):
        if isinstance(config, dict):
            config = MetricsProcessorConfig(**config)

        self.config = config or MetricsProcessorConfig()

        self.preprocessor = Preprocessor(config=self.config.preprocessor)
        self.heuristic_analyzer = HeuristicAnalyzer(config=self.config.heuristics)

    def __call__(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Step 1: Preprocess the data
            logger.info("Preprocessing raw data...")
            processed_features = self.preprocessor(raw_data)

            logger.info("Preprocessing raw data...")

            if processed_features is None:
                logger.error("Preprocessing failed")
                return {
                    "success": False,
                    "error": "Preprocessing failed",
                    "stage": "preprocessing",
                }

            # Step 2: Run heuristic analysis
            logger.info("Running heuristic analysis...")
            analysis_results = self.heuristic_analyzer(processed_features)

            return {
                "success": True,
                "project_id": processed_features["project_id"],
                "user_id": processed_features["user_id"],
                "analysis": analysis_results,
            }

        except Exception as e:
            logger.error(f"Error in metrics processing: {str(e)}", exc_info=True)
            raise


