# 🚀 Resume & Portfolio Builder

A lightweight, AI-free Streamlit web app that generates professional **DOCX**, **PDF**, and **HTML portfolio** files from your personal details.

---

## 📁 Project Structure

```
resume_portfolio_builder/
├── app.py                        # Main Streamlit app
├── requirements.txt              # Dependencies
├── generators/
│   ├── __init__.py
│   ├── summary_generator.py      # Rule-based summary generator
│   ├── docx_generator.py         # python-docx DOCX builder
│   ├── pdf_generator.py          # ReportLab PDF builder
│   └── html_generator.py         # Standalone HTML portfolio
```

---

## ⚙️ Local Setup

### 1. Clone / copy the project folder

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud

1. Push the project folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** → `app.py`
5. Click **Deploy** — done!

> Streamlit Cloud automatically installs packages from `requirements.txt`.

---

## 📦 Generated Outputs

| File | Format | Description |
|------|--------|-------------|
| `Name_Resume.docx` | DOCX | Formatted Word document resume |
| `Name_Resume.pdf`  | PDF  | Clean PDF resume (ReportLab) |
| `Name_Portfolio.html` | HTML | Standalone dark-theme portfolio site |

---

## 🛠 Tech Stack

- **Frontend & Backend**: Streamlit (Python)
- **DOCX Generation**: `python-docx`
- **PDF Generation**: `reportlab`
- **Portfolio**: Pure HTML/CSS (no framework, no CDN required for core features)
- **Summary**: Rule-based NLP (no AI API)

---

## ✨ Features

- Zero API dependencies — fully offline capable
- Instant file generation and download
- Professional dark-theme portfolio HTML
- Rule-based smart summary generator
- Streamlit Cloud compatible
