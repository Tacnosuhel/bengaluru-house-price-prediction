# Bengaluru House Price Predictor 🏡

A full-stack machine learning web application to estimate Bengaluru real estate prices using Linear Regression, FastAPI, and Streamlit.

## Features
- **Model**: Linear Regression trained on cleaned area, bedroom, and location features.
- **Backend API**: High-performance FastAPI server serving `/user` inference.
- **Frontend**: Interactive Streamlit web interface with dynamic input controls.

## Project Structure
```text
├── Backend/
│   ├── app/
│   │   └── main.py
│   └── model/
│       ├── columns.json
│       ├── models.pickle
│       └── bhp.ipynb
├── frontend/
│   └── app.py
├── pyproject.toml
└── requirements.txt

Local Setup & Run
Clone the repository:

Bash
git clone [https://github.com/](https://github.com/)<your-username>/bengaluru-house-price-prediction.git
cd bengaluru-house-price-prediction
Set up virtual environment:

Bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
Start the FastAPI backend:

Bash
uvicorn Backend.app.main:app --reload --port 8000
Start the Streamlit frontend (in a separate terminal):

Bash
streamlit run frontend/app.py