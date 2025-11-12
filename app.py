import streamlit as st
from engine import analyze_text, analyze_twitter, analyze_batch
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sentiment Analysis", layout="wide", initial_sidebar_state="expanded")

# === SIDEBAR ===
with st.sidebar:
    st.title("Sentiment Analysis")
    dark = st.checkbox("Dark Mode 🌙", True)

# === GLOBAL THEME ===
if dark:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {background-color: #0e1117; color: #fafafa;}
        [data-testid="stSidebar"] {background-color: #161a1f;}
        .stButton>button {background-color: #ff4b4b; color: white; border: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

template = "plotly_dark" if dark else "plotly_white"

# === TABS ===
tab1, tab2, tab3 = st.tabs(["📝 Text", "🐦 Twitter", "📁 CSV Batch"])

# === TEXT TAB ===
with tab1:
    st.header("🔍 Single Text Analysis")
    txt = st.text_area("Paste your text below:", height=120)
    if st.button("Analyze Text", type="primary") and txt:
        res = analyze_text(txt)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res["sentiment"]["score"] * 100,
            title={'text': res["sentiment"]["label"]},
            gauge={'bar': {'color': res["sentiment"]["color"]}}
        ))
        fig.update_layout(template=template)
        st.plotly_chart(fig, use_container_width=True)
        st.write("**Detected Aspects:**", ", ".join(res["aspects"]))

# === TWITTER TAB ===
with tab2:
    st.header("🐦 Twitter Sentiment (Demo)")
    q = st.text_input("Search keyword or username", "@elonmusk")
    lim = st.selectbox("Number of Tweets", [5, 10, 15, 20])
    if st.button("Fetch Tweets") and q:
        data = analyze_twitter(q, lim)
        st.metric("Tweets Analyzed", data["tweets_analyzed"])
        st.metric("Dominant Sentiment", data["overall_sentiment"])
        fig = go.Figure(go.Pie(
            labels=list(data["sentiment_breakdown"].keys()),
            values=list(data["sentiment_breakdown"].values()),
            hole=0.4
        ))
        fig.update_layout(template=template)
        st.plotly_chart(fig, use_container_width=True)
        for t in data["tweets"]:
            r = analyze_text(t["text"])
            with st.expander(t["text"][:80] + "..."):
                st.write(f"**Sentiment:** {r['sentiment']['label']}")
                st.write(f"**Aspects:** {', '.join(r['aspects'])}")

# === CSV TAB ===
with tab3:
    st.header("📊 CSV Batch Sentiment Analysis")

    # --- SAMPLE CSV ---
    sample = '''text
"The food was amazing, but the service was slow."
"I love the camera quality!"
"Terrible support, never again."
"It's okay."
"Battery dies fast."
"Great value!"
"Worst purchase ever."'''
    st.download_button("📥 Download Sample CSV", sample, "sample_reviews.csv", "text/csv")

    uploaded = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded:
        try:
            content = uploaded.getvalue().decode("utf-8-sig")
            lines = content.strip().split('\n')
            texts = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('"') and line.endswith('"'):
                    texts.append(line[1:-1])
                else:
                    parts = [p.strip() for p in line.split(',')]
                    texts.append(', '.join([p for p in parts if p]))

            if lines and lines[0].strip().lower() in ['text', 'review', 'comment', 'sentence']:
                texts = texts[1:]

            texts = [t for t in texts if t and len(t) > 3]

            if not texts:
                st.warning("⚠️ No valid text found. Try the sample CSV.")
            else:
                with st.spinner(f"Analyzing {len(texts)} reviews..."):
                    results = analyze_batch(texts)

                # --- PIE CHART ---
                sentiments = [r["sentiment"]["label"] for r in results]
                counts = Counter(sentiments)
                fig = go.Figure(go.Pie(
                    labels=list(counts.keys()),
                    values=list(counts.values()),
                    hole=0.4,
                    marker_colors=["darkblue", "blue", "gray", "red", "darkred"]
                ))
                fig.update_layout(template=template)
                st.plotly_chart(fig, use_container_width=True)

                # --- TABLE ---
                st.subheader("🧾 Sentence-Level Sentiment Results")
                table_data = [{"Sentence": r["text"], "Sentiment": r["sentiment"]["label"]} for r in results]
                df = pd.DataFrame(table_data)

                # Highlight Sentiment Function
                def highlight_sentiment(val):
                    color = {
                        "Very Positive": "background-color: #0047AB; color: white;",
                        "Positive": "background-color: #6495ED; color: white;",
                        "Neutral": "background-color: #808080; color: white;",
                        "Negative": "background-color: #FF6347; color: white;",
                        "Very Negative": "background-color: #8B0000; color: white;",
                    }
                    return color.get(val, "")

                styled_df = df.style.applymap(highlight_sentiment, subset=["Sentiment"])
                st.dataframe(styled_df, use_container_width=True)

                # --- DONE MESSAGE ---
                st.success("✅ Analysis Complete!")
                st.balloons()

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Try the sample CSV – it works!")


