import streamlit as st
from article_recommendation import get_recommendations

st.set_page_config(page_title="News Engine", layout="wide")

st.title("🧠 News Article Engine")
st.write("Search news.......")

query = st.text_input("Enter author name, topic, or headline idea", placeholder="e.g. Elyse Wanshel or climate change")
top_n = 10

if st.button("Recommend") and query.strip():
    with st.spinner("Searching..."):
        results = get_recommendations(query, top_n)

    if results:
        for r in results:
            st.markdown(f"### {r['headline']}")
            st.markdown(f"**Category:** {r['category']} | **Author:** {r['authors']}")
            st.markdown(r['description'])
            st.markdown(f"[Read more]({r['link']})")
            st.markdown("---")
    else:
        st.warning("No results found.")
