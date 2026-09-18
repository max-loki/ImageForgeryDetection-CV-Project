# 🛡️ VeriPixel: Digital Image Forgery & Tampering Detection

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/OpenCV-4.8%2B-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/License-Academic_Use-brightgreen?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <img src="assets/veripixel_hero_banner.jpg" alt="VeriPixel Forensic Vision Banner" width="100%"/>
</p>

<p align="center">
  <b>An Advanced Computer Vision System for Copy-Move Image Forgery Detection utilizing Scale-Invariant Feature Transform (SIFT), Spatial Distance Clustering, RANSAC Homography Geometric Inlier Verification, and Morphological Region Segmentation.</b>
</p>

---

## 🔬 Real-World Photographic Detection Stages

The pipeline processes high-resolution photographic imagery through consecutive invariant feature extraction and geometric verification stages:

<p align="center">
  <img src="assets/real_detection_stages.png" alt="Computer Vision Execution on Real Photographic Image" width="100%"/>
</p>

### Pipeline Stage Details

| Stage | Operation | Computer Vision Functionality | Output Description |
|---|---|---|---|
| **1. Input** | Image Ingestion & Normalization | Validates color channels, bit-depth, and spatial dimensions. | Standardized $H \times W \times 3$ RGB matrix |
| **2. Preprocessing** | Gaussian Denoising & Filtering | Applies a $5 \times 5$ Gaussian kernel ($\sigma = 0$) to suppress high-frequency sensor noise. | Denoised grayscale intensity matrix |
| **3. SIFT Extraction** | DoG Scale-Space Extrema | Identifies stable multi-scale extrema in octave pyramids and extracts $128$-dimensional orientation histograms. | Local invariant keypoints $(x, y, \sigma, \theta)$ & descriptors |
| **4. Feature Matching** | $k\text{NN}$ ($k=3$) + Lowe's Ratio Test | Performs descriptor self-matching; discards identical self-points and pairs where $d_1 \ge \tau \cdot d_2$. | Raw candidate feature correspondence vectors |
| **5. Spatial Filtering** | Euclidean Distance Threshold | Filters candidate pairs where $\|p_1 - p_2\|_2 < d_{\min}$ to prevent keypoint self-clustering false alarms. | Spatially separated match candidates |
| **6. Geometric Verification** | RANSAC & Homography ($\mathbf{H}$) | Estimates planar projective transformation $\mathbf{H} \in \mathbb{R}^{3 \times 3}$ and isolates geometric inliers. | Affine/projective consistent inlier matches |
| **7. Localization & Mask** | Morphological Dilation & Contours | Projects inlier points into a binary mask, applies elliptical morphological closing, and outlines suspicious regions. | Localized bounding boxes & confidence score |

---

## 📸 Real-World Multi-Scene Benchmark Evaluations

Detection performance demonstrated across natural landscapes, structured architecture, and authentic unaltered control images:

<p align="center">
  <img src="assets/real_cases_comparison.png" alt="Real-World Benchmark Evaluations" width="100%"/>
</p>

* **Case 1 (Natural Landscape)**: Detects and isolates cloned mountain structures across natural organic textures ($76$ verified RANSAC inliers).
* **Case 2 (Architectural Structure)**: Resolves duplicated glass facade windows across complex high-frequency urban patterns ($398$ inliers).
* **Case 3 (Unaltered Authentic Photo)**: Rejects ambient repetitive patterns via geometric homography verification, confirming authenticity with **$0$ false-positive detections**.

---

## 🖥️ Interactive Web Application & Forensic Dashboard

VeriPixel features an interactive Streamlit-based graphical interface for real-time parameter tuning, visual inspection, and instant reporting:

<p align="center">
  <img src="assets/veripixel_ui_dashboard.jpg" alt="VeriPixel Web Dashboard Interface" width="100%"/>
</p>

### Interactive Features:
* **Real-time Parameter Tuning**: Dynamic sliders for Lowe's ratio test threshold ($\tau$) and minimum spatial separation distance ($d_{\min}$).
* **Multi-View Visual Inspection**: Side-by-side comparison of original image, SIFT keypoint scales, RANSAC matching vectors, and localized contour overlays.
* **Automated Forensic PDF Export**: Single-click generation of audit-ready summary reports with tabulated metrics.
* **SQLite Audit Logging**: Persistent storage of past scan history, timestamps, file metadata, and confidence scores.

---

## 📐 Mathematical Foundations

### 1. Scale-Space Representation & Difference of Gaussians (DoG)
To ensure scale invariance across varied image resolutions, the input image $I(x,y)$ is convolved with variable-scale Gaussian kernels:
$$L(x, y, \sigma) = G(x, y, \sigma) * I(x, y)$$
Scale-space extrema are localized via Difference of Gaussians (DoG) across octave pyramids:
$$D(x, y, \sigma) = (G(x, y, k\sigma) - G(x, y, \sigma)) * I(x, y) = L(x, y, k\sigma) - L(x, y, \sigma)$$

### 2. SIFT 128-Dimensional Local Descriptor
For each stable keypoint, local gradient magnitudes and orientations are accumulated into $4 \times 4$ spatial sub-regions across $8$ canonical orientation bins, yielding an illumination- and rotation-invariant feature vector $\mathbf{f} \in \mathbb{R}^{128}$.

### 3. Lowe's Nearest-Neighbor Ratio Criterion
To differentiate genuine copy-move matches from ambient texture similarity, descriptor distances to the first ($d_1$) and second ($d_2$) closest non-identical neighbors are tested:
$$\frac{\|\mathbf{f}_i - \mathbf{f}_{j1}\|_2}{\|\mathbf{f}_i - \mathbf{f}_{j2}\|_2} < \tau \quad (\text{Default: } \tau = 0.75)$$

### 4. RANSAC Homography Estimation
Planar copy-move regions adhere to a projective transformation matrix $\mathbf{H} \in \mathbb{R}^{3 \times 3}$:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} \sim \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
Point pairs satisfying the reprojection error threshold $\|\mathbf{p}'_i - \mathbf{H}\mathbf{p}_i\|_2 < \epsilon$ are retained as verified geometric inliers.

---

## 📊 Quantitative Performance & Robustness Analysis

<p align="center">
  <img src="assets/evaluation_charts.png" alt="VeriPixel Evaluation Charts" width="100%"/>
</p>

### Key Performance Findings:
* **Threshold Sensitivity (Plot 1)**: Operating at Lowe's ratio $\tau \in [0.72, 0.76]$ maximizes the F1-score ($> 0.92$), balancing false-positive rejection against forgery recall.
* **Scoring Reliability (Plot 2)**: Forgery confidence increases with geometric consensus inliers, providing clear separation between authentic ($< 4$ inliers) and tampered images ($\ge 12$ inliers).
* **Adversarial Transformation Invariance (Plot 3)**: SIFT + RANSAC preserves high detection accuracy under rotation ($\pm 45^\circ$) and scaling ($0.7\times - 1.5\times$), outperforming classical block-based DCT techniques.

---

## 📂 Project Structure

```text
ImageForgeryDetection/
├── assets/                          # Photographic figures, UI showcases, & charts
│   ├── veripixel_hero_banner.jpg    # Forensic analysis hero banner
│   ├── real_detection_stages.png    # 6-stage detection visual on real photo
│   ├── real_cases_comparison.png    # Multi-scene real-world benchmark evaluations
│   ├── veripixel_ui_dashboard.jpg   # Interactive UI dashboard presentation
│   └── evaluation_charts.png        # Precision-Recall & Robustness evaluation graphs
├── modules/                         # Core Computer Vision processing modules
│   ├── __init__.py
│   ├── preprocessing.py             # Grayscale conversion, Gaussian filter, Equalization
│   ├── feature_extractor.py         # SIFT keypoint extraction & rich visualization
│   ├── matcher.py                   # Self kNN descriptor matching & Lowe's ratio test
│   ├── ransac.py                    # RANSAC homography estimation & inlier filtering
│   ├── detector.py                  # Spatial filtering, morphological mask, scoring
│   └── report.py                    # Automated PDF forensic report generator
├── database/                        # Database persistence layer
│   ├── __init__.py
│   └── database.py                  # SQLite schema, storage, & audit query logs
├── data/                            # Input & output data directory
│   ├── input/                       # Real test photos (landscape, building, castle)
│   └── output/                      # Exported annotated results & detection masks
├── docs/                            # Technical documentation & system specifications
│   ├── architecture.md
│   ├── workflow.md
│   ├── use_case.md
│   ├── class_diagram.md
│   ├── sequence_diagram.md
│   └── er_diagram.md
├── tests/                           # Automated unit test suite
│   └── test_detection.py            # Preprocessing & score verification tests
├── app.py                           # Interactive Streamlit Web Application
├── generate_real_assets.py          # Script for generating photographic assets
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation & Project Guide
```

---

## 💻 Installation & Quickstart

### 1. Prerequisites
* Python 3.10, 3.11, or 3.12
* Git

### 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ImageForgeryDetection.git
cd ImageForgeryDetection

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit Web Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser:
* Upload any test photograph (`.jpg`, `.jpeg`, `.png`).
* Adjust Lowe's ratio threshold and spatial separation sliders in real time.
* Inspect the multi-stage visualizations (Keypoints, Match lines, Suspicious Region overlays).
* Download structured **PDF Forensic Analysis Reports**.

---

## 🧪 Running Automated Tests

Run the test suite with `pytest`:

```bash
pytest -v
```

---

## ⚠️ Limitations & Forensic Disclaimer

1. **Feature Dependency**: SIFT-based copy-move detection requires distinctive local texture variations. Flat textures (e.g., solid skies, smooth studio backgrounds) lack the gradient entropy needed for keypoint extraction.
2. **Post-Processing Artifacts**: Heavy JPEG compression ($Q < 30$) or extreme non-linear blurs can degrade descriptor fidelity.
3. **Forensic Context**: The generated *Confidence Score* is intended as a triage and screening metric for academic and investigative workflows, not legal proof of authenticity.

---

## 🎓 Academic Alignment & References

This project fulfills coursework requirements for **CSE3010 Computer Vision**:
* **Scale-Invariant Feature Transform (SIFT)**: D. G. Lowe, *"Distinctive Image Features from Scale-Invariant Keypoints"*, International Journal of Computer Vision (IJCV), 2004.
* **Random Sample Consensus (RANSAC)**: M. A. Fischler and R. C. Bolles, *"Random Sample Consensus: A Paradigm for Model Fitting"*, Communications of the ACM, 1981.
* **Mathematical Morphology**: Structuring elements, dilation, and closing operations for spatial candidate grouping and contour extraction.

---

## 📄 License

This repository is licensed for **Academic and Educational Use**.
