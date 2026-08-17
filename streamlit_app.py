import streamlit as st
import requests


API_URL = "https://aylin-ai-loan-assistant.onrender.com"


st.set_page_config(
    page_title="Aylin AI Loan Assistant",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "application_id" not in st.session_state:
    st.session_state.application_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Conversation"


# ============================================================
# API HELPER
# ============================================================

def api_get(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        st.error(
            f"API connection error: {error}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Aylin")

    st.caption(
        "AI Loan Assistant"
    )

    st.divider()

    st.subheader("Customer")

    phone = st.text_input(
        "Phone number",
        value=st.session_state.phone,
        placeholder="996555123456",
    )

    st.session_state.phone = phone.strip()

    st.divider()

    st.subheader("Navigation")

    if st.button(
        "💬 Conversation",
        use_container_width=True,
    ):
        st.session_state.page = "Conversation"

    if st.button(
        "📋 Current Application",
        use_container_width=True,
    ):
        st.session_state.page = "Current Application"

    if st.button(
        "📜 Conversation History",
        use_container_width=True,
    ):
        st.session_state.page = "Conversation History"

    if st.button(
        "🗂 Application History",
        use_container_width=True,
    ):
        st.session_state.page = "Application History"

    if st.button(
        "🔗 System Status",
        use_container_width=True,
    ):
        st.session_state.page = "System Status"

    st.divider()

    if st.session_state.application_id:

        st.subheader("Application")

        st.code(
            st.session_state.application_id
        )

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.application_id = None

        st.rerun()


# ============================================================
# CONVERSATION
# ============================================================

if st.session_state.page == "Conversation":

    st.title(
        "💬 Conversation"
    )

    st.caption(
        "Test Aylin's loan application conversation."
    )

    if not st.session_state.phone:

        st.info(
            "Enter the customer's phone number in the sidebar."
        )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    user_message = st.chat_input(
        "Введите сообщение клиента..."
    )

    if user_message:

        if not st.session_state.phone:

            st.error(
                "Введите номер телефона клиента."
            )

            st.stop()

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        with st.chat_message("user"):

            st.write(
                user_message
            )

        payload = {

            "phone":
                st.session_state.phone,

            "message":
                user_message,

            "application_id":
                st.session_state.application_id,

        }

        try:

            response = requests.post(

                f"{API_URL}/conversation/message",

                json=payload,

                timeout=60,

            )

            response.raise_for_status()

            data = response.json()

            st.session_state.application_id = (

                data.get("application_id")

                or

                st.session_state.application_id

            )

            aylin_response = data.get(

                "response",

                "Не удалось получить ответ от Aylin."

            )

            st.session_state.messages.append(

                {
                    "role":
                        "assistant",

                    "content":
                        aylin_response,

                }

            )

            with st.chat_message("assistant"):

                st.write(
                    aylin_response
                )

        except requests.RequestException as error:

            st.error(
                f"Ошибка подключения к Aylin API: {error}"
            )

        except Exception as error:

            st.error(
                f"Ошибка: {error}"
            )


# ============================================================
# CURRENT APPLICATION
# ============================================================

elif st.session_state.page == "Current Application":

    st.title(
        "📋 Current Application"
    )

    if not st.session_state.phone:

        st.info(
            "Enter a customer phone number first."
        )

    else:

        data = api_get(

            f"/applications/current/"
            f"{st.session_state.phone}"

        )

        if data:

            st.success(
                "Current application found."
            )

            st.json(
                data
            )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

elif st.session_state.page == "Conversation History":

    st.title(
        "📜 Conversation History"
    )

    if not st.session_state.application_id:

        st.info(
            "Start a conversation first. "
            "The application ID will appear here."
        )

    else:

        data = api_get(

            "/dashboard/conversation/"
            f"{st.session_state.application_id}"

        )

        if data:

            st.json(
                data
            )


# ============================================================
# APPLICATION HISTORY
# ============================================================

elif st.session_state.page == "Application History":

    st.title(
        "🗂 Application History"
    )

    if not st.session_state.phone:

        st.info(
            "Enter a customer phone number first."
        )

    else:

        data = api_get(

            f"/applications/history/"
            f"{st.session_state.phone}"

        )

        if data:

            count = data.get(
                "count",
                0
            )

            st.metric(
                "Applications",
                count
            )

            applications = data.get(
                "applications",
                []
            )

            if applications:

                for index, application in enumerate(
                    applications,
                    start=1
                ):

                    with st.expander(
                        f"Application {index}"
                    ):

                        st.json(
                            application
                        )

            else:

                st.info(
                    "No previous applications found."
                )


# ============================================================
# SYSTEM STATUS
# ============================================================

elif st.session_state.page == "System Status":

    st.title(
        "🔗 System Status"
    )

    st.write(
        "Backend:"
    )

    st.code(
        API_URL
    )

    health = api_get(
        "/health"
    )

    if health:

        st.success(
            "Backend is online"
        )

        st.json(
            health
        )

    st.subheader(
        "API Information"
    )

    info = api_get(
        "/api/info"
    )

    if info:

        st.json(
            info
        )
