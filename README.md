# Generative Data Augmentation for Small-Cohort Glioblastoma Diagnosis from Circulating microRNA

**Why same-modality validation overstates performance**

## Overview

Circulating microRNAs (miRNAs) are attractive minimally invasive biomarker candidates for glioblastoma (GBM), but discovery cohorts in this literature are typically tiny (tens of patients), which makes training a reliable classifier difficult. Generative data augmentation — synthesizing additional training examples with a learned generative model instead of collecting more patients — is an increasingly common response to this problem.

This project asks a more pointed question than most papers in this space: **does that augmentation actually generalize, or does it just look better on validation data that resembles the training data?**

To test this, we built an **escalating validation framework**: evaluate first on an independent cohort of the *same* modality (plasma), then on a cohort from a *different* modality and platform (solid tissue). The gap between those two results is the actual finding.

## Data

Four public cohorts, harmonized onto a common set of **201 mature miRNAs** present across all of them:

| Cohort | Modality | N | Role |
|---|---|---|---|
| GSE122488 | Blood plasma | 38 (22 tumour: 12 GBM + 10 grade II–III glioma, 16 healthy control) | Discovery / training |
| GSE184472 | Blood plasma | 118 (45 tumour, 73 control) | Independent same-modality validation |
| CGGA | Solid tissue | 198 (81 GBM, 117 non-GBM glioma) | External cross-platform validation |
| GSE90603 | Solid tissue + cell lines | 25 | Biological validation (tumour vs. non-tumour/astrocyte) |

**Important caveat on class definitions:** "tumour" does not mean the same thing in every cohort. In GSE122488, the positive class pools GBM with lower-grade glioma against *healthy* controls. In CGGA, there are no healthy controls at all — the comparison is strictly GBM vs. *non-GBM glioma* (grade II–III). This mismatch is one of the contributors to the cross-cohort generalization gap described below, not just a modality difference.

Raw data isn't included in this repo (large files, already publicly hosted). Source accessions: GSE122488, GSE184472, GSE90603 (GEO/NCBI), CGGA microRNA array 198 (cgga.org.cn).

## Pipeline

1. **`preprocessing.ipynb`** — parses raw GEO/CGGA files, harmonizes all four cohorts onto the shared 201-miRNA feature set, extracts clinical labels, writes `processed/` and `ml_ready/` splits.
2. **Baseline models** — Random Forest, XGBoost, and a tabular Transformer trained directly on the raw 38-patient discovery cohort (no augmentation).
3. **Generative augmentation** — CTGAN and TVAE are each fit on the 38-patient cohort and used to generate 500 synthetic samples. CTGAN produces a near-balanced synthetic split (253 tumour / 247 control); **TVAE over-represents the tumour class relative to the real discovery cohort** (see Limitations).
4. **`training.ipynb`** — trains classifiers on augmented data, selects the champion model (TVAE + XGBoost), and evaluates it across validation stages, including Min-Max feature harmonization before testing on CGGA.
5. **Biomarker discovery** — Gini feature importances extracted from the champion model to identify candidate diagnostic miRNAs (`top_20_biomarkers.png`).

## Results

| Pipeline | Test cohort | AUROC | Accuracy | Recall |
|---|---|---|---|---|
| Baseline (no augmentation), best of 3 models | GSE184472 (n=118) | 0.42–0.53 | — | — |
| **TVAE + XGBoost (champion)** | GSE184472 (n=118) | **0.592** (95% CI 0.485–0.699) | — | — |
| TVAE + XGBoost (champion) | CGGA (n=198), before harmonization | 0.403 | 0.556 | 0.074 |
| TVAE + XGBoost (champion) | CGGA (n=198), after Min-Max harmonization | 0.467 | 0.409 | **1.00** |

None of the AUROCs reported here are statistically distinguishable from chance (0.5) at p < 0.05 — including the "champion" model's 0.592 on GSE184472 (p = 0.092).

The post-harmonization CGGA result is a degenerate classifier: recall of 1.00 was achieved by predicting *every single sample* as GBM — not by actually discriminating tumour from non-tumour (`cgga_confusion_matrix.png`).

## The actual finding

Augmentation gave a small, not-statistically-significant improvement when tested on a second plasma cohort — and that improvement **did not transfer** to a tissue cohort on a different platform. The gap is attributable to a combination of:

- **Modality mismatch** — plasma miRNA levels reflect contributions from many tissues (including blood cells) and are sensitive to pre-analytical handling (e.g. hemolysis); tissue miRNA levels do not share these confounds.
- **Inconsistent class definitions across cohorts** (see Data section above).
- **Synthetic class-imbalance drift** — TVAE's synthetic data shifts the tumour/control ratio away from the real discovery cohort, which was not fully accounted for downstream.
- **Incomplete cross-platform harmonization** — Min-Max scaling aligns feature ranges but not distribution shape or central tendency, and is sensitive to outliers.

**This is the point of the project**: a lot of small-cohort biomarker papers validate only on a second, similar dataset and report that as "external validation." This project shows that bar is too low — same-modality validation can look like a genuine improvement while the model has learned nothing that generalizes across platforms. Any claim of a usable miRNA biomarker panel for GBM needs validation across platforms and tissue types before it means anything clinically.

## Limitations

- Discovery cohort was small and biologically heterogeneous (GBM and lower-grade glioma pooled as "tumour").
- Each generator/classifier was trained with a single random seed — run-to-run variability was not characterized.
- Biomarker feature-importance rankings are exploratory and have not been independently validated.

## Repository contents

```
preprocessing.ipynb          # Data harmonization pipeline (4 cohorts → shared feature set)
training.ipynb               # Baseline + augmented model training, evaluation, harmonization
check_cgga.py                # CGGA data inspection utility
check_geo.py                 # GEO series matrix inspection utility
peek.py                      # Generic dataset preview utility
top_20_biomarkers.png        # Gini feature importance, champion model
cgga_confusion_matrix.png    # Champion model confusion matrix on CGGA, pre/post harmonization
```
