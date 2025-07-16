import streamlit as st
from view.styling import CHAT_STYLES
from .logging_config import logger


def configure_streamlit() -> None:
    logger.info("Configuring Streamlit page settings")
    st.set_page_config(layout="wide", page_title="ADK Chat UI")
    st.markdown(CHAT_STYLES, unsafe_allow_html=True)
    logger.info("Streamlit configuration completed")
