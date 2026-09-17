# Behavioral Metrics Statistical Analysis & Bootstrapping

## Overview
This repository contains a Python-based statistical analysis pipeline designed to calculate and visualize the mean differences in behavioral metrics (Stress and Boredom) under varying conditions (Timer vs. No Timer). 

## Technical Approach
Instead of relying on standard parametric tests, this project utilizes **Custom Bootstrap Resampling** to generate 95% Confidence Intervals. This non-parametric approach is highly robust for smaller datasets or non-normally distributed behavioral data.

## Tech Stack
*   **Data Manipulation:** `pandas`, `numpy`
*   **Statistical Modeling:** `sklearn.utils.resample` (Bootstrapping with 10,000 iterations)
*   **Data Visualization:** `matplotlib.pyplot`

## Output & Visualization
The script generates a publication-ready Forest Plot detailing:
*   The mean change (Delta) for each behavioral metric.
*   The 95% Confidence Intervals calculated via bootstrapping.
*   Visual annotations indicating statistical significance (whether the CI crosses the zero-effect line).

*(Note to yourself: Once you upload this to GitHub, take a screenshot of the graph your code generates and add the image right here in the README!)*
