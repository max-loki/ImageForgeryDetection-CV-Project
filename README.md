# 🛡️ VeriPixel: Image Forgery & Tampering Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/OpenCV-4.8%2B-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/License-Academic_Use-brightgreen?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <b>A Computer Vision System for Copy-Move Image Forgery Detection utilizing Scale-Invariant Feature Transform (SIFT), Spatial Euclidean Filtering, RANSAC Geometric Homography Verification, and Morphological Region Segmentation.</b>
</p>

---

## 📌 Architecture & System Workflow

The detection pipeline processes suspicious images through a 7-stage Computer Vision pipeline designed to detect replicated regions with high transformation invariance (rotation, scaling, compression).

<p align="center">
  <img src="assets/pipeline_architecture.png" alt="VeriPixel Pipeline Architecture" width="100%"/>
</p>

```mermaid
flowchart LR
    A[📷 Input Image] --> B[⚙️ Preprocessing\nGrayscale & Gaussian Filter]
    B --> C[🔍 SIFT Extraction\nScale-Space & 128-d Descriptors]
    C --> D[🔗 Self-Matching\nkNN Matching & Lowe's Ratio]
    D --> E[📐 RANSAC Verification\nHomography Matrix Estimation]
    E --> F[🎭 Morphological Masking\nDilation & Contour Analysis]
    F --> G[📊 Results & Report\nScore + SQLite + PDF Export]

    classDef primary fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    class A,B,C,D,E,F,G primary;
```

---

## 🔬 Step-by-Step Computer Vision Pipeline in Action

Below is an end-to-end visualization of the internal detection stages operating on a copy-move tampered sample image:

<p align="center">
  <img src="assets/cv_pipeline_stages.png" alt="Computer Vision Pipeline Stages" width="100%"/>
</p>

### Pipeline Stages Breakdown

| Stage | Operation | Computer Vision Functionality | Output Description |
|---|---|---|---|
| **1. Input** | Validation & RGB Normalization | Reads image data, validates dimensions, and converts to working color space. | Standardized BGR / RGB tensor |
| **2. Preprocessing** | Gaussian Smoothing & Equalization | Applies $5 \times 5$ Gaussian kernel $(\sigma = 0)$ to suppress high-frequency noise and optional histogram equalization. | Denoised grayscale matrix $I(x,y)$ |
| **3. SIFT Extraction** | DoG Scale-Space Extrema | Computes multi-scale keypoints and calculates 128-dimensional gradient orientation histograms. | Keypoint coordinates $(x,y)$, scales, and descriptors |
| **4. Feature Matching** | kNN $(k=3)$ + Lowe's Ratio Test | Performs self-matching across the descriptor set; rejects trivial identical indices and non-distinctive matches ($d_1 / d_2 < \tau$). | Raw candidate match pairs |
| **5. Spatial Filtering** | Euclidean Distance Threshold | Prunes feature pairs located closer than minimum spatial threshold $\|p_1 - p_2\|_2 < d_{\min}$ to prevent keypoint clustering artifacts. | Spatially separated match candidates |
| **6. Geometric Verification** | RANSAC & Homography ($\mathbf{H}$) | Estimates planar projective transformation matrix $\mathbf{H} \in \mathbb{R}^{3 \times 3}$ and eliminates geometric outliers. | Verified inlier correspondences |
| **7. Mask & Annotation** | Morphological Dilation & Contours | Projects inlier points into binary mask, expands with elliptical structuring element, and draws bounding boxes. | Flagged suspicious regions & confidence score |

---

## 📐 Mathematical Foundations & Theoretical Principles

<p align="center">
  <img src="assets/sift_ransac_theory.png" alt="SIFT and RANSAC Theoretical Infographic" width="100%"/>
</p>

### 1. Scale-Space Representation & Difference of Gaussians (DoG)
To achieve scale and resolution invariance, the image is convolved with Gaussian kernels across multiple octaves:
$$L(x, y, \sigma) = G(x, y, \sigma) * I(x, y)$$
The scale-space extrema are identified efficiently via Difference-of-Gaussians (DoG):
$$D(x, y, \sigma) = (G(x, y, k\sigma) - G(x, y, \sigma)) * I(x, y) = L(x, y, k\sigma) - L(x, y, \sigma)$$

### 2. SIFT 128-Dimensional Local Descriptor
For each stable keypoint, local image gradients $\nabla I = (\frac{\partial I}{\partial x}, \frac{\partial I}{\partial y})$ are accumulated into $4 \times 4$ spatial sub-regions across 8 canonical orientation bins, producing an illumination-invariant and rotation-invariant feature vector $\mathbf{f} \in \mathbb{R}^{128}$.

### 3. Lowe's Nearest-Neighbor Ratio Criterion
To distinguish genuine copied feature matches from background textures, descriptor distances are evaluated against the first and second nearest non-identical neighbors:
$$\frac{\|\mathbf{f}_i - \mathbf{f}_{j1}\|_2}{\|\mathbf{f}_i - \mathbf{f}_{j2}\|_2} < \tau \quad (\text{Default: } \tau = 0.75)$$

### 4. RANSAC Projective Transformation (Homography)
Copy-move operations obey a consistent affine or projective geometric mapping $\mathbf{H}$. Given matched pairs $(p_1, p_2)$, RANSAC iteratively estimates:
$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} \sim \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
Point correspondences satisfying reprojection error $\|\mathbf{p}'_i - \mathbf{H}\mathbf{p}_i\|_2 < \epsilon$ are classified as inliers, filtering out uncorrelated false matches.

---

## 📊 Experimental Evaluation & Performance Characteristics

<p align="center">
  <img src="assets/performance_metrics.png" alt="VeriPixel Performance and Robustness Graphs" width="100%"/>
</p>

### Key Performance Insights:
* **Ratio Test Optimization (Plot A)**: Balancing Lowe's ratio between $0.70$ and $0.75$ yields peak F1-score $(> 0.91)$, effectively trading off false alarm rate against detection recall.
* **Geometric Inlier Scoring (Plot B)**: Tampering confidence transitions smoothly with verified inliers count; authentic images typically produce $< 4$ scattered inliers, whereas forged regions produce coherent clusters ($\ge 12$ inliers).
* **Attack Invariance (Plot C)**: The SIFT + RANSAC pipeline maintains superior detection accuracy under rotation ($\pm 45^\circ$) and scaling ($0.7\times - 1.5\times$) compared to traditional block-based discrete cosine transform (DCT) methods.

---

## 📂 Project Structure

```text
ImageForgeryDetection/
├── assets/                          # Generated Computer Vision diagrams & graphs
│   ├── pipeline_architecture.png    # System architecture workflow banner
│   ├── cv_pipeline_stages.png       # 6-stage Computer Vision detection visual
│   ├── performance_metrics.png      # Precision-Recall & Robustness metric charts
│   └── sift_ransac_theory.png       # Mathematical theory infographic
├── modules/                         # Core Computer Vision processing modules
│   ├── __init__.py
│   ├── preprocessing.py             # Grayscale conversion, Gaussian filter, Equalization
│   ├── feature_extractor.py         # SIFT keypoint extraction & rich visualization
│   ├── matcher.py                   # Self kNN descriptor matching & Lowe's ratio test
│   ├── ransac.py                    # RANSAC homography estimation & inlier filtering
│   ├── detector.py                  # Spatial filtering, morphological mask, scoring
│   └── report.py                    # Automated PDF forensic report generator
├── database/                        # Persistence layer
│   ├── __init__.py
│   └── database.py                  # SQLite schema, storage, & audit query logs
├── data/                            # Input & output image directory
│   ├── input/                       # Source test images
│   └── output/                      # Exported annotated results and masks
├── docs/                            # Software architecture & specification docs
│   ├── architecture.md
│   ├── workflow.md
│   ├── use_case.md
│   ├── class_diagram.md
│   ├── sequence_diagram.md
│   └── er_diagram.md
├── tests/                           # Unit test suite
│   └── test_detection.py            # Preprocessing & metric verification tests
├── app.py                           # Streamlit interactive UI application
├── generate_readme_assets.py        # Reproducible graphics generator script
├── requirements.txt                 # Project dependency specifications
└── README.md                        # Documentation & Project Guide
```

---

## 💻 Installation & Quickstart

### 1. Prerequisites
* Python 3.10, 3.11, or 3.12
* Git

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/ImageForgeryDetection.git
cd ImageForgeryDetection

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Interactive Web Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` to access the interactive GUI:
* Upload any test image (`.jpg`, `.jpeg`, `.png`).
* Tune ratio test thresholds and spatial distance parameters in real time.
* Inspect multi-view outputs (SIFT Keypoints, RANSAC match lines, Suspicious Region overlays).
* Export downloadable **PDF Forensic Analysis Reports**.

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

---

## 🖥️ Streamlit Application Interface Preview

```text
+-----------------------------------------------------------------------------+
|  🛡️ VeriPixel - Image Forgery & Tampering Detection                      |
|  SIFT + feature matching + RANSAC-based geometric verification              |
+-----------------------------------------------------------------------------+
|  [ Upload Image (PNG/JPG) ]                                                 |
|  Parameters:  [ Ratio Test: 0.75 ]  [ Min Distance: 30px ]                  |
|               [x] Gaussian Denoise   [ ] Histogram Equalize                 |
|  [ Analyze Image (Primary Action) ]                                         |
+-----------------------------------------------------------------------------+
|  Keypoints: 2,501 | Matches: 490 | Verified Inliers: 129 | Score: 94.6%     |
+-----------------------------------------------------------------------------+
|  [ Original Image ]              |  [ SIFT Keypoints & Orientations ]       |
|  [ RANSAC Verified Matches ]     |  [ Suspicious Region Contour Overlay ]   |
+-----------------------------------------------------------------------------+
|  [ 📄 Download PDF Report ]      |  [ SQLite Audit History Table ]          |
+-----------------------------------------------------------------------------+
```

---

## ⚠️ Limitations & Forensic Disclaimer

1. **Feature Dependency**: SIFT-based copy-move detection relies on distinctive local texture variations. Solid flat backgrounds, uniform skies, or heavily blurred regions with low gradient entropy cannot generate sufficient keypoints.
2. **Post-Processing Degradations**: Extreme JPEG compression ($Q < 30$) or aggressive non-linear filtering can disrupt descriptor invariance.
3. **Forensic Context**: The calculated *Screening Confidence Score* serves as a probabilistic indicator for triage and academic evaluation—not conclusive legal evidence of authenticity.

---

## 🎓 Academic Alignment & References

This project satisfies the coursework requirements for **CSE3010 Computer Vision**, demonstrating practical implementation of core curriculum concepts:
* **Scale-Invariant Feature Transform (SIFT)**: D. G. Lowe, *"Distinctive Image Features from Scale-Invariant Keypoints"*, IJCV, 2004.
* **Random Sample Consensus (RANSAC)**: M. A. Fischler and R. C. Bolles, *"Random Sample Consensus: A Paradigm for Model Fitting"*, ACM, 1981.
* **Image Morphology & Contour Analysis**: Morphological operations for spatial defect grouping and contour localization.

---

## 📄 License

This repository is licensed for **Academic and Educational Use**.
