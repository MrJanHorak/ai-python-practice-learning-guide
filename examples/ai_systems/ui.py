"""Optional local interface: python -m streamlit run examples/ai_systems/ui.py"""
import json
import sys
import uuid
from pathlib import Path

# Streamlit executes this as a script; expose the repo for absolute imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import streamlit as st
from examples.ai_systems.core import DATA, ROOT, TOOLS, ReviewStore, ToolContext, customers, read_json, validate_extraction
from examples.ai_systems.providers import Conversation, MockConversation, run_agent

st.set_page_config(page_title="AI systems practice lab")
st.title("Synthetic onboarding review lab")
st.caption("Fictional training data and rules. Mock is scripted; live provider choices send the prompt and tool results to that service.")

fixtures = read_json(DATA / "extraction_fixtures.json")
selected = st.selectbox("Extraction fixture", [x["document_id"] for x in fixtures])
fixture = next(x for x in fixtures if x["document_id"] == selected)
with st.expander("Inspect extraction and validation", expanded=True):
    st.json(fixture)
    st.json(validate_extraction(fixture))

with st.form("agent"):
    provider = st.selectbox("Provider", ["mock", "openai", "anthropic", "gemini", "ollama", "local-openai"])
    prompt = st.text_input("Request", "What is the risk tier for C-1002?")
    request_id = st.text_input("Request ID (keep for identical retries)", "ui-demo-001")
    allowed = st.checkbox("Authorize this request to create one pending LOCAL review", value=False)
    write_customer = st.selectbox("Customer authorized for this write", list(customers()))
    submit = st.form_submit_button("Run request")
if submit:
    store = ReviewStore(ROOT / "output/reviews.sqlite3")
    try:
        with st.spinner("Running request..."):
            context = ToolContext(store, request_id or str(uuid.uuid4()), allowed, write_customer)
            conversation = MockConversation(prompt) if provider == "mock" else Conversation(provider, prompt)
            result = run_agent(conversation, context, TOOLS)
        st.write(result["text"])
        st.json(result)
    except Exception as error:
        # Show class only: SDK/server error strings can contain private details.
        st.error(f"Request failed ({type(error).__name__}). Check local configuration and lesson 09.")
    finally:
        store.close()

store = ReviewStore(ROOT / "output/reviews.sqlite3")
try:
    st.subheader("Persistent review queue")
    st.dataframe(store.list())
    st.caption("Use the CLI review command for a named human decision. This UI is a single-user local exercise without authentication.")
finally:
    store.close()
