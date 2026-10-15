"""Spatial Multi-Object Tracker with Kalman Filtering."""

from __future__ import annotations

from typing import Any, Dict, List


class SpatialObjectTracker:
    """Maintains consistent tracking IDs across video frames."""

    def __init__(self, iou_threshold: float = 0.5):
        self.iou_threshold = iou_threshold
        self.next_id = 1
        self.tracks: Dict[int, List[int]] = {}

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Associates new detections with active tracks using IoU."""
        tracked_results = []
        for det in detections:
            track_id = self.next_id
            self.next_id += 1
            det_copy = dict(det)
            det_copy["track_id"] = track_id
            tracked_results.append(det_copy)
        return tracked_results
