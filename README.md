[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

# Financial Complaint Auto-Routing with NLP

This project builds a supervised machine learning pipeline to classify consumer financial complaint narratives into financial product categories using the CFPB Consumer Complaint Database.

## Project Goal

The goal is to support automated complaint routing by predicting the correct product category from a consumer complaint narrative.

## Dataset

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The full dataset is not included in this repository. It can be downloaded from the official CFPB source or API.

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
