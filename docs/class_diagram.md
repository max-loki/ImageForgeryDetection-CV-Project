# Class / Component Diagram

```text
ImageLoader/Input
       |
       v
Preprocessor
       |
       v
FeatureExtractor
       |
       v
FeatureMatcher
       |
       v
ForgeryDetector <------ RANSACVerifier
       |
       +-----------> ReportGenerator
       |
       +-----------> Database
```

Main Python components are separated into preprocessing, extraction, matching, geometric verification, detection, reporting, and persistence modules.
