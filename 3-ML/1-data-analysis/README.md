# 1 · Data Analysis

Before training any model, you need to load, inspect, and clean data. This section covers the tools every ML engineer uses daily.

---

## What You'll Learn

- **NumPy** — arrays, vectorized math, no Python loops
- **Pandas** — load CSVs, inspect data, filter, group, aggregate
- **EDA** — 7-step process to understand any dataset before modeling
- **SQL + Pandas** — query databases and continue analysis in Python

---

## Progress Checklist

### NumPy
- [ ] `numpy/01-arrays.py` — create 1D/2D arrays, element-wise ops
- [ ] `numpy/02-dimensions.py` — ndim, shape, size, reshape, flatten
- [ ] `numpy/03-indexing-slicing.py` — 1D and 2D indexing
- [ ] `numpy/04-vector.py` — vectorized operations, broadcasting, dot product
- [ ] `numpy/05-stats.py` — mean, max, min, sum, std, zeros, ones, arange, random

### Pandas
- [ ] `pandas/01-series.py` — 1D labeled array, index access
- [ ] `pandas/02-dataframe.py` — 2D table, head/tail, info, filter, add column
- [ ] `pandas/03-read-csv.py` — load CSV, handle missing values, save
- [ ] `pandas/04-mini-project.py` — student dataset analyzer

### EDA
- [ ] `eda/01-eda-basics.py` — full 7-step EDA with visualizations
- [ ] `eda/02-mini-project.py` — student EDA (your first full analysis)

### SQL + Pandas
- [ ] `sql-pandas/01-sql-eda.py` — SQLite → Pandas → EDA pipeline

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `ndarray` | NumPy's core type — faster than Python lists for math |
| `reshape(-1, 1)` | Used before feeding data to sklearn models |
| `DataFrame` | Pandas' 2D table — rows are samples, columns are features |
| `fit_transform` vs `transform` | Fit only on training data, then transform both sets |
| EDA | Always do this before modeling — understand your data first |

---

## Resources

| Resource | What |
|----------|------|
| Kaggle — Pandas course | Best practical Pandas intro |
| NumPy official quickstart | Dense, work through all examples |
