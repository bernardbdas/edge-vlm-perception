import numpy as np
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.quantization.tensorrt_engine import TensorRTRunner


@pytest.fixture
def client():
    return TestClient(app)


def test_tensorrt_runner_infer():
    runner = TensorRTRunner()
    dummy_img = np.zeros((300, 300, 3), dtype=np.uint8)
    tokens = [1, 2, 3]

    res = runner.infer(dummy_img, tokens)
    assert "boxes" in res
    assert "latency_ms" in res
    assert res["latency_ms"] > 0


def test_api_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_api_detect(client):
    res = client.post("/api/v1/detect", json={"prompt": "locate yellow helmet"})
    assert res.status_code == 200
    data = res.json()
    assert data["prompt"] == "locate yellow helmet"
    assert len(data["detections"]) > 0
