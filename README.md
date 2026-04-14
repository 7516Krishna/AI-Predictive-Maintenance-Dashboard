# 🏭 AI-Powered Predictive Maintenance Dashboard

An interactive AI-driven dashboard that analyzes industrial IoT sensor data to predict equipment failures using machine learning.

---

## 🚀 Project Overview

This project simulates a real-world **predictive maintenance system** used in industries to monitor machine health and detect potential failures before they occur.

It integrates:
- 📡 IoT sensor data simulation (NASA dataset)
- 🤖 Machine Learning for failure prediction
- 📊 Interactive dashboards (Power BI / Tableau style)
- 💬 AI chat assistant for data insights

---

## 🎯 Key Features

- 📂 Upload CSV or NASA Turbofan Dataset (`.txt`)
- 📊 Real-time interactive dashboards
- 📈 Sensor trend visualization (interactive)
- 📊 Data distribution analysis
- 🔗 Correlation heatmap
- 🚨 Failure prediction insights
- 💬 AI-powered chat assistant
- 🎯 Clean white professional UI

---

## 🧠 Machine Learning

- Model: Random Forest Classifier
- Task: Binary Classification (Failure / No Failure)
- Feature Engineering:
  - Temperature
  - Vibration
  - Pressure
  - Flow Rate
  - Efficiency
- Label Creation using Remaining Useful Life (RUL)

---

## 📊 Dataset

- Source: NASA Turbofan Engine Degradation Dataset (C-MAPSS)
- File Used: `train_FD001.txt`

---

## 🖼️ Dashboard Preview

### 🏠 Main Dashboard
![Dashboard](assets/dashboard_overview.png)

### 📈 Sensor Trends
![Trends](assets/sensor_trends_plot.png)

### 📊 Distribution
![Distribution](assets/sensor_distribution.png)

### 🔗 Correlation Heatmap
![Heatmap](assets/correlation_heatmap.png)

### 🚨 Failure Analysis
![Failure](assets/failure_analysis.png)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly (Interactive Charts)

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/AI-Predictive-Maintenance-Dashboard.git
cd AI-Predictive-Maintenance-Dashboard

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt