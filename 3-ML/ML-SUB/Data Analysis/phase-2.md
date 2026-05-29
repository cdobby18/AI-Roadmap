# Phase 2: Data Analysis - Python Notes 📊

This repository contains essential Python data analysis foundations.  
It covers EDA, NumPy, Pandas, SQL integration, and data visualization techniques.

---

## 1. Introduction to Data Analysis 📝

- **Types of Data Analysis**:  
  - **Descriptive**: summarize main features of data  
  - **Exploratory (EDA)**: find patterns, anomalies, test hypotheses  
  - **Inferential**: make predictions or generalizations from sample data

---

## 2. Exploratory Data Analysis (EDA) 🔍

- Process to understand dataset structure, patterns, and relationships.
- **Steps**:  
  1. Load data (CSV, Excel, SQL, JSON)  
  2. Inspect shape, columns, data types  
  3. Summary statistics: mean, median, mode, std, min, max  
  4. Check missing values and duplicates  
  5. Visualizations:  
     - Histograms, Boxplots, Scatterplots, Bar charts  
     - Libraries: `matplotlib`, `seaborn`  
  6. Correlation analysis: numeric relationships  
  7. Feature distribution: outliers, skewness, categorical distributions

---

## 3. NumPy (Numerical Python) ⚡

- Library for numerical computations.
- Supports:  
  - Arrays (`ndarray`)  
  - Vectorized operations (fast arithmetic on entire arrays)  
  - Mathematical functions (`mean`, `sum`, `sqrt`, `sin`, etc.)  
  - Random number generation

- **Key Operations**:  
  - Array creation: `np.array()`, `np.zeros()`, `np.ones()`, `np.arange()`, `np.linspace()`  
  - Indexing & slicing arrays  
  - Reshaping arrays: `reshape()`, `flatten()`  
  - Broadcasting for arithmetic operations  
  - Aggregations: `sum()`, `mean()`, `min()`, `max()`, `std()`

---

## 4. Pandas 🐼

- Library for data manipulation and analysis.
- **Core Data Structures**:  
  - `Series`: 1D labeled array  
  - `DataFrame`: 2D labeled table

- **Key Functions**:  
  - Reading data: `pd.read_csv()`, `pd.read_excel()`, `pd.read_sql()`  
  - Inspecting data: `head()`, `tail()`, `info()`, `describe()`, `shape`  
  - Selecting data: `loc[]`, `iloc[]`, filtering  
  - Data cleaning: `dropna()`, `fillna()`, `drop_duplicates()`  
  - Transformations: `apply()`, `map()`, `replace()`, `rename()`  
  - Grouping & aggregation: `groupby()`, `agg()`, `pivot_table()`  
  - Merging & joining: `merge()`, `join()`, `concat()`

---

## 5. SQL with Pandas 🛢️

- Combine SQL queries with Python data manipulation.
- **Steps**:  
  1. Connect to database (`sqlite3.connect()` or SQLAlchemy engine)  
  2. Run SQL queries: `pd.read_sql("SELECT * FROM table_name", conn)`  
  3. Perform EDA on SQL-extracted DataFrame

- **Common SQL Operations**:  
  - `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `JOIN`  
  - Aggregations: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`

- **Pandas Equivalent**:  
  - `df.groupby()`, `df.merge()`, `df.sort_values()`, `df.query()`

---

## 6. Data Visualization (Basics) 📈

- **Libraries**:  
  - `matplotlib.pyplot`: basic plots (line, bar, scatter, histogram, pie)  
  - `seaborn`: advanced statistical plots (heatmap, boxplot, pairplot, distplot)

- **Steps**:  
  1. Import library: `import matplotlib.pyplot as plt`, `import seaborn as sns`  
  2. Create figure and axes: `plt.figure()`, `sns.plot()`  
  3. Customize plot: `title()`, `xlabel()`, `ylabel()`, `legend()`, `grid()`  
  4. Show or save plot: `plt.show()`, `plt.savefig()`

---

# End of Phase-2 Data Analysis Notes