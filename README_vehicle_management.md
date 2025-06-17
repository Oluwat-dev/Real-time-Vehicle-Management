
# Real-Time Vehicle Management System

This project is a full-stack application for real-time vehicle monitoring and analytics using YOLOv8 for object detection and OCR for license plate recognition. It features a Flask backend, Dash-based frontend, and robust detection modules for live traffic analysis.

---

## 🧩 Project Structure

```
Real-time vehicle management/
│
├── backend/
│   ├── app.py                 # Flask application
│   ├── models.py              # Database models and ORM
│   ├── routes.py              # API routes
│   ├── database.py            # Database connection and initialization
│   ├── analytics.py           # Data analytics functions
│   └── requirements.txt       # Python package dependencies
│
├── frontend/
│   ├── app.py                 # Dash application
│   ├── layout.py              # Layout and UI components
│   ├── callbacks.py           # Callback functions for interactivity
│   └── assets/
│       └── styles.css         # CSS for styling
│
├── detection/
│   ├── detection.py           # YOLOv8 vehicle detection script
│   ├── ocr.py                 # License plate recognition script
│   └── requirements.txt       # Dependencies for detection
│
├── reports/                   # Exported reports
├── tests/                     # Unit tests
└── README.md                  # Documentation
```

---

## 🚀 Features

- **Real-time Vehicle Detection** using YOLOv8
- **License Plate Recognition** via OCR
- **RESTful API** with Flask for backend processing
- **Interactive Dashboard** built with Plotly Dash
- **Data Analytics** and exportable reports
- **Modular Codebase** for easy maintenance and scaling

---

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy
- **Frontend:** Dash (Plotly), CSS
- **Detection:** YOLOv8, OpenCV, Tesseract OCR
- **Database:** SQLite / PostgreSQL (configurable)
- **Others:** Pandas, Numpy, Gunicorn, Docker (optional)

---

## 🧪 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/vehicle-management.git
cd vehicle-management
```

2. **Set up the backend**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

3. **Set up the frontend**

```bash
cd ../frontend
pip install dash
python app.py
```

4. **Set up the detection module**

```bash
cd ../detection
pip install -r requirements.txt
python detection.py
```

---

## 📂 Reports

All generated vehicle data and analytics can be exported and found in the `reports/` folder.

---

## ✅ Testing

```bash
cd tests
pytest
```

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Oluwatobi Aluko — [Portfolio](https://oluwat.dev) | [LinkedIn](https://linkedin.com/in/aluko-oluwatobi-a2536823a)
