import cv2
import numpy as np
import streamlit as st
from PIL import Image

from modules.preprocessing import preprocess
from modules.feature_extractor import extract_sift, draw_keypoints
from modules.matcher import self_match
from modules.ransac import verify_matches
from modules.detector import spatially_filter_matches, suspicious_mask, annotate, confidence_score
from modules.report import build_pdf
from database.database import save_analysis, recent_analyses

st.set_page_config(page_title="VisionGuard - Image Forgery Detection", layout="wide")
st.title("Image Forgery & Tampering Detection")
st.caption("SIFT + feature matching + RANSAC-based geometric verification")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
col1, col2 = st.columns(2)
with col1:
    ratio = st.slider("SIFT ratio-test threshold", 0.60, 0.90, 0.75, 0.01)
    min_distance = st.slider("Minimum spatial separation", 10, 100, 30)
with col2:
    denoise = st.checkbox("Gaussian denoising", True)
    equalize = st.checkbox("Histogram equalization", False)

if uploaded:
    image = np.array(Image.open(uploaded).convert("RGB"))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if st.button("Analyze Image", type="primary"):
        with st.spinner("Running Computer Vision pipeline..."):
            gray, processed = preprocess(bgr, denoise=denoise, equalize=equalize)
            keypoints, descriptors = extract_sift(gray)

            if descriptors is None or len(keypoints) < 4:
                st.error("Not enough distinctive features were found in this image.")
                st.stop()

            candidates = self_match(descriptors, ratio=ratio)
            candidates = spatially_filter_matches(keypoints, candidates, min_distance=min_distance)
            H, inliers, _ = verify_matches(keypoints, candidates)
            mask = suspicious_mask(bgr.shape, keypoints, inliers)
            annotated, contours = annotate(bgr, mask)
            regions = [c for c in contours if cv2.contourArea(c) >= 100]
            score = confidence_score(len(candidates), len(inliers), len(regions))

            stats = {
                "Keypoints": len(keypoints),
                "Candidate matches": len(candidates),
                "Verified matches": len(inliers),
                "Suspicious regions": len(regions),
                "Screening score (%)": score,
            }
            save_analysis(uploaded.name, len(candidates), len(inliers), len(regions), score)

        st.subheader("Analysis Results")
        metric_cols = st.columns(5)
        for c, (k, v) in zip(metric_cols, stats.items()):
            c.metric(k, v)

        c1, c2 = st.columns(2)
        with c1:
            st.image(image, caption="Original", use_container_width=True)
            st.image(cv2.cvtColor(draw_keypoints(bgr, keypoints), cv2.COLOR_BGR2RGB), caption="SIFT Keypoints", use_container_width=True)
        with c2:
            match_vis = cv2.drawMatches(bgr, keypoints, bgr, keypoints, inliers[:100], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            st.image(cv2.cvtColor(match_vis, cv2.COLOR_BGR2RGB), caption="RANSAC-verified matches", use_container_width=True)
            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Suspicious-region visualization", use_container_width=True)

        pdf = build_pdf(uploaded.name, stats)
        st.download_button("Download PDF Report", data=pdf, file_name="forgery_detection_report.pdf", mime="application/pdf")

st.divider()
st.subheader("Recent Analysis History")
rows = recent_analyses()
if rows:
    st.dataframe(rows, use_container_width=True, column_config={
        "score": st.column_config.NumberColumn("Score", format="%.2f")
    })
else:
    st.info("No analysis history yet.")
