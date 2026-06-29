import os
import requests
import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="TDS Virtual TA",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Backend URL
# -----------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000")

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/chatbot.png",
        width=80
    )

    st.title("TDS Virtual TA")

    st.caption(
        "Retrieval-Augmented AI Assistant for IIT Madras TDS"
    )

    st.divider()

    st.subheader("🧠 Tech Stack")

    st.markdown("""
- ⚡ FastAPI
- 🎨 Streamlit
- 🧠 GPT-4o-mini
- 📦 SQLite
- 🔍 Vector Search
""")

    st.divider()

    try:

        health = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if health.status_code == 200:

            data = health.json()

            st.success("Backend Online")

            st.metric(
                "Discourse Chunks",
                data["discourse_chunks"]
            )

            st.metric(
                "Markdown Chunks",
                data["markdown_chunks"]
            )

        else:

            st.error("Backend Offline")

    except:

        st.error("Backend Offline")

    st.divider()

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages=[]

        st.rerun()

# -----------------------------
# Main Title
# -----------------------------
st.title("🎓 TDS Virtual Teaching Assistant")

st.caption("Ask anything about the IITM TDS course.")
if len(st.session_state.messages)==0:

    st.info(
        """
👋 Welcome!

Try asking questions like:

• What is Gradient Descent?

• Explain GitHub

• Difference between SGD and Batch Gradient Descent

• What is Linear Regression?

• Explain Cosine Similarity
"""
    )

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg.get("links"):

            st.markdown("### 📚 Sources")

            for link in msg["links"]:

                st.markdown(
                    f"- [{link['text']}]({link['url']})"
                )

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": prompt
                    },
                    timeout=120
                )

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer returned."
                )

                links = data.get(
                    "links",
                    []
                )

                st.markdown(answer)

                if links:

                    st.markdown("### 📚 Sources")

                    for link in links:

                        st.markdown(
                            f"- [{link['text']}]({link['url']})"
                        )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "links": links
                    }
                )

            except Exception as e:

                st.error(f"Error: {e}")
                
                
st.divider()

st.caption(
"""
Built with ❤️ by Samarth

FastAPI • Streamlit • SQLite • AI Pipe
"""
)                