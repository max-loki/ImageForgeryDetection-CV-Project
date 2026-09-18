# Sequence Diagram

```text
User -> Streamlit UI: Upload image
Streamlit UI -> Preprocessor: preprocess(image)
Preprocessor -> FeatureExtractor: grayscale image
FeatureExtractor -> Matcher: descriptors
Matcher -> RANSAC: candidate matches
RANSAC -> Detector: verified matches
Detector -> Database: save statistics
Detector -> Report: generate PDF
Report -> Streamlit UI: report bytes
Streamlit UI -> User: annotated results + report
```
