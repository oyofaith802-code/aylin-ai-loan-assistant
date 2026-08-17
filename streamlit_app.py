import streamlit as st
import requests
import time


API_URL = "https://aylin-ai-loan-assistant.onrender.com"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aylin — AI помощник",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
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
    st.session_state.page = "Диалог"

if "started" not in st.session_state:
    st.session_state.started = False


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

    except requests.RequestException as error:

        st.error(
            f"Не удалось подключиться к серверу: {error}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Aylin")

    st.caption(
        "AI-помощник по оформлению займа"
    )

    st.divider()

    st.subheader("Клиент")

    phone = st.text_input(
        "Номер телефона",
        value=st.session_state.phone,
        placeholder="996555123456",
    )

    st.session_state.phone = phone.strip()

    st.divider()

    st.subheader("Разделы")

    if st.button(
        "💬 Диалог",
        use_container_width=True,
    ):
        st.session_state.page = "Диалог"
        st.rerun()

    if st.button(
        "📋 Текущая заявка",
        use_container_width=True,
    ):
        st.session_state.page = "Текущая заявка"
        st.rerun()

    if st.button(
        "📜 История диалога",
        use_container_width=True,
    ):
        st.session_state.page = "История диалога"
        st.rerun()

    if st.button(
        "🗂 История заявок",
        use_container_width=True,
    ):
        st.session_state.page = "История заявок"
        st.rerun()

    if st.button(
        "🔗 Состояние системы",
        use_container_width=True,
    ):
        st.session_state.page = "Состояние системы"
        st.rerun()

    st.divider()

    if st.session_state.application_id:

        st.subheader("Заявка")

        st.write(
            "Номер заявки:"
        )

        st.code(
            st.session_state.application_id
        )

    st.divider()

    if st.button(
        "🗑 Начать новый диалог",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.application_id = None
        st.session_state.started = False

        st.rerun()


# ============================================================
# MAIN — CONVERSATION
# ============================================================

if st.session_state.page == "Диалог":

    st.title(
        "💬 Диалог с Aylin"
    )

    st.caption(
        "Проверьте, как Aylin общается с клиентом и собирает информацию для заявки."
    )

    # --------------------------------------------------------
    # WELCOME
    # --------------------------------------------------------

    if not st.session_state.messages:

        st.info(
            "Здравствуйте! Я Aylin — AI-помощник по оформлению займа. "
            "Введите сообщение клиента ниже, чтобы начать диалог."
        )

        st.markdown(
            """
**Примеры сообщений клиента:**

- «У меня Toyota Camry 2021 года, хочу получить 500000 сом»
- «Машина стоит примерно 1500000 сом»
- «Хочу оформить займ без изъятия автомобиля»
- «Я нахожусь в Бишкеке»
- «Мне нужен займ на 12 месяцев»
"""
        )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        avatar = (
            "👤"
            if message["role"] == "user"
            else "🤖"
        )

        with st.chat_message(
            message["role"],
            avatar=avatar,
        ):

            st.write(
                message["content"]
            )

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_message = st.chat_input(
        "Напишите сообщение клиента..."
    )

    if user_message:

        if not st.session_state.phone:

            st.warning(
                "Сначала укажите номер телефона клиента слева."
            )

            st.stop()

        # ----------------------------------------------------
        # CUSTOMER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        with st.chat_message(
            "user",
            avatar="👤",
        ):

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

        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):

            with st.spinner(
                "Aylin анализирует сообщение..."
            ):

                try:

                    response = requests.post(

                        f"{API_URL}/conversation/message",

                        json=payload,

                        timeout=90,

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
                        "Извините, сейчас не удалось получить ответ.",
                    )

                    # Small delay makes the interface feel
                    # more natural without slowing the API.

                    time.sleep(0.3)

                    st.write(
                        aylin_response
                    )

                    st.session_state.messages.append(
                        {
                            "role":
                                "assistant",

                            "content":
                                aylin_response,
                        }
                    )

                except requests.RequestException as error:

                    st.error(
                        "Не удалось получить ответ от Aylin. "
                        "Попробуйте ещё раз."
                    )

                    st.caption(
                        str(error)
                    )

                except Exception as error:

                    st.error(
                        "Произошла ошибка при обработке сообщения."
                    )

                    st.caption(
                        str(error)
                    )


# ============================================================
# CURRENT APPLICATION
# ============================================================

elif st.session_state.page == "Текущая заявка":

    st.title(
        "📋 Текущая заявка"
    )

    st.caption(
        "Информация, которую Aylin уже собрала о клиенте."
    )

    if not st.session_state.phone:

        st.info(
            "Укажите номер телефона клиента слева."
        )

    else:

        data = api_get(
            f"/applications/current/{st.session_state.phone}"
        )

        if data:

            st.success(
                "Заявка найдена"
            )

            customer = data.get(
                "customer",
                data
            )

            if isinstance(customer, dict):

                columns = [

                    ("car_model", "Автомобиль"),

                    ("car_year", "Год выпуска"),

                    ("car_value", "Стоимость автомобиля"),

                    ("loan_amount", "Сумма займа"),

                    ("loan_program", "Программа займа"),

                    ("loan_term_months", "Срок займа"),

                    ("vehicle_possession", "Условия хранения автомобиля"),

                    ("registration_region", "Регион регистрации"),

                    ("stage", "Этап"),

                ]

                for key, label in columns:

                    value = customer.get(key)

                    if value is not None:

                        st.write(
                            f"**{label}:** {value}"
                        )

            else:

                st.json(
                    data
                )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

elif st.session_state.page == "История диалога":

    st.title(
        "📜 История диалога"
    )

    st.caption(
        "Предыдущие сообщения по текущей заявке."
    )

    if not st.session_state.application_id:

        st.info(
            "Сначала начните диалог с клиентом."
        )

    else:

        data = api_get(
            "/dashboard/conversation/"
            f"{st.session_state.application_id}"
        )

        if data:

            if isinstance(data, list):

                for item in data:

                    st.write(item)

            else:

                st.json(data)


# ============================================================
# APPLICATION HISTORY
# ============================================================

elif st.session_state.page == "История заявок":

    st.title(
        "🗂 История заявок"
    )

    st.caption(
        "Все предыдущие заявки клиента."
    )

    if not st.session_state.phone:

        st.info(
            "Укажите номер телефона клиента слева."
        )

    else:

        data = api_get(
            f"/applications/history/{st.session_state.phone}"
        )

        if data:

            count = data.get(
                "count",
                0
            )

            st.metric(
                "Количество заявок",
                count
            )

            applications = data.get(
                "applications",
                []
            )

            if applications:

                for index, application in enumerate(
                    applications,
                    start=1,
                ):

                    with st.expander(
                        f"Заявка №{index}"
                    ):

                        st.json(
                            application
                        )

            else:

                st.info(
                    "У клиента пока нет предыдущих заявок."
                )


# ============================================================
# SYSTEM STATUS
# ============================================================

elif st.session_state.page == "Состояние системы":

    st.title(
        "🔗 Состояние системы"
    )

    health = api_get(
        "/health"
    )

    if health:

        st.success(
            "Aylin работает"
        )

        st.json(
            health
        )

    st.subheader(
        "Информация об API"
    )

    info = api_get(
        "/api/info"
    )

    if info:

        st.json(
            info
        )

    st.caption(
        "Wazzup/WhatsApp пока не подключён. "
        "Интеграция будет выполнена после согласования логики диалога."
    )
