# Lung Cancer Detection System

An end-to-end Deep Learning platform for detecting lung cancer from CT scan images. Built with **TensorFlow**, **FastAPI**, and **React**.

## 🚀 Overview
This repository contains a full-stack application designed to aid medical professionals in radiology. It uses a **ResNet50** convolutional neural network to classify Axial CT scans as either "Normal" or "Malignant".

### Key Features
- **Deep Learning Model**: Transfer learning based on ResNet50.
- **Explainability**: Integrated Grad-CAM heatmaps to visualize the model's focus.
- **Radiology Dashboard**: Modern React interface for scan uploads and result analysis.
- **REST API**: High-performance FastAPI backend for model inference.
- **Dockerized**: Easy deployment using Docker Compose.

---

## 🛠️ Tech Stack
- **Frontend**: React, Vite, React Router, CSS3 (Vanilla)
- **Backend**: FastAPI, Uvicorn, Python 3.11
- **ML/DS**: TensorFlow, Keras, OpenCV, NumPy, Scikit-learn
- **Deployment**: Docker, Docker Compose

---

## 📂 Project Structure
```text
lung-cancer-detection/
├── model/           # ML training & processing scripts
├── backend/          # FastAPI server and utility logic
├── frontend/         # React dashboard and components
├── data/             # CT scan storage (raw & processed)
├── notebooks/        # Exploratory Data Analysis & experiments
└── docker-compose.yml # Full stack orchestration
```

---

## 🚦 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.11 (if running locally)
- Node.js 20+ (if running locally)

### 2. Installation
```bash
git clone https://github.com/your-username/lung-cancer-detection.git
cd lung-cancer-detection
```

### 3. Data Preparation
Place your CT scans in `data/raw/normal` and `data/raw/malignant`. Then run:
```bash
python model/preprocess.py
```

### 4. Running the Application
Using Docker Compose:
```bash
docker-compose up --build
```
The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (Swagger UI)

---

## 📜 Disclaimer
This software is intended for research and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
