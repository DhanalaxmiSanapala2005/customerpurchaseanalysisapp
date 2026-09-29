# Customer Purchase Analysis (Streamlit)

Interactive dashboard with filters, KPIs and charts.

## Run locally
```bash
python -m venv venv
# Windows:  venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501

## Deploy to Streamlit Cloud
1. Push this folder to a GitHub repo (app.py, data.csv, requirements.txt).
2. Go to https://share.streamlit.io and log in with GitHub.
3. Click "Create app" -> select repo, branch, and main file `app.py`.
4. Click Deploy -> you get a public URL.

## Files
- `app.py` – Streamlit app
- `data.csv` – dataset (100 customers)
- `generate_data.py` – regenerates the dataset
- `requirements.txt` – dependencies
