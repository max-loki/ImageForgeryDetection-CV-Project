import cv2
import numpy as np
from modules.preprocessing import preprocess
from modules.detector import confidence_score


def test_preprocess_shape():
    image = np.zeros((100, 120, 3), dtype=np.uint8)
    gray, processed = preprocess(image)
    assert gray.shape == (100, 120)
    assert processed.shape == (100, 120)


def test_confidence_score_zero():
    assert confidence_score(0, 0, 0) == 0.0


def test_confidence_score_range():
    score = confidence_score(100, 50, 2)
    assert 0 <= score <= 100
