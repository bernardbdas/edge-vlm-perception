"""GStreamer Hardware-Accelerated Video Pipeline."""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np

logger = logging.getLogger("edge.video")


class VideoCapturePipeline:
    """Manages OpenCV VideoCapture with Jetson nvarguscamerasrc support."""

    def __init__(self, gstreamer_pipeline_str: Optional[str] = None):
        self.pipeline_str = gstreamer_pipeline_str
        self._cap = None
        self._init_capture()

    def _init_capture(self) -> None:
        try:
            import cv2

            if self.pipeline_str:
                self._cap = cv2.VideoCapture(self.pipeline_str, cv2.CAP_GSTREAMER)
            else:
                self._cap = cv2.VideoCapture(0)
            if not self._cap or not self._cap.isOpened():
                self._cap = None
        except Exception as e:
            logger.warning("Live camera unavailable (%s). Using synthetic frame generator.", e)
            self._cap = None

    def read_frame(self) -> np.ndarray:
        """Reads next frame; generates a synthetic colored frame if camera is absent."""
        if self._cap and self._cap.isOpened():
            ret, frame = self._cap.read()
            if ret and frame is not None:
                return frame

        # Synthetic 640x480 frame for testing
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add gradient pattern
        frame[:, :, 0] = np.linspace(0, 255, 640, dtype=np.uint8)
        frame[:, :, 1] = 120
        frame[:, :, 2] = 200
        return frame

    def release(self) -> None:
        if self._cap:
            self._cap.release()
