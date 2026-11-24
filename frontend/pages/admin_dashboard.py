import streamlit as st

from frontend.services.api_client import APIClient, APIClientError


def render() -> None:
    """Render the initial administrator diagnostics page."""

    st.title("Administrator Dashboard")

    st.write("Backend connectivity and application diagnostics.")

    if st.button("Check Backend Health"):
        try:
            client = APIClient()
            result = client.health_check()

            st.success("Backend is responding.")
            st.json(result)

        except APIClientError as exc:
            st.error(str(exc))

    st.info(
        "Document statistics, user management, permissions, and audit "
        "reports will be integrated after the corresponding backend "
        "components are implemented."
    )
