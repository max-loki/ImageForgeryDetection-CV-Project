# Workflow Diagram

```text
START
  |
Upload image
  |
Validate input
  |
Preprocess
  |
Extract SIFT features
  |
Match descriptors within image
  |
Apply ratio test
  |
Spatially filter candidate matches
  |
RANSAC homography verification
  |
Generate suspicious mask
  |
Find suspicious contours
  |
Calculate screening score
  |
Save history + generate report
  |
Display results
  |
END
```
