import streamlit as st
import requests
import time


API_URL = "https://aylin-ai-loan-assistant.onrender.com"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Aylin — Тестирование",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION
# ============================================================

defaults = {
    "phone": "",
    "application_id": None,
    "messages": [],
    "page": "Диалог",
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

    except requests.RequestException:
        return None

    except Exception:
        return None


def get_customer():

    if not st.session_state.phone:
        return None

    return api_get(
        f"/applications/current/{st.session_state.phone}"
    )


def reset_client():

    st.session_state.messages = []
    st.session_state.application_id = None
    st.session_state.page = "Диалог"


# ============================================================
# CUSTOMER CARD
# ============================================================

def show_customer_card(customer):

    st.subheader("👤 Карточка клиента")

    if not customer:

        st.info(
            "После первого сообщения здесь появится "
            "информация о клиенте."
        )

        return

    fields = [

        ("car_model", "Модель автомобиля"),

        ("car_year", "Год выпуска"),

        ("car_value", "Стоимость автомобиля"),

        ("loan_amount", "Сумма займа"),

        ("loan_program", "Программа займа"),

        ("loan_term_months", "Срок займа"),

        ("vehicle_possession", "Условия хранения автомобиля"),

        ("registration_region", "Регион регистрации"),

        ("stage", "Этап"),

    ]

    for key, label in fields:

        value = customer.get(key)

        if value is None or value == "":
            value = "Не указано"

        if key in (
            "car_value",
            "loan_amount",
        ) and value != "Не указано":

            try:
                value = (
                    f"{float(value):,.0f}"
                    .replace(",", " ")
                    + " сом"
                )
            except Exception:
                pass

        if key == "loan_term_months" and value != "Не указано":

            value = f"{value} мес."

        if key == "vehicle_possession":

            if value == "customer":
                value = "Автомобиль остаётся у клиента"

            elif value == "lender":
                value = "Охраняемая стоянка"

        st.markdown(
            f"""
            <div style="
                padding:10px;
                margin-bottom:6px;
                border:1px solid #ddd;
                border-radius:8px;
            ">
                <div style="font-size:13px;color:#777;">
                    {label}
                </div>
                <div style="font-size:16px;font-weight:600;">
                    {value}
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

        st.caption("Номер заявки")

        st.code(
            application_id
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Aylin")

    st.caption(
        "AI-помощник по оформлению займа"
    )

    st.divider()

    st.subheader("Тестовый клиент")

    phone = st.text_input(
        "Номер телефона",
        value=st.session_state.phone,
        placeholder="996555123456",
    )

    st.session_state.phone = phone.strip()

    st.divider()

    # --------------------------------------------------------
    # NEW CLIENT
    # --------------------------------------------------------

    if st.button(
        "➕ Новый клиент",
        use_container_width=True,
        type="primary",
    ):

        reset_client()

        st.rerun()

    st.divider()

    st.subheader("Разделы")

    if st.button(
        "💬 Диалог",
        use_container_width=True,
    ):

        st.session_state.page = "Диалог"

        st.rerun()

    if st.button(
        "📋 Карточка клиента",
        use_container_width=True,
    ):

        st.session_state.page = "Карточка клиента"

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


# ============================================================
# DIALOG
# ============================================================

if st.session_state.page == "Диалог":

    st.title("💬 Тестирование Aylin")

    st.caption(
        "Проверьте реальный сценарий общения с клиентом. "
        "Карточка клиента обновляется после каждого сообщения."
    )

    left, right = st.columns(
        [1.55, 1]
    )

    # ========================================================
    # CHAT
    # ========================================================

    with left:

        st.subheader("Диалог")

        if not st.session_state.phone:

            st.info(
                "Введите номер телефона клиента слева, "
                "затем начните диалог."
            )

        if not st.session_state.messages:

            st.markdown(
                """
                **Начните тестирование**

                Например:

                > Здравствуйте, хочу получить займ под автомобиль.

                Или сразу передайте несколько данных:

                > У меня Toyota Camry 2021 года, машина стоит
                > примерно 1 500 000 сом, хочу получить
                > 500 000 сом.
                """
            )

        for message in st.session_state.messages:

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

        user_message = st.chat_input(
            "Введите сообщение клиента..."
        )

        if user_message:

            if not st.session_state.phone:

                st.warning(
                    "Сначала укажите номер телефона клиента."
                )

                st.stop()

            # ------------------------------------------------
            # SHOW CLIENT MESSAGE
            # ------------------------------------------------

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

            # ------------------------------------------------
            # SEND TO API
            # ------------------------------------------------

            with st.chat_message(
                "assistant",
                avatar="🤖",
            ):

                with st.spinner(
                    "Aylin обрабатывает сообщение..."
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

                            data.get(
                                "application_id"
                            )
                            or
                            st.session_state.application_id
                        )

                        aylin_response = data.get(
                            "response",
                            "Не удалось получить ответ от Aylin.",
                        )

                        time.sleep(0.2)

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
                            "Не удалось подключиться к Aylin API."
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

            # ------------------------------------------------
            # REFRESH PAGE
            # ------------------------------------------------

            st.rerun()

    # ========================================================
    # CUSTOMER CARD
    # ========================================================

    with right:

        customer_data = get_customer()

        show_customer_card(
            customer_data
        )


# ============================================================
# CUSTOMER CARD PAGE
# ============================================================

elif st.session_state.page == "Карточка клиента":

    st.title("👤 Карточка клиента")

    st.caption(
        "Все данные, которые Aylin уже собрала."
    )

    if not st.session_state.phone:

        st.info(
            "Введите номер телефона клиента."
        )

    else:

        customer_data = get_customer()

        if customer_data:

            customer = customer_data.get(
                "customer",
                customer_data
            )

            show_customer_card(
                customer
            )

        else:

            st.info(
                "Для этого номера пока нет активной заявки."
            )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

elif st.session_state.page == "История диалога":

    st.title("📜 История диалога")

    if not st.session_state.messages:

        st.info(
            "В текущем тестовом диалоге пока нет сообщений."
        )

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.markdown(
                    f"**👤 Клиент:** {message['content']}"
                )

            else:

                st.markdown(
                    f"**🤖 Aylin:** {message['content']}"
                )

            st.divider()


# ============================================================
# APPLICATION HISTORY
# ============================================================

elif st.session_state.page == "История заявок":

    st.title("🗂 История заявок")

    if not st.session_state.phone:

        st.info(
            "Введите номер телефона клиента."
        )

    else:

        data = api_get(
            f"/applications/history/{st.session_state.phone}"
        )

        if not data:

            st.warning(
                "Не удалось получить историю заявок."
            )

        else:

            applications = data.get(
                "applications",
                []
            )

            if not applications:

                st.info(
                    "У клиента пока нет истории заявок."
                )

            else:

                st.write(
                    f"Количество заявок: {len(applications)}"
                )

                for application in applications:

                    with st.expander(
                        application.get(
                            "application_id",
                            "Заявка"
                        )
                    ):

                        st.json(
                            application
                        )


# ============================================================
# SYSTEM STATUS
# ============================================================

elif st.session_state.page == "Состояние системы":

    st.title("🔗 Состояние системы")

    st.write(
        "Проверка доступности Aylin API."
    )

    health = api_get(
        "/health"
    )

    if health is not None:

        st.success(
            "Aylin API работает"
        )

        st.json(
            health
        )

    else:

        st.error(
            "Aylin API недоступен"
        )

    st.divider()

    st.write(
        "**API:**"
    )

    st.code(
        API_URL
    )

    st.write(
        "**Основной endpoint:**"
    )

    st.code(
        "/conversation/message"
    )
