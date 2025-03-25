import streamlit as st
from article_recommendation import get_recommendations

# Page config
st.set_page_config(page_title="🧠 NeuroScoop Engine", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        h1, h2, h4 {
            color: #2c3e50;
        }
        .article-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.08);
            margin-bottom: 1rem;
        }
        .read-more a {
            font-weight: bold;
            color: #007bff;
        }
    </style>
""", unsafe_allow_html=True)

# Title and subheader
st.title("🧠 NeuroScoop Engine")
st.markdown("### 🔎 Discover articles tailored to your ideas or interests")
st.caption("Type in a topic, headline, or author — and receive semantically similar news recommendations.")
st.markdown("### 📝 Search")

# 🧩 Input and aligned button
col1, col2 = st.columns([6, 1])
with col1:
    query = st.text_input("Enter author name, topic, or headline idea", placeholder="e.g. Elyse Wanshel or climate change", label_visibility="collapsed")
with col2:
    recommend_clicked = st.button("🔍 Search")

# 🔍 Recommendations
top_n = 10
if recommend_clicked and query.strip():
    with st.spinner("Searching for similar articles..."):
        results = get_recommendations(query, top_n)

    if results:
        st.markdown("## ✨ Recommended Articles")
        for r in results:
            with st.container():
                st.markdown(f"""
                    <div class='article-card'>
                        <h4>📰 {r['headline']}</h4>
                        <p><strong>📚 Category:</strong> {r['category']} &nbsp;&nbsp; | &nbsp;&nbsp; <strong>✍️ Author:</strong> {r['authors']}</p>
                        <p>{r['description']}</p>
                        <p class='read-more'><a href="{r['link']}" target="_blank">Read more ➜</a></p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No results found. Try a different topic or author.")
