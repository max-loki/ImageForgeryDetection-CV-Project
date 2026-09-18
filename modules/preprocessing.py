import cv2
import numpy as np


def preprocess(image: np.ndarray, denoise: bool = True, equalize: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Return grayscale and analysis-ready image."""
    if image is None or image.size == 0:
        raise ValueError("Invalid or empty image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

    if denoise:
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

    if equalize:
        gray = cv2.equalizeHist(gray)

    return gray, gray.copy()
