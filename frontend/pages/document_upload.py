import streamlit as st

from frontend.config import MAX_UPLOAD_SIZE_MB
from frontend.services.api_client import APIClient, APIClientError


def render() -> None:
    """Render the company document upload interface."""

    st.title("Document Upload")

    st.write("Upload company documents for the knowledge base.")

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx", "csv"],
    )

    if uploaded_file is None:
        st.info("Select a PDF, DOCX, or CSV document.")
        return

    file_size_mb = uploaded_file.size / (1024 * 1024)

    st.write(f"Selected file: {uploaded_file.name}")
    st.write(f"File size: {file_size_mb:.2f} MB")

    if file_size_mb > MAX_UPLOAD_SIZE_MB:
        st.error(f"File exceeds the {MAX_UPLOAD_SIZE_MB} MB upload limit.")
        return

    if st.button("Upload Document", type="primary"):
        try:
            client = APIClient()

            result = client.upload_document(
                filename=uploaded_file.name,
                file_content=uploaded_file.getvalue(),
            )

            st.success("Document uploaded successfully.")

            st.json(result)

        except APIClientError as exc:
            st.error(str(exc))
