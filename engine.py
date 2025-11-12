# engine.py
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from collections import Counter
import random

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(c):
    if c <= -0.6: return "Very Negative", "darkred"
    if c <= -0.2: return "Negative", "red"
    if c < 0.2:   return "Neutral", "gray"
    if c < 0.6:   return "Positive", "blue"
    return "Very Positive", "darkblue"

def extract_aspects(text):
    try:
        blob = TextBlob(str(text).lower())
        aspects = []
        for i, (w, t) in enumerate(blob.tags):
            if t in ['NN', 'NNS', 'NNP']:
                if i > 0 and blob.tags[i-1][1] in ['JJ', 'JJR', 'JJS']:
                    aspects.append(f"{blob.tags[i-1][0]} {w}")
                else:
                    aspects.append(w)
        aspects = [a for a in aspects if len(a) > 2 and a not in ["thing","one","item"]]
        return list(set(aspects))[:4] or ["general"]
    except:
        return ["general"]

def analyze_text(text):
    if not text or not str(text).strip():
        return {"sentiment": {"label":"Neutral","color":"gray","score":0}, "aspects":["general"]}
    s = analyzer.polarity_scores(str(text))
    label, color = get_sentiment(s['compound'])
    return {
        "sentiment": {"label": label, "color": color, "score": abs(s['compound'])},
        "aspects": extract_aspects(text)
    }

MOCK_TWEETS = [
    {"text": "Tesla FSD is mind-blowing!", "likes": 3200},
    {"text": "AI will change humanity.", "likes": 2800},
    {"text": "Starship launch perfect!", "likes": 5000},
    {"text": "Traffic is awful.", "likes": 900},
    {"text": "Neuralink success!", "likes": 4200},
] * 20
random.shuffle(MOCK_TWEETS)

def analyze_twitter(q, lim=12):
    tweets = random.sample(MOCK_TWEETS, min(lim * 3, len(MOCK_TWEETS)))
    # Deduplicate by text content
    unique_texts = list({t["text"]: t for t in tweets}.values())[:lim]

    res = [analyze_text(t["text"]) for t in unique_texts]
    lbl = [r["sentiment"]["label"] for r in res]
    cnt = Counter(lbl)
    return {
        "tweets_analyzed": len(unique_texts),
        "overall_sentiment": cnt.most_common(1)[0][0] if cnt else "Neutral",
        "sentiment_breakdown": dict(cnt),
        "tweets": unique_texts
    }

# THIS FUNCTION WAS MISSING IN YOUR IMPORT
def analyze_batch(texts):
    results = []
    for t in texts:
        if t and str(t).strip():
            analysis = analyze_text(t)
            analysis["text"] = t  # ✅ Include original text for display
            results.append(analysis)
    return results
