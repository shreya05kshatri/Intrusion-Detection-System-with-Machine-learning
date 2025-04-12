# Intrusion-Detection-System-with-Machine-learning
This project is to design and implement a machine learning-based Intrusion Detection System using the Random Forest algorithm to accurately identify and classify network threats. This involves utilizing the NSL-KDD dataset for training, where raw network traffic data is preprocessed, and label-encoded to ensure compatibility with the model.

# 🛡️ Intrusion Detection System (IDS) with Flask & Random Forest

This project is a lightweight Intrusion Detection System (IDS) built using Python, Flask, and a Random Forest classifier. It uses the NSL-KDD dataset for training and allows real-time traffic analysis through a web interface and an API.

---

## 🚀 Features

- Detects normal and malicious network activity using ML
- Real-time monitoring and live UI updates
- Web interface for manual traffic input
- REST API for automated input (e.g., packet sniffer)
- Styled dark-mode frontend with basic animations

---

## 🧰 Tech Stack

- Python, Flask
- Scikit-learn (Random Forest)
- HTML/CSS (dark themed)
- JavaScript (SSE for live stream)
- NSL-KDD Dataset

---
## ⚙️ Setup Instructions

### 1. Clone the Repository

### 2. Create and Activate Virtual Environment
``` python -m venv .venv
.\.venv\Scripts\activate  # Windows
```
### 3. Install Library 
```
pip install flask numpy pandas scikit-learn joblib
```
### 4. Train the Model
```
from sklearn.ensemble import RandomForestClassifier
import joblib

# Assume X_train, y_train already preprocessed
model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'models/random_forest_ids_model.pkl')
joblib.dump(encoders, 'models/label_encoders.pkl')
```
### 5. Run the App
```
python app.py
```
### 6. Start packet sniffing
```
python realtime_sniffer.py
```

## Screenshot 
Detection Module
![image (1)](https://github.com/user-attachments/assets/e2fa33d4-7476-4c32-b1d7-395cf2af0882)

Live Detecting 
![image](https://github.com/user-attachments/assets/652a8040-eb98-4ec8-8ac3-251096af98cf)













