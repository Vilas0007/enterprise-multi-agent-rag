import logging

import streamlit as st

from frontend.pages.admin_dashboard import render as admin_page
from frontend.pages.chat import render as chat_page
from frontend.pages.document_upload import render as upload_page

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Enterprise Agentic RAG frontend."""

    # Configure Streamlit page settings
    st.set_page_config(
        page_title="Enterprise Agentic RAG",
        page_icon="🤖",
        layout="wide",
    )

    logger.info("Starting Streamlit frontend")

    # Define application pages
    pages = [
        st.Page(
            chat_page,
            title="AI Assistant",
            icon=":material/chat:",
            url_path="ai-assistant",
            default=True,
        ),
        st.Page(
            upload_page,
            title="Document Upload",
            icon=":material/upload_file:",
            url_path="document-upload",
        ),
        st.Page(
            admin_page,
            title="Admin Dashboard",
            icon=":material/dashboard:",
            url_path="admin-dashboard",
        ),
    ]

    # Create navigation menu
    navigation = st.navigation(pages)

    # Run selected page
    navigation.run()


if __name__ == "__main__":
    main()
