"""Open-Vocabulary Vision-Language Spatial Grounding Pipeline."""

from __future__ import annotations

import logging
from typing import Any, Dict

import numpy as np

from ..quantization.tensorrt_engine import TensorRTRunner

logger = logging.getLogger("edge.grounding")


class VLMGroundingPipeline:
    """Takes RGB image frames and natural language queries to predict localized bounding boxes."""

    def __init__(self, runner: TensorRTRunner):
        self.runner = runner

    def process_frame(self, frame: np.ndarray, prompt: str) -> Dict[str, Any]:
        """Runs open-vocabulary detection conditioned on the text prompt."""
        # Simulated tokenization of the prompt
        tokens = [ord(c) for c in prompt[:16]]

        # Run inference via TensorRT engine
        raw_result = self.runner.infer(frame, tokens)

        # Annotate detections with query label
        detections = []
        for box in raw_result["boxes"]:
            detections.append(
                {
                    "query": prompt,
                    "label": f"{prompt}: {box['label']}",
                    "confidence": box["confidence"],
                    "bbox_xyxy": box["bbox"],
                }
            )

        return {
            "prompt": prompt,
            "detections": detections,
            "latency_ms": raw_result["latency_ms"],
            "fps": raw_result["fps"],
        }
