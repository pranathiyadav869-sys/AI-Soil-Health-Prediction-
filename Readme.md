<h1 align="center">🌱 AI Soil Health Prediction System</h1>

<p align="center">
  <b>Hybrid Multimodal Deep Learning for Smart Agriculture</b><br>
  <i>Soil Data 📊 + NDVI 🌿 + Weather 🌦️ + Image Intelligence 🖼️</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Models-8-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Best-CNN--LSTM-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/R²-0.9609-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Accuracy-89.39%25-brightgreen?style=for-the-badge"/>
</p>

---

## 🚀 Project Overview

This project presents a **Hybrid Multimodal AI System** for predicting **Soil Health Index (SHI)** by combining:

* 📊 Tabular soil & crop data
* 🌿 NDVI time-series (vegetation index)
* 🌦️ Weather data
* 🖼️ Image-based soil & disease analysis

Unlike fully fused architectures, this system uses **separate deep learning pipelines** and integrates results at the **application level**, making it efficient and practical.

---

## 🎯 Objectives

* Predict **Soil Health Index (0–1 scale)**
* Classify soil condition (**Poor / Moderate / Healthy**)
* Recommend suitable crops
* Provide fertilizer & irrigation advice
* Detect soil type and plant diseases from images

---

## 🧠 System Architecture (Actual Implementation)

```text id="arch_real"
🧩 TABULAR + TIME-SERIES PIPELINE
--------------------------------
Input:
  • Soil Data (N, P, K, pH, Organic Carbon, Sand)
  • Weather Data (Temperature, Rainfall, Humidity)
  • NDVI Time-Series

        │
        ▼
 Deep Learning Models
 (LSTM / CNN-LSTM / Transformer / GRU / etc.)
        │
        ▼
 Soil Health Index + Recommendations


🖼️ IMAGE PIPELINE (SEPARATE)
---------------------------
Input:
  • Soil / Crop Image

        │
        ▼
     ResNet50
        │
        ▼
 Soil Type + Disease Detection


🔗 FINAL INTEGRATION
-------------------
Outputs combined in:
👉 Gradio Application (UI Layer)

Final Output:
✔ Soil Health Index  
✔ Crop Recommendations  
✔ Fertilizer Advice  
✔ Irrigation Advisory  
✔ Image-Based Insights  
✔ PDF Report
```

📌 **Key Insight:**
This project uses **decision-level fusion (not feature-level fusion)**.

---

## 📂 Datasets Used

### 📊 Tabular Dataset (Custom Engineered)

* Crop Recommendation Dataset
* WoSIS Soil Data:

  * Organic Carbon
  * Soil pH
  * Sand Content

📁 Final dataset:

```id="ds1"
final_dataset_with_ndvi_weather.csv
```

Includes:

* NDVI time-series (8 timesteps)
* Weather sequences

---

### 🖼️ Image Datasets

* `ai4a-lab/comprehensive-soil-classification-datasets`
* `prasanshasatpathy/soil-types`
* `emmarex/plantdisease`

✔ Used for:

* Soil classification
* Plant disease detection

---

## ⚙️ Data Processing Pipeline

* ✔ Data cleaning & normalization
* ✔ Topsoil filtering
* ✔ Feature merging (nearest neighbor matching)
* ✔ Class balancing using SMOTE
* ✔ NDVI time-series generation
* ✔ Weather data integration
* ✔ Feature scaling

---

## 📈 Soil Health Index (SHI)

A custom composite score:

| Feature        | Weight |
| -------------- | ------ |
| Organic Carbon | 30%    |
| NDVI           | 25%    |
| Soil pH        | 20%    |
| Humidity       | 15%    |
| Rainfall       | 10%    |

📊 Output:

* **0 → Poor**
* **1 → Healthy**

---

## 🤖 Models Implemented (8 Models)

* LSTM
* GRU
* BiLSTM
* CNN-LSTM ⭐ (Best Model)
* TCN
* Transformer
* CNN-Transformer
* Attention-LSTM

---

## 🏆 Model Performance

| Model          | R²     | Accuracy |
| -------------- | ------ | -------- |
| CNN-LSTM ⭐     | 0.9609 | 89.39%   |
| LSTM           | 0.9576 | 87.58%   |
| Attention-LSTM | 0.9572 | 89.39%   |

📌 **Why CNN-LSTM performs best?**

* CNN → captures local patterns
* LSTM → captures temporal dependencies

---

## 📊 Outputs & Features

### 🌟 Soil Health Analysis

* Soil Health Index (SHI) score
* Classification:

  * 🔴 Poor
  * 🟡 Moderate
  * ✨ Healthy
* Interactive gauge visualization

---

### 🌿 NDVI Time-Series

* 8-step NDVI trend graph
* Vegetation health visualization

---

### 🗺️ Geospatial Visualization

* Interactive map using latitude & longitude
* Soil location visualization

---

### 🌾 Crop Recommendations

* Ranked crop suggestions
* Suitability score (%)
* Issue identification

---

### 🧪 Fertilizer Recommendations

* Nutrient-based suggestions
* Soil improvement guidance

---

### 💧 Irrigation Advisory

* Irrigation level
* Watering frequency
* Smart usage advice

---

### 🖼️ Image-Based Analysis

* Upload soil/crop image
* Outputs:

  * Soil type
  * Disease detection
  * AI explanation

---

### 📄 PDF Report Generation

* Downloadable full report including:

  * SHI score
  * Crop recommendations
  * Fertilizer advice
  * Irrigation plan
  * Image insights

---

### 🎨 Interactive Dashboard

* Built using **Gradio + Custom CSS**
* Features:

  * Modern UI
  * Interactive plots
  * Real-time outputs

---

## 💻 Tech Stack

* Python
* TensorFlow / Keras
* PyTorch
* Scikit-learn
* Plotly
* Folium
* Gradio
* Google Earth Engine
* Open-Meteo API

---

## ▶️ How to Run

```bash id="run1"
git clone https://github.com/YOUR_USERNAME/AI-Soil-Health-Prediction.git
cd AI-Soil-Health-Prediction
pip install -r requirements.txt
python app.py
```

---

## 📸 Demo

*Add screenshots here*

```id="img1"
/assets/ui.png
/assets/results.png
/assets/graphs.png
```

---

## 🔮 Future Work

* 🌍 Real-time satellite NDVI integration
* 📱 Web/mobile deployment
* 🌾 Crop + irrigation automation
* 🤖 Full multimodal fusion (single model)

---

## 👩‍💻 Author

**Pranathi**

---

## ⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
📢 Share it

---

<p align="center">
  🌱 <b>AI for Sustainable Agriculture</b> 🌍
</p>
