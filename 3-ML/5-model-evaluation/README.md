# 5 · Model Evaluation

Accuracy alone is misleading — especially on imbalanced datasets. This section covers how to actually know if your model is good.

---

## What You'll Learn

- Confusion matrix — the foundation of all classification metrics
- Precision, Recall, F1 — when to use each
- AUC-ROC — model performance across all thresholds
- `classification_report` — full breakdown in one call

---

## Progress Checklist

- [ ] `01-metrics.py` — accuracy, precision, recall, F1, AUC-ROC, confusion matrix

---

## Metrics Reference

| Metric | Formula | Use when |
|--------|---------|----------|
| Accuracy | (TP + TN) / total | Balanced classes only |
| Precision | TP / (TP + FP) | False positives are costly (spam filter) |
| Recall | TP / (TP + FN) | False negatives are costly (cancer screening) |
| F1 | 2 × (P × R) / (P + R) | Imbalanced classes, need both P and R |
| AUC-ROC | Area under curve | Compare models regardless of threshold |

---

## Confusion Matrix Layout

```
              Predicted 0   Predicted 1
Actual 0        TN (good)    FP (bad — false alarm)
Actual 1        FN (bad — missed!)   TP (good)
```

**TN** — True Negative (correctly predicted negative)  
**TP** — True Positive (correctly predicted positive)  
**FP** — False Positive (predicted positive, was negative)  
**FN** — False Negative (predicted negative, was positive)
