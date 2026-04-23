# Phase 4: Machine Learning - Python Notes 🤖

This repository contains essential Machine Learning foundations using Python.  
It covers Supervised and Unsupervised Learning, Deep Learning, and key ML concepts.

---

## 1. Introduction to Machine Learning 🧠

- Machine Learning (ML) is a subset of AI that allows systems to learn patterns from data and make predictions or decisions.
- **Key Components**:  
  - Dataset: training and testing data  
  - Features: input variables  
  - Labels/Targets: output variables (for supervised learning)  
  - Model: algorithm that learns patterns  
  - Training: process of fitting model to data  
  - Evaluation: measure model performance using metrics

---

## 2. Supervised Learning 📊

- Involves training a model on labeled data (input-output pairs).
- **Goal**: predict output for new inputs.
- **Types**:  
  1. Regression: predicts continuous values  
     - Examples: Linear Regression, Ridge Regression, Lasso Regression  
     - Metrics: Mean Squared Error (MSE), Mean Absolute Error (MAE), R² Score  
  2. Classification: predicts discrete labels  
     - Examples: Logistic Regression, Decision Trees, Random Forest, K-Nearest Neighbors (KNN), Naive Bayes, SVM  
     - Metrics: Accuracy, Precision, Recall, F1 Score, ROC-AUC
- **Steps**:  
  1. Split dataset into train and test sets  
  2. Choose model and train on training data  
  3. Predict on test data  
  4. Evaluate using performance metrics  
  5. Tune hyperparameters for better performance

---

## 3. Unsupervised Learning 🔍

- Training on data without labels.
- **Goal**: find patterns, groupings, or structure in the data.
- **Types**:  
  1. Clustering: group similar data points  
     - Examples: K-Means, Hierarchical Clustering, DBSCAN  
     - Evaluation: silhouette score, Davies-Bouldin index  
  2. Dimensionality Reduction: reduce feature space  
     - Examples: PCA, t-SNE, UMAP  
     - Applications: data visualization, noise reduction, feature extraction
- **Applications**:  
  - Customer segmentation  
  - Market basket analysis  
  - Anomaly detection

---

## 4. Deep Learning 🧠

- Subset of ML using neural networks with multiple layers.
- **Core Concepts**:  
  - Neural Network: layers of neurons connected with weights  
  - Activation functions: ReLU, Sigmoid, Tanh, Softmax  
  - Loss functions: MSE, Cross-Entropy  
  - Optimization: Gradient Descent, Adam  
  - Backpropagation: update weights using gradients
- **Types of Neural Networks**:  
  - Feedforward Neural Network (FNN)  
  - Convolutional Neural Network (CNN) – for images  
  - Recurrent Neural Network (RNN) – for sequences/time series  
  - Long Short-Term Memory (LSTM) – improved RNN for long dependencies
- **Frameworks**: TensorFlow, Keras, PyTorch
- **Applications**:  
  - Image recognition  
  - Natural Language Processing (NLP)  
  - Speech recognition  
  - Recommendation systems

---

# End of Phase-4 Machine Learning Notes

