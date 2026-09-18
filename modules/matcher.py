import cv2
import numpy as np


def self_match(descriptors: np.ndarray, ratio: float = 0.75, min_spatial_distance: float = 20.0):
    """Find similar descriptors within the same image while avoiding trivial self-matches."""
    if descriptors is None or len(descriptors) < 2:
        return []

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    raw = matcher.knnMatch(descriptors, descriptors, k=2)
    good = []

    # Spatial filtering is applied later because descriptor matching does not know coordinates.
    for pair in raw:
        if len(pair) < 2:
            continue
        m, n = pair
        if m.queryIdx == m.trainIdx:
            continue
        if m.distance < ratio * n.distance:
            good.append(m)

    return good
