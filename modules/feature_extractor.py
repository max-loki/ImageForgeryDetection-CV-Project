import cv2
import numpy as np


def extract_sift(image_gray: np.ndarray, max_features: int = 2500):
    """Extract SIFT keypoints and descriptors."""
    sift = cv2.SIFT_create(nfeatures=max_features)
    keypoints, descriptors = sift.detectAndCompute(image_gray, None)
    return keypoints, descriptors


def draw_keypoints(image: np.ndarray, keypoints):
    return cv2.drawKeypoints(
        image,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )
