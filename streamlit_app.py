import streamlit as st
import requests


API_URL = "https://aylin-ai-loan-assistant.onrender.com"


st.set_page_config(
    page_title="Aylin AI Loan Assistant",
    page_icon="🤖",
    layout="centered",
)


st.title("Aylin AI Loan Assistant")
st.caption("AI-powered loan application assistant")


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "application_id" not in st.session_state:
    st.session_state.application_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------------------------------
# CUSTOMER PHONE
# ------------------------------------------------------------

phone = st.text_input(
    "Customer phone number",
    value=st.session_state.phone,
    placeholder="996555123456",
)

st.session_state.phone = phone.strip()


# ------------------------------------------------------------
# CONVERSATION HISTORY
# ------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------

user_message = st.chat_input(
    "Введите сообщение клиента..."
)


if user_message:

    if not st.session_state.phone:
        st.error("Введите номер телефона клиента.")
        st.stop()


    # Show customer message immediately

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    with st.chat_message("user"):
        st.write(user_message)


    # --------------------------------------------------------
    # SEND TO AYLIN API
    # --------------------------------------------------------

    payload = {
        "phone": st.session_state.phone,
        "message": user_message,
        "application_id": st.session_state.application_id,
    }


    try:

        response = requests.post(
            f"{API_URL}/conversation/message",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()


        # Save application ID for continuing conversation

        st.session_state.application_id = (
            data.get("application_id")
            or st.session_state.application_id
        )


        aylin_response = data.get(
            "response",
            "Не удалось получить ответ от Aylin.",
        )


        # ----------------------------------------------------
        # SHOW AYLIN RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": aylin_response,
            }
        )


        with st.chat_message("assistant"):
            st.write(aylin_response)


    except requests.RequestException as error:

        st.error(
            f"Ошибка подключения к Aylin API: {error}"
        )

    except Exception as error:

        st.error(
            f"Ошибка: {error}"
        )


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.header("Application")

    if st.session_state.application_id:

        st.write(
            "Application ID:"
        )

        st.code(
            st.session_state.application_id
        )

    else:

        st.write(
            "Application ID will appear after the first message."
        )


    if st.button("Clear conversation"):

        st.session_state.messages = []
        st.session_state.application_id = None

        st.rerun()
