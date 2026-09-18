# Image Forgery & Tampering Detection System

A Computer Vision project for detecting possible copy-move image forgery using image preprocessing, SIFT feature extraction, feature matching, and RANSAC-based geometric verification.

## Overview

Digital images can be manipulated by copying a region of an image and pasting it elsewhere. This project analyzes an uploaded image, extracts local visual features, searches for similar feature regions, removes geometrically inconsistent matches using RANSAC, and highlights suspicious areas.

> **Important:** The system provides an indication of possible tampering. It is not a forensic proof of authenticity.

## Objectives

- Preprocess images before analysis.
- Extract local features using SIFT.
- Match feature descriptors within the same image.
- Verify geometrically consistent matches using RANSAC/homography.
- Identify and visualize suspicious regions.
- Produce a confidence-style score and downloadable analysis report.
- Maintain an analysis history using SQLite.

## Major Functional Modules

1. **Image Preprocessing** - validation, grayscale conversion, denoising and optional histogram equalization.
2. **Feature Extraction** - SIFT keypoint and descriptor extraction.
3. **Feature Matching** - descriptor matching and ratio-test filtering.
4. **Geometric Verification** - RANSAC/homography filtering of candidate matches.
5. **Forgery Region Detection** - grouping verified matches and generating a suspicious mask.
6. **Report & History** - SQLite history and PDF report generation.

## Computer Vision Concepts Used

- Image preprocessing
- Grayscale conversion
- Gaussian filtering
- Histogram processing
- SIFT
- Feature descriptors
- Feature matching
- Homography
- RANSAC
- Morphological processing
- Contour analysis

## System Workflow

```text
Image Upload
     |
     v
Input Validation
     |
     v
Preprocessing
     |
     v
SIFT Feature Extraction
     |
     v
Self Feature Matching
     |
     v
Ratio Test
     |
     v
RANSAC / Homography Verification
     |
     v
Suspicious Region Mask
     |
     v
Visualization + Score
     |
     v
SQLite History + PDF Report
```

## Project Structure

```text
ImageForgeryDetection/
├── app.py
├── requirements.txt
├── README.md
├── statement.md
├── modules/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── feature_extractor.py
│   ├── matcher.py
│   ├── ransac.py
│   ├── detector.py
│   └── report.py
├── database/
│   ├── __init__.py
│   └── database.py
├── data/
│   ├── input/
│   └── output/
├── tests/
│   └── test_detection.py
└── docs/
    ├── architecture.md
    ├── workflow.md
    ├── use_case.md
    ├── class_diagram.md
    ├── sequence_diagram.md
    └── er_diagram.md
```

## Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The application provides controls for uploading an image and running the analysis pipeline.

## Testing

Run:

```bash
pytest -q
```

The tests cover preprocessing and basic pipeline behavior.

## Output

The application displays:

- Original image
- Preprocessed image
- SIFT keypoints
- Candidate feature matches
- RANSAC-verified matches
- Suspicious-region mask
- Annotated result
- Analysis statistics
- PDF report

## Limitations

- Copy-move detection depends on sufficient distinctive local features.
- Highly blurred, textureless, heavily compressed, or very small manipulated regions can be difficult to detect.
- A high score does not prove that an image is forged.
- The current implementation is designed as an academic Computer Vision project rather than a production forensic system.

## Future Enhancements

- Add SURF/HOG comparison where licensing and implementation constraints permit.
- Add block-based copy-move detection.
- Add splicing detection using a supervised classifier.
- Add a larger benchmark dataset and automated metric evaluation.
- Add user authentication and role-based access.
- Add batch image analysis.

## Academic Alignment

The project applies Computer Vision topics including image preprocessing, feature extraction, matching, homography/RANSAC, segmentation-style region generation, and image analysis. These concepts align with the CSE3010 Computer Vision syllabus and the VITyarthi project requirement to build an original project relevant to the course.

## License

For academic/educational use.
