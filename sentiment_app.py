import streamlit as st
import openai
import requests

# Load API keys from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]
news_api_key = st.secrets["newsapi"]["api_key"]

# Streamlit UI setup
st.set_page_config(page_title="Sentivault", page_icon="📈")
st.title("📈 Sentivault: Market Sentiment Analyzer")

# User input
query = st.text_input("Enter a company, asset, or keyword")

# Button to trigger analysis
if st.button("Analyze Sentiment") and query.strip():
    st.info("🔍 Fetching news headlines...")

    # Step 1: Fetch news headlines
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={news_api_key}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles if article.get("title")]

    if not headlines:
        st.warning("No headlines found. Try a different keyword.")
    else:
        # Step 2: Analyze sentiment using GPT
        st.info("🧠 Analyzing sentiment...")
        results = []
        for headline in headlines:
            try:
                gpt_response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Classify this news headline as Positive, Negative, or Neutral."},
                        {"role": "user", "content": headline}
                    ]
                )
                sentiment = gpt_response.choices[0].message.content.strip()
                results.append((headline, sentiment))
            except Exception as e:
                results.append((headline, f"Error: {e}"))

        # Step 3: Display results
        st.markdown("### 🧾 Sentiment Results")
        for headline, sentiment in results:
            st.write(f"**{sentiment}** — {headline}")
