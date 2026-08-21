# Lung Cancer Detection System

An end-to-end Deep Learning platform for detecting lung cancer from CT scan images using **ResNet50, TensorFlow, FastAPI, and React**.

## Live Demo

**Frontend:**
https://lung-cancer-frontend-axwt.onrender.com

**Backend API:**
https://lung-cancer-backend-0que.onrender.com

> **Note:** This project is developed for research and educational purposes and should not be used as a substitute for professional medical diagnosis.

---

## Overview

The **Lung Cancer Detection System** is a full-stack deep learning application designed to analyze CT scan images and classify them as **Normal** or **Malignant**.

The system combines a **ResNet50-based deep learning model** with **Grad-CAM explainability** to provide visual insights into the regions of the CT scan that influence the model's prediction.

The application provides a modern React-based interface where users can upload CT scan images, receive predictions, and analyze the model's results.

---

## Key Features

* **Deep Learning Classification**
  ResNet50-based transfer learning model for CT scan classification.

* **Lung Cancer Prediction**
  Classifies CT scan images as **Normal** or **Malignant**.

* **Grad-CAM Explainability**
  Generates heatmaps to visualize the regions influencing the model's prediction.

* **Modern Web Interface**
  React and Vite-based frontend for image upload and result visualization.

* **REST API**
  FastAPI backend for model inference and image processing.

* **Dockerized Application**
  Backend containerized using Docker for consistent deployment.

* **Cloud Deployment**
  Frontend and backend deployed using Render.

---

## Tech Stack

### Frontend

* React
* Vite
* React Router
* CSS3

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* OpenCV
* NumPy

### Machine Learning

* TensorFlow
* Keras
* ResNet50
* Scikit-learn
* Grad-CAM

### Deployment

* Docker
* Render

### Development Tools

* Git
* GitHub
* Docker Compose

---

## System Architecture

```text
                  ┌─────────────────────┐
                  │      User           │
                  │   CT Scan Upload    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   React Frontend    │
                  │       + Vite        │
                  └──────────┬──────────┘
                             │
                        REST API
                             │
                             ▼
                  ┌─────────────────────┐
                  │   FastAPI Backend   │
                  │ Image Processing    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     ResNet50        │
                  │  Deep Learning      │
                  │      Model          │
                  └──────────┬──────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
          ┌───────────────┐     ┌───────────────┐
          │  Prediction   │     │   Grad-CAM    │
          │ Normal /      │     │   Heatmap     │
          │ Malignant     │     │ Visualization │
          └───────────────┘     └───────────────┘
```

---

## Project Structure

```text
lung-cancer-detection/
│
├── backend/
│   ├── Dockerfile
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── model/
│   ├── training/
│   ├── preprocessing/
│   └── ...
│
├── data/
│   └── ...
│
├── notebooks/
│   └── ...
│
├── scripts/
│   └── ...
│
├── docker-compose.yml
├── render.yaml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.11+
* Node.js 20+
* npm
* Docker
* Docker Compose
* Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ajaykumar1234484/lung-cancer-detection.git
cd lung-cancer-detection
```

If the application files are inside the nested project directory:

```bash
cd lung-cancer-detection
```

### 2. Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Running with Docker

From the project root:

```bash
docker-compose up --build
```

This starts the application using Docker Compose.

---

## Model

The project uses **ResNet50** with transfer learning for image classification.

### Workflow

```text
CT Scan Image
      ↓
Image Preprocessing
      ↓
ResNet50 Model
      ↓
Prediction
      ↓
Normal / Malignant
      ↓
Grad-CAM Visualization
```

Grad-CAM is used to generate a heatmap showing the areas of the image that contributed most to the model's prediction.

---

## API

The FastAPI backend provides REST endpoints for:

* Image upload
* Model inference
* Prediction results
* Grad-CAM visualization

Swagger documentation is available at:

```text
/docs
```

For the deployed backend:

https://lung-cancer-backend-0que.onrender.com/docs

---

## Deployment

The application is deployed using **Render**.

### Frontend

https://lung-cancer-frontend-axwt.onrender.com

### Backend

https://lung-cancer-backend-0que.onrender.com

The frontend communicates with the FastAPI backend through the configured `VITE_API_URL` environment variable.

---

## Screenshots

Add screenshots of the application here to make the project easier to understand.

Example:

```markdown
![Application Dashboard](path/to/screenshot.png)
```

Recommended screenshots:

* Application dashboard
* CT scan upload screen
* Prediction result
* Grad-CAM heatmap

---

## Future Improvements

* Improve model accuracy with a larger dataset.
* Add multi-class lung disease classification.
* Add patient history and prediction tracking.
* Improve model explainability.
* Add authentication and role-based access.
* Add automated model monitoring.
* Improve mobile responsiveness.

---

## Disclaimer

This software is intended **only for research and educational purposes**.

The predictions generated by this system must **not** be considered a medical diagnosis. Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment.

---

## License

This project is distributed under the **MIT License**.

---

## Author

**Ajay Kumar**

GitHub:
https://github.com/Ajaykumar1234484

Project Repository:
https://github.com/Ajaykumar1234484/lung-cancer-detection

**Live Project:**
https://lung-cancer-frontend-axwt.onrender.com
