import cv2
import numpy as np


def verify_matches(keypoints, matches, reprojection_threshold: float = 5.0):
    """Verify candidate self-matches with a homography estimated by RANSAC."""
    if len(matches) < 4:
        return None, [], np.empty((0, 1), dtype=np.uint8)

    src = np.float32([keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src, dst, cv2.RANSAC, reprojection_threshold)
    if mask is None:
        return H, [], np.empty((0, 1), dtype=np.uint8)

    inlier_mask = mask.ravel().astype(bool)
    inliers = [m for m, keep in zip(matches, inlier_mask) if keep]
    return H, inliers, mask
