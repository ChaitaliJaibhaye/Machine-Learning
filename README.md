# 💬 Sentiment Pro — AI-Powered Sentiment Analyzer

**Sentiment Pro** is a Streamlit-based web application that performs **sentiment analysis** on text, tweets, or uploaded CSV files.  
It uses **TextBlob** and **VADER** to classify text into five categories:
> _Very Positive, Positive, Neutral, Negative, Very Negative_

---

## 🚀 Features

✅ **Single Text Analysis** — Paste a sentence or paragraph and instantly view:
- Sentiment score gauge
- Extracted aspects (like *food*, *service*, etc.)

✅ **Twitter (Mock) Analysis** — Analyze a set of sample tweets about a topic:
- Sentiment distribution pie chart
- Tweet-level breakdown

✅ **CSV Batch Analysis** — Upload a CSV of reviews or comments:
- Automated sentiment tagging
- Interactive pie chart + color-coded table
- Optional sample CSV download

✅ **Modern UI**
- Dark/Light theme toggle  
- Animated feedback (`st.balloons()` 🎈 & success notifications ✅)  
- Styled DataFrame with sentiment-based highlighting  

---

## 🧠 Tech Stack

| Tool | Purpose |
|------|----------|
| **Python 3.11+** | Programming language |
| **Streamlit** | Web UI framework |
| **TextBlob** | NLP processing |
| **VADER Sentiment** | Sentiment scoring |
| **Plotly** | Interactive charts |
| **Pandas** | Data handling |
| **NLTK** | Tokenization & tagging |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/sentiment-pro.git
cd sentiment-pro
