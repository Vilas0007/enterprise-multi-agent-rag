import streamlit as st

from frontend.services.api_client import APIClient, APIClientError


def render() -> None:
    """Render the employee chat interface."""

    st.title("Enterprise AI Assistant")

    st.caption("Ask questions about company documents and policies.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    # Display earlier messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask your company-related question...")

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

            with st.chat_message("assistant"), st.spinner(
                "Processing your question..."
            ):
                try:
                    client = APIClient()

                    result = client.ask_question(
                        question=question,
                        conversation_id=st.session_state.conversation_id,
                    )

                    answer = result.get("answer")

                    if not isinstance(answer, str) or not answer.strip():
                        raise APIClientError(
                            "Backend returned an empty or invalid answer."
                        )

                    st.markdown(answer)

                    conversation_id = result.get("conversation_id")

                    if isinstance(conversation_id, str):
                        st.session_state.conversation_id = conversation_id

                    citations = result.get("citations", [])

                    if isinstance(citations, list) and citations:
                        with st.expander("View sources"):
                            for citation in citations:
                                st.write(citation)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except APIClientError as exc:
                    error_message = str(exc)
                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": f"Request failed: {error_message}",
                        }
                    )




 