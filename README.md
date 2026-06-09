[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

# Financial Complaint Auto-Routing with NLP

This project builds a supervised machine learning pipeline to classify consumer financial complaint narratives into financial product categories using the CFPB Consumer Complaint Database.

## Project Goal

The goal is to support automated complaint routing by predicting the correct product category from a consumer complaint narrative.

## Dataset

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The project uses public consumer complaint narratives from the CFPB API.

- Input text column: `complaint_what_happened`
- Target label column: `product`
- Raw local file: `data/raw/cfpb_complaints_2024_raw.csv`

The raw CSV is downloaded locally by `notebooks/01_data_download.ipynb`. It is not included in this repository and should not be uploaded to GitHub. The repository ignores raw data files under `data/raw/` and ignores `*.csv` files.

## Version 1: Scikit-learn Baseline

Planned Version 1 pipeline:

`CFPB complaint narrative -> TF-IDF features -> Logistic Regression / Naive Bayes / Linear SVM -> product category`

## Skills Demonstrated

- Python
- Pandas
- Natural Language Processing
- TF-IDF
- Scikit-learn
- Classification modeling
- Accuracy, precision, recall, F1-score
- Confusion matrix

## Future Upgrade

A future Version 2 may compare the Scikit-learn baseline with a PyTorch / DistilBERT transformer model.
