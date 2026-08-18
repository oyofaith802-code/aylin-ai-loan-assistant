import streamlit as st
import requests
import time
import pandas as pd


API_URL = "https://aylin-ai-loan-assistant.onrender.com"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aylin — AI Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "phone": "",
    "application_id": None,
    "messages": [],
    "page": "Диалог",
    "audio_history": [],
    "csv_data": None,
    "selected_message": None,
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# API
# ============================================================

def api_get(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except Exception as error:

        st.error(
            f"API error: {error}"
        )

        return None


def get_customer():

    if not st.session_state.phone:

        return None

    return api_get(
        f"/applications/current/{st.session_state.phone}"
    )


# ============================================================
# RESET CLIENT
# ============================================================

def reset_client():

    st.session_state.phone = ""
    st.session_state.application_id = None
    st.session_state.messages = []
    st.session_state.audio_history = []
    st.session_state.csv_data = None
    st.session_state.selected_message = None
    st.session_state.page = "Диалог"


# ============================================================
# CUSTOMER CARD
# ============================================================

def show_customer_card(customer):

    st.subheader("👤 Customer Card")

    if not customer:

        st.info(
            "Customer information will appear here "
            "after the first message."
        )

        return


    customer = customer.get(
        "customer",
        customer
    )


    fields = [

        ("car_model", "🚗 Vehicle model"),

        ("car_year", "📅 Year"),

        ("car_value", "💰 Vehicle value"),

        ("loan_amount", "💵 Loan amount"),

        ("loan_program", "📋 Loan program"),

        ("loan_term_months", "⏱ Loan term"),

        ("vehicle_possession", "🔐 Vehicle possession"),

        ("registration_region", "📍 Registration region"),

        ("stage", "⚙️ Stage"),

    ]


    for key, label in fields:

        value = customer.get(key)


        if value in (None, ""):

            display_value = "Not specified"

        else:

            display_value = value


        if key in (
            "car_value",
            "loan_amount",
        ):

            if value not in (None, ""):

                try:

                    display_value = (
                        f"{float(value):,.0f}"
                        .replace(",", " ")
                        + " сом"
                    )

                except Exception:

                    display_value = value


        if key == "loan_term_months":

            if value not in (None, ""):

                display_value = (
                    f"{value} months"
                )


        if key == "vehicle_possession":

            if value == "customer":

                display_value = (
                    "Vehicle remains with customer"
                )

            elif value == "lender":

                display_value = (
                    "Secure parking"
                )


        st.markdown(
            f"""
            <div style="
                padding:12px;
                margin-bottom:7px;
                border:1px solid #e5e7eb;
                border-radius:10px;
                background:#fafafa;
            ">
                <div style="
                    font-size:12px;
                    color:#6b7280;
                ">
                    {label}
                </div>

                <div style="
                    font-size:16px;
                    font-weight:600;
                    margin-top:3px;
                ">
                    {display_value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.divider()


    application_id = customer.get(
        "application_id"
    )


    if application_id:

        st.caption(
            "Application ID"
        )

        st.code(
            application_id
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Aylin")

    st.caption(
        "AI Loan Assistant — Testing Center"
    )

    st.divider()


    # --------------------------------------------------------
    # CLIENT
    # --------------------------------------------------------

    st.subheader("👤 Test Client")

    phone = st.text_input(
        "Phone number",
        value=st.session_state.phone,
        placeholder="996555123456",
    )

    st.session_state.phone = phone.strip()


    st.divider()


    # --------------------------------------------------------
    # NEW CLIENT
    # --------------------------------------------------------

    if st.button(
        "➕ New Client",
        use_container_width=True,
        type="primary",
    ):

        reset_client()

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.subheader("Navigation")


    if st.button(
        "💬 Conversation",
        use_container_width=True,
    ):

        st.session_state.page = "Диалог"

        st.rerun()


    if st.button(
        "👤 Customer Card",
        use_container_width=True,
    ):

        st.session_state.page = "Карточка клиента"

        st.rerun()


    if st.button(
        "📜 Previous Chats",
        use_container_width=True,
    ):

        st.session_state.page = "История диалога"

        st.rerun()


    if st.button(
        "🗂 Applications",
        use_container_width=True,
    ):

        st.session_state.page = "История заявок"

        st.rerun()


    if st.button(
        "🎙️ Audio",
        use_container_width=True,
    ):

        st.session_state.page = "Аудио"

        st.rerun()


    if st.button(
        "📊 CSV",
        use_container_width=True,
    ):

        st.session_state.page = "CSV"

        st.rerun()


    if st.button(
        "🔗 System Status",
        use_container_width=True,
    ):

        st.session_state.page = "Состояние системы"

        st.rerun()


    st.divider()

    st.caption(
        "Aylin Testing Center"
    )


# ============================================================
# CONVERSATION
# ============================================================

if st.session_state.page == "Диалог":

    st.title("💬 Aylin Conversation")

    st.caption(
        "Test real customer conversations while watching "
        "the customer card update."
    )


    left, right = st.columns(
        [1.55, 1]
    )


    # ========================================================
    # CHAT
    # ========================================================

    with left:

        st.subheader("Conversation")


        if not st.session_state.phone:

            st.info(
                "Enter a customer phone number in the sidebar."
            )


        if not st.session_state.messages:

            st.markdown(
                """
### Start a test

Try a complete customer message:

> У меня Toyota Camry 2021 года, стоимость примерно
> 1500000 сом, хочу получить 500000 сом

Or test a natural conversation step by step.
                """
            )


        # ----------------------------------------------------
        # MESSAGE HISTORY
        # ----------------------------------------------------

        for index, message in enumerate(
            st.session_state.messages
        ):

            if message["role"] == "user":

                with st.chat_message(
                    "user",
                    avatar="👤",
                ):

                    st.write(
                        message["content"]
                    )

            else:

                with st.chat_message(
                    "assistant",
                    avatar="🤖",
                ):

                    st.write(
                        message["content"]
                    )


        # ----------------------------------------------------
        # CHAT INPUT
        # ----------------------------------------------------

        user_message = st.chat_input(
            "Type customer message..."
        )


        if user_message:

            if not st.session_state.phone:

                st.warning(
                    "Enter the customer's phone number first."
                )

                st.stop()


            # ------------------------------------------------
            # CLIENT MESSAGE
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_message,
                    "timestamp": time.time(),
                }
            )


            payload = {

                "phone":
                    st.session_state.phone,

                "message":
                    user_message,

                "application_id":
                    st.session_state.application_id,

            }


            # ------------------------------------------------
            # API
            # ------------------------------------------------

            try:

                with st.spinner(
                    "Aylin is analyzing the message..."
                ):

                    response = requests.post(

                        f"{API_URL}/conversation/message",

                        json=payload,

                        timeout=90,

                    )


                response.raise_for_status()

                data = response.json()


                st.session_state.application_id = (

                    data.get(
                        "application_id"
                    )

                    or

                    st.session_state.application_id
                )


                aylin_response = data.get(
                    "response",
                    "Aylin did not return a response.",
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": aylin_response,
                        "timestamp": time.time(),
                    }
                )


                st.rerun()


            except Exception as error:

                st.error(
                    f"Could not contact Aylin API: {error}"
                )


    # ========================================================
    # CUSTOMER CARD
    # ========================================================

    with right:

        customer_data = get_customer()

        show_customer_card(
            customer_data
        )


# ============================================================
# CUSTOMER CARD
# ============================================================

elif st.session_state.page == "Карточка клиента":

    st.title("👤 Customer Card")

    st.caption(
        "Information collected by Aylin."
    )


    customer_data = get_customer()


    if customer_data:

        show_customer_card(
            customer_data
        )

    else:

        st.info(
            "No active application found for this customer."
        )


# ============================================================
# PREVIOUS CHATS
# ============================================================

elif st.session_state.page == "История диалога":

    st.title("📜 Conversation History")

    st.caption(
        "Messages from the current testing session."
    )


    if not st.session_state.messages:

        st.info(
            "No messages yet."
        )

    else:

        for index, message in enumerate(
            st.session_state.messages
        ):

            role = (
                "👤 Customer"
                if message["role"] == "user"
                else "🤖 Aylin"
            )


            with st.expander(
                f"{role} — Message {index + 1}"
            ):

                st.write(
                    message["content"]
                )


# ============================================================
# APPLICATION HISTORY
# ============================================================

elif st.session_state.page == "История заявок":

    st.title("🗂 Applications")

    st.caption(
        "Previous applications associated with this client."
    )


    if not st.session_state.phone:

        st.info(
            "Enter a customer phone number."
        )

    else:

        data = api_get(
            f"/applications/history/{st.session_state.phone}"
        )


        if data:

            applications = data.get(
                "applications",
                []
            )


            if applications:

                for application in applications:

                    application_id = application.get(
                        "application_id",
                        "Application"
                    )


                    with st.expander(
                        application_id
                    ):

                        st.json(
                            application
                        )

            else:

                st.info(
                    "No previous applications."
                )


# ============================================================
# AUDIO
# ============================================================

elif st.session_state.page == "Аудио":

    st.title("🎙️ Audio Testing")

    st.caption(
        "Test customer voice messages before connecting "
        "speech-to-text to Aylin."
    )


    tab_record, tab_upload = st.tabs(
        [
            "🎙️ Record",
            "📁 Upload",
        ]
    )


    # ========================================================
    # RECORD
    # ========================================================

    with tab_record:

        st.subheader(
            "Record customer audio"
        )


        audio_value = st.audio_input(
            "Record a voice message"
        )


        if audio_value:

            st.audio(
                audio_value
            )


            st.success(
                "Audio captured successfully."
            )


            st.download_button(
                "⬇️ Save audio",
                audio_value,
                file_name="customer_voice.wav",
                mime="audio/wav",
                use_container_width=True,
            )


    # ========================================================
    # UPLOAD
    # ========================================================

    with tab_upload:

        st.subheader(
            "Upload audio file"
        )


        uploaded_audio = st.file_uploader(

            "Choose an audio file",

            type=[
                "wav",
                "mp3",
                "m4a",
                "ogg",
                "webm",
            ],

        )


        if uploaded_audio:

            st.audio(
                uploaded_audio
            )


            st.success(
                f"Loaded: {uploaded_audio.name}"
            )


            st.write(
                f"File size: "
                f"{uploaded_audio.size / 1024:.1f} KB"
            )


# ============================================================
# CSV
# ============================================================

elif st.session_state.page == "CSV":

    st.title("📊 CSV Testing")

    st.caption(
        "Upload customer data for testing and inspection."
    )


    uploaded_csv = st.file_uploader(

        "Upload customer CSV",

        type=[
            "csv",
        ],

    )


    if uploaded_csv:

        try:

            dataframe = pd.read_csv(
                uploaded_csv
            )


            st.session_state.csv_data = dataframe


            st.success(
                f"Loaded {len(dataframe):,} records."
            )


            st.subheader(
                "Dataset Preview"
            )


            st.dataframe(
                dataframe.head(100),
                use_container_width=True,
                height=400,
            )


            st.subheader(
                "Dataset Information"
            )


            metric1, metric2, metric3 = st.columns(3)


            metric1.metric(
                "Rows",
                f"{len(dataframe):,}"
            )


            metric2.metric(
                "Columns",
                f"{len(dataframe.columns):,}"
            )


            metric3.metric(
                "Missing values",
                f"{int(dataframe.isna().sum().sum()):,}"
            )


            st.subheader(
                "Columns"
            )


            column_data = pd.DataFrame(
                {
                    "Column":
                        dataframe.columns,

                    "Data type":
                        [
                            str(dtype)
                            for dtype in dataframe.dtypes
                        ],

                    "Missing":
                        [
                            int(dataframe[col].isna().sum())
                            for col in dataframe.columns
                        ],
                }
            )


            st.dataframe(
                column_data,
                use_container_width=True,
            )


        except Exception as error:

            st.error(
                f"Could not read CSV: {error}"
            )


    else:

        st.info(
            "Upload a CSV file to begin."
        )


# ============================================================
# SYSTEM STATUS
# ============================================================

elif st.session_state.page == "Состояние системы":

    st.title("🔗 System Status")


    st.write(
        "Checking Aylin API..."
    )


    health = api_get(
        "/health"
    )


    if health is not None:

        st.success(
            "🟢 Aylin API is online"
        )


        st.json(
            health
        )

    else:

        st.error(
            "🔴 Aylin API is unavailable"
        )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Messages in current session",
            len(st.session_state.messages)
        )


    with col2:

        st.metric(
            "Current application",
            st.session_state.application_id
            or "None"
        )


    st.subheader(
        "API"
    )


    st.code(
        API_URL
    )


    st.subheader(
        "Conversation endpoint"
    )


    st.code(
        "/conversation/message"
    )
