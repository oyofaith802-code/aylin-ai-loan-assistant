from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from extraction import (
    FIELDS,
    extract_fields,
    merge_extraction,
)

from validation import validate_application


# ============================================================
# FIELD ORDER
# ============================================================

FIELD_ORDER = [
    "car_model",
    "car_year",
    "car_value",
    "loan_amount",
    "loan_program",
    "registration_region",
]


# ============================================================
# QUESTIONS
# ============================================================

QUESTION_RU = {
    "car_model": "Какая у вас модель автомобиля?",

    "car_year": "Какого года ваш автомобиль?",

    "car_value": "Какова примерная стоимость автомобиля?",

    "loan_amount": "Какую сумму займа вы хотите получить?",

    "loan_program": (
        "Подскажите, пожалуйста, Вас интересует займ "
        "без изъятия автомобиля или с размещением автомобиля "
        "на охраняемой стоянке?"
    ),

    "registration_region": (
        "В каком регионе вы зарегистрированы?"
    ),
}


# ============================================================
# CUSTOMER CARD
# ============================================================

@dataclass
class CustomerCard:

    application_id: str
    phone: str

    car_model: Optional[str] = None
    car_year: Optional[int] = None
    car_value: Optional[float] = None

    loan_amount: Optional[float] = None
    loan_program: Optional[str] = None
    registration_region: Optional[str] = None

    loan_term_months: Optional[int] = None

    stage: str = "collecting_information"

    decision: Optional[str] = None
    decision_reason: Optional[str] = None

    errors: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------------
    # TO DICT
    # --------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return {
            "application_id": self.application_id,
            "phone": self.phone,

            "car_model": self.car_model,
            "car_year": self.car_year,
            "car_value": self.car_value,

            "loan_amount": self.loan_amount,
            "loan_program": self.loan_program,
            "registration_region": self.registration_region,

            "loan_term_months": self.loan_term_months,

            "stage": self.stage,

            "decision": self.decision,
            "decision_reason": self.decision_reason,

            "errors": list(self.errors),
        }

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self, values: Dict[str, Any]) -> None:

        for field_name in FIELDS:

            if field_name not in values:
                continue

            value = values[field_name]

            # Never overwrite existing information with None
            if value is None:
                continue

            # Never overwrite with empty string
            if isinstance(value, str) and not value.strip():
                continue

            setattr(
                self,
                field_name,
                value,
            )


# ============================================================
# CONVERSATION MANAGER
# ============================================================

class ConversationManager:

    def __init__(
        self,
        application_id: Optional[str] = None,
        phone: str = "",
    ):

        self.card = CustomerCard(
            application_id=(
                application_id
                or self._generate_application_id()
            ),
            phone=phone,
        )

        self.history: List[Dict[str, Any]] = []

    # ========================================================
    # APPLICATION ID
    # ========================================================

    @staticmethod
    def _generate_application_id() -> str:

        return f"APP-{uuid.uuid4().hex[:8].upper()}"

    # ========================================================
    # PROCESS MESSAGE
    # ========================================================

    def process_message(
        self,
        customer_message: str,
    ) -> Dict[str, Any]:

        if not customer_message or not customer_message.strip():

            return self._response(
                status="invalid_message",
                message=(
                    "Пожалуйста, напишите Ваш вопрос "
                    "или информацию."
                ),
                next_field=self._next_field(),
            )

        # ----------------------------------------------------
        # CLEAN MESSAGE
        # ----------------------------------------------------

        customer_message = customer_message.strip()

        # ----------------------------------------------------
        # EXTRACT
        # ----------------------------------------------------

        extracted = extract_fields(
            customer_message
        )

        # ----------------------------------------------------
        # DEBUG
        #
        # This is temporary but very useful.
        # It tells us exactly what extraction.py returned
        # BEFORE the card is updated.
        # ----------------------------------------------------

        print("\n[EXTRACTION DEBUG]")
        print("Customer message:")
        print(customer_message)
        print("Extracted:")
        print(extracted)
        print("[END EXTRACTION DEBUG]\n")

        # ----------------------------------------------------
        # MERGE
        # ----------------------------------------------------

        existing = self.card.to_dict()

        merged = merge_extraction(
            existing,
            extracted,
        )

        # ----------------------------------------------------
        # UPDATE CARD
        # ----------------------------------------------------

        self.card.update(merged)

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        validation = validate_application(
            self.card.to_dict()
        )

        self.card.errors = validation.get(
            "errors",
            [],
        )

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        self.history.append(
            {
                "direction": "incoming",
                "text": customer_message,

                "extracted": dict(
                    extracted
                ),

                "merged_card": self.card.to_dict(),

                "errors": list(
                    self.card.errors
                ),
            }
        )

        # ----------------------------------------------------
        # FIND NEXT FIELD
        # ----------------------------------------------------

        next_field = self._next_field()

        # ----------------------------------------------------
        # STILL COLLECTING
        # ----------------------------------------------------

        if next_field is not None:

            self.card.stage = (
                "collecting_information"
            )

            return self._response(
                status="waiting_for_customer",
                message=QUESTION_RU[next_field],
                next_field=next_field,
            )

        # ----------------------------------------------------
        # EVERYTHING COLLECTED
        # ----------------------------------------------------

        self.card.stage = "ready_for_review"

        return self._response(
            status="ready_for_review",
            message=(
                "Спасибо. Я получила всю основную "
                "информацию по заявке. Данные готовы "
                "для проверки сотрудником компании."
            ),
            next_field=None,
        )

    # ========================================================
    # NEXT FIELD
    # ========================================================

    def _next_field(self) -> Optional[str]:

        for field_name in FIELD_ORDER:

            value = getattr(
                self.card,
                field_name,
                None,
            )

            if value is None:
                return field_name

        return None

    # ========================================================
    # RESPONSE
    # ========================================================

    def _response(
        self,
        status: str,
        message: str,
        next_field: Optional[str],
    ) -> Dict[str, Any]:

        latest_extracted: Dict[str, Any] = {}

        if self.history:

            latest_extracted = dict(
                self.history[-1].get(
                    "extracted",
                    {},
                )
            )

        return {
            "status": status,

            "message": message,

            "next_field": next_field,

            "stage": self.card.stage,

            "application_id": (
                self.card.application_id
            ),

            "card": self.card.to_dict(),

            "extracted": latest_extracted,

            "errors": list(
                self.card.errors
            ),
        }

    # ========================================================
    # CARD
    # ========================================================

    def get_card(self) -> Dict[str, Any]:

        return self.card.to_dict()

    # ========================================================
    # HISTORY
    # ========================================================

    def get_history(
        self,
    ) -> List[Dict[str, Any]]:

        return list(self.history)


# ============================================================
# GLOBAL MANAGER STORAGE
# ============================================================

_MANAGERS: Dict[
    str,
    ConversationManager,
] = {}


# ============================================================
# GET OR CREATE
# ============================================================

def get_or_create_manager(
    phone: str,
    application_id: Optional[str] = None,
) -> ConversationManager:

    if phone not in _MANAGERS:

        _MANAGERS[phone] = ConversationManager(
            application_id=application_id,
            phone=phone,
        )

    return _MANAGERS[phone]


# ============================================================
# PROCESS MESSAGE API
# ============================================================

def process_message(
    phone: str,
    message: str,
    application_id: Optional[str] = None,
) -> Dict[str, Any]:

    manager = get_or_create_manager(
        phone=phone,
        application_id=application_id,
    )

    return manager.process_message(
        message
    )


# ============================================================
# GET CARD
# ============================================================

def get_customer_card(
    phone: str,
) -> Optional[Dict[str, Any]]:

    manager = _MANAGERS.get(phone)

    if manager is None:
        return None

    return manager.get_card()


# ============================================================
# RESET
# ============================================================

def reset_conversation(
    phone: str,
) -> None:

    _MANAGERS.pop(
        phone,
        None,
    )


# ============================================================
# COMPATIBILITY
# ============================================================

RealConversationManager = ConversationManager
