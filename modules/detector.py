import cv2
import numpy as np


def spatially_filter_matches(keypoints, matches, min_distance: float = 30.0):
    """Keep matches whose two points are sufficiently separated spatially."""
    result = []
    for m in matches:
        p1 = np.array(keypoints[m.queryIdx].pt)
        p2 = np.array(keypoints[m.trainIdx].pt)
        if np.linalg.norm(p1 - p2) >= min_distance:
            result.append(m)
    return result


def suspicious_mask(shape, keypoints, matches, dilation: int = 15):
    """Create a visualization mask around verified matched feature locations."""
    mask = np.zeros(shape[:2], dtype=np.uint8)
    for m in matches:
        p1 = tuple(np.round(keypoints[m.queryIdx].pt).astype(int))
        p2 = tuple(np.round(keypoints[m.trainIdx].pt).astype(int))
        cv2.circle(mask, p1, 12, 255, -1)
        cv2.circle(mask, p2, 12, 255, -1)

    if dilation > 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation, dilation))
        mask = cv2.dilate(mask, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


def annotate(image, mask):
    result = image.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(result, "Suspicious", (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return result, contours


def confidence_score(candidate_count: int, verified_count: int, region_count: int) -> float:
    """Heuristic visualization score, not a forensic probability."""
    if candidate_count <= 0:
        return 0.0
    ratio = verified_count / candidate_count
    score = min(100.0, 100.0 * ratio * min(1.0, verified_count / 20.0))
    if region_count == 0:
        score *= 0.5
    return round(score, 2)
