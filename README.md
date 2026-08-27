# Spotify Tracks Analysis & Smart Recommendation System

A comprehensive machine learning and exploratory data analysis (EDA) pipeline that decodes the non-linear audio features driving track popularity on Spotify, directly powering an advanced music recommendation engine.

## 📋 Table of Contents
- [Spotify Tracks Analysis \& Smart Recommendation System](#spotify-tracks-analysis--smart-recommendation-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [1. Data Cleaning](#1-data-cleaning)
  - [2. Data Understanding](#2-data-understanding)
    - [2.1 Column Description](#21-column-description)
    - [2.2 Explicit Songs Analysis](#22-explicit-songs-analysis)
    - [2.3 Songs' Popularity Analysis](#23-songs-popularity-analysis)
    - [2.4 Track's Duration Analysis](#24-tracks-duration-analysis)
  - [3. Executive Summary \& Key Takeaways](#3-executive-summary--key-takeaways)
  - [4. Spotify Recommendation System App](#4-spotify-recommendation-system-app)

---

## 1. Data Cleaning
This initial phase establishes data integrity by handling missing values, filtering duplicates, and isolating active metadata. Crucially, "zero-popularity" metadata noise (inactive tracks or unplayed uploads) is handled separately to prevent structural distortion across continuous feature averages.

## 2. Data Understanding

### 2.1 Column Description
Mapping the physical and acoustic dimensions of the dataset, including core identifiers, technical variables (`loudness`, `tempo`, `key`), and Spotify-specific acoustic estimates (`danceability`, `energy`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`).

### 2.2 Explicit Songs Analysis
* **Statistical Distribution:** Boxplots and numerical averages reveal that explicit tracks lean heavily into high-volume, spoken-word-dense structures.
* **The Vocal Necessity:** Jointplot and sample filtering reveal a strict data boundary: explicit content clusters aggressively at an `instrumentalness` score of 0.0, proving that lyrical restrictions rely entirely on vocal-present recordings.
* **Machine Learning Diagnostics:** A Decision Tree Classifier and scaled Logistic Regression show that `speechiness` acts as the dominant predictor for explicit content, while binary flags like musical `mode` provide no classification power.

### 2.3 Songs' Popularity Analysis
* **The Non-Linear Reality:** Correlation matrices confirm near-zero linear relationships between isolated audio features and popularity, proving success is driven by complex feature synergies.
* **Algorithmic Sweet Spots:** Random Forest models combined with **Partial Dependence Plots (PDP)** and **SHAP Interpretation** map specific thresholds. `danceability` yields peak popularity scores within a distinct 0.62–0.72 window before facing a penalty, while `loudness` acts as a continuous positive driver.

### 2.4 Track's Duration Analysis
* **Industry Formatting:** Track length follows a highly standardized bell curve peaking between 3.0 and 4.0 minutes.
* **The Time Penalty:** Advanced ML feature importance ranks `duration_minutes` as the second most powerful predictor in the dataset. PDP models isolate strict "formatting cliffs," demonstrating aggressive algorithmic penalties for tracks breaking the 2.5 to 5.0-minute mainstream threshold.

---

## 3. Executive Summary & Key Takeaways
* **The Commercial Profile:** Mainstream streaming success is highly structured, deeply favoring vocal-present (`instrumentalness` ≈ 0), loud, rhythmically engaging tracks constrained inside a tight 3.3 to 3.9-minute format.
* **Synergy Over Single Metrics:** Individual acoustic attributes cannot linearly force or predict a hit. Popularity relies on multi-dimensional, non-linear interactions captured perfectly by modern ensemble models.

---

## 4. Spotify Recommendation System App
The architectural insights uncovered during the data understanding phase directly serve as the **core rules and feature weights** for the recommendation engine. 

Instead of matching tracks blindly on generic audio traits, the application leverages an upgraded content-based filtering approach tailored to handle the non-linear boundaries discovered in the EDA:
* **Feature Filtering:** Eliminates purely dead metadata (0 popularity) and leverages duration-clipping to align recommendations with optimal listening habits.
* **Distance Metrics Matrix:** Implements advanced similarity algorithms (such as Cosine Similarity) across the refined, non-linear acoustic feature space.
* **Intelligent Weighting:** Weights variables according to their Random Forest importance scores—prioritising dominant vectors like `acousticness` and `duration_minutes` over weaker variables like musical `mode` to ensure highly accurate, mood-coherent music discovery.