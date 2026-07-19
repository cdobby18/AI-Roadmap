"""Poneglyph Reader — Streamlit chat UI for the One Piece RAG system.

Run with:  streamlit run app.py

The UI is organized into:
- Sidebar: data management (scrape, index, stats, filters)
- Main panel: chat interface with conversation history
"""

import streamlit as st

from config import SEED_PAGES
from scraper import scrape_pages, list_cached_pages
from ingestion import index_documents, collection_stats, clear_collection
from rag import ask


# -------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Poneglyph Reader",
    page_icon="📜",
    layout="wide",
)

st.title("📜 Poneglyph Reader")
st.markdown("Chat with the One Piece wiki — ask about characters, Devil Fruits, arcs, and more.")


# -------------------------------------------------------------------
# Sidebar — data management
# -------------------------------------------------------------------

with st.sidebar:
    st.header("🏴‍☠️ Data Sources")

    stats = collection_stats()
    st.metric("Indexed Chunks", stats["count"])
    if stats["sources"]:
        with st.expander(f"Sources ({stats['source_count']})"):
            for s in stats["sources"]:
                st.caption(s[:60])

    st.divider()

    # Scrape & index controls
    st.subheader("Scrape Wiki Pages")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Scrape + Index", type="primary", use_container_width=True):
            with st.spinner("Scraping wiki pages..."):
                docs = scrape_pages()
            if docs:
                with st.spinner("Indexing into ChromaDB..."):
                    n = index_documents(docs)
                st.success(f"Indexed {n} chunks from {len(docs)} pages")
                st.rerun()
            else:
                st.warning("No pages scraped. Check Ollama/wiki access.")

    with col2:
        if st.button("Clear All", use_container_width=True):
            clear_collection()
            st.rerun()

    cached = list_cached_pages()
    if cached:
        with st.expander(f"Cached Pages ({len(cached)})"):
            for page in cached[:20]:
                st.caption(page)
            if len(cached) > 20:
                st.caption(f"... and {len(cached) - 20} more")

    st.divider()

    # Settings
    st.subheader("⚙️ Settings")
    use_reranker = st.toggle("Use Reranker", value=True, help="Cross-encoder reranking for better precision")

    category_options = {
        "All": None,
        "Characters": "character",
        "Devil Fruits": "devil_fruit",
        "Abilities": "ability",
        "Locations": "location",
    }
    selected_category = st.selectbox(
        "Filter by category",
        options=list(category_options.keys()),
        index=0,
    )
    category_filter = category_options[selected_category]

    st.divider()
    st.caption("Built on Phase 6 — Retrieval-Augmented Generation")
    st.caption("Uses ChromaDB + sentence-transformers + Ollama")


# -------------------------------------------------------------------
# Main panel — chat interface
# -------------------------------------------------------------------

def init_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []


def display_chunk(chunk, i: int):
    """Display a retrieved chunk in an expandable card."""
    text, source, score = chunk
    with st.expander(f"Source {i+1} — Score: {score:.3f}"):
        st.caption(f"📄 {source}")
        st.text(text[:300] + ("..." if len(text) > 300 else ""))


init_chat()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            for i, chunk_data in enumerate(msg.get("chunks", [])):
                display_chunk(chunk_data, i)
        if "source_urls" in msg and msg["source_urls"]:
            st.divider()
            st.caption("Sources:")
            for url in msg["source_urls"]:
                st.caption(f"🔗 [{url.split(' (')[-1].rstrip(')')}]({url.split(' (')[-1].rstrip(')')})" if "(" in url else f"🔗 {url}")

# Chat input
if prompt := st.chat_input("Ask about One Piece..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Reading the Poneglyphs..."):
            result = ask(
                prompt,
                history=st.session_state.history if st.session_state.history else None,
                category_filter=category_filter,
                use_reranker=use_reranker,
            )

        st.markdown(result["answer"])

        # Show sources
        if result["chunks"]:
            st.divider()
            st.caption(f"📚 Retrieved from {len(result['sources'])} sources")
            for i, chunk_data in enumerate(result["chunks"]):
                display_chunk(chunk_data, i)

        # Store in history
        msg_entry = {
            "role": "assistant",
            "content": result["answer"],
            "chunks": result["chunks"],
            "source_urls": result["sources"],
        }
        st.session_state.messages.append(msg_entry)

    # Update conversation history for query rewriting
    st.session_state.history.append(prompt)
    st.session_state.history.append(result["answer"])

    # Keep only last 10 turns to avoid context overflow
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[-20:]
