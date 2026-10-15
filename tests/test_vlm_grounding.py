import numpy as np

from src.perception.spatial_tracker import SpatialObjectTracker
from src.perception.vlm_grounding import VLMGroundingPipeline
from src.quantization.tensorrt_engine import TensorRTRunner


def test_vlm_grounding_pipeline():
    runner = TensorRTRunner()
    pipeline = VLMGroundingPipeline(runner)

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    prompt = "find blue tool"

    result = pipeline.process_frame(frame, prompt)

    assert result["prompt"] == prompt
    assert len(result["detections"]) > 0
    assert "bbox_xyxy" in result["detections"][0]
    assert result["fps"] > 0


def test_spatial_tracker():
    tracker = SpatialObjectTracker()
    detections = [
        {"label": "box1", "confidence": 0.9, "bbox_xyxy": [10, 10, 50, 50]},
        {"label": "box2", "confidence": 0.85, "bbox_xyxy": [100, 100, 150, 150]},
    ]
    tracked = tracker.update(detections)
    assert len(tracked) == 2
    assert "track_id" in tracked[0]
    assert "track_id" in tracked[1]
    assert tracked[0]["track_id"] != tracked[1]["track_id"]
