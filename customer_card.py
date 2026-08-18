from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================
# CUSTOMER CARD
# ============================================================

@dataclass
class CustomerCard:

    application_id: str
    phone: str

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    car_model: Optional[str] = None
    car_year: Optional[int] = None
    car_value: Optional[float] = None

    # --------------------------------------------------------
    # LOAN
    # --------------------------------------------------------

    loan_amount: Optional[float] = None
    loan_program: Optional[str] = None
    loan_term_months: Optional[int] = None

    # --------------------------------------------------------
    # VEHICLE POSSESSION
    # --------------------------------------------------------

    vehicle_possession: Optional[str] = None

    # --------------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------------

    registration_region: Optional[str] = None

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language: str = "russian"

    # --------------------------------------------------------
    # APPLICATION STATE
    # --------------------------------------------------------

    stage: str = "new"

    # Whether Aylin has already introduced herself
    # to this customer.
    introduced: bool = False

    decision: Optional[str] = None
    decision_reason: Optional[str] = None

    errors: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # ========================================================
    # STAGE COMPATIBILITY
    # ========================================================

    @property
    def current_stage(self):
        return self.stage

    @current_stage.setter
    def current_stage(self, value):
        if hasattr(value, "value"):
            self.stage = value.value
        else:
            self.stage = str(value)

    # ========================================================
    # TO DICT
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:

        return {
            "application_id": self.application_id,
            "phone": self.phone,

            "car_model": self.car_model,
            "car_year": self.car_year,
            "car_value": self.car_value,

            "loan_amount": self.loan_amount,
            "loan_program": self.loan_program,
            "loan_term_months": self.loan_term_months,

            "vehicle_possession": self.vehicle_possession,

            "registration_region": self.registration_region,

            "language": self.language,

            "stage": self.stage,

            "introduced": self.introduced,

            "decision": self.decision,
            "decision_reason": self.decision_reason,

            "errors": list(self.errors),
        }

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        values: Dict[str, Any],
    ) -> None:

        if not values:
            return

        fields = [
            "car_model",
            "car_year",
            "car_value",

            "loan_amount",
            "loan_program",
            "loan_term_months",

            "vehicle_possession",
            "registration_region",
        ]

        for field_name in fields:

            value = values.get(field_name)

            if value is None:
                continue

            if isinstance(value, str):
                if not value.strip():
                    continue

            setattr(
                self,
                field_name,
                value,
            )

    # ========================================================
    # FROM DICT
    # ========================================================

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "CustomerCard":

        return cls(
            application_id=data.get(
                "application_id",
                "",
            ),

            phone=data.get(
                "phone",
                "",
            ),

            car_model=data.get(
                "car_model"
            ),

            car_year=data.get(
                "car_year"
            ),

            car_value=data.get(
                "car_value"
            ),

            loan_amount=data.get(
                "loan_amount"
            ),

            loan_program=data.get(
                "loan_program"
            ),

            loan_term_months=data.get(
                "loan_term_months"
            ),

            vehicle_possession=data.get(
                "vehicle_possession"
            ),

            registration_region=data.get(
                "registration_region"
            ),

            language=data.get(
                "language",
                "russian",
            ),

            stage=data.get(
                "stage",
                "new",
            ),

            introduced=bool(
                data.get(
                    "introduced",
                    False,
                )
            ),

            decision=data.get(
                "decision"
            ),

            decision_reason=data.get(
                "decision_reason"
            ),

            errors=list(
                data.get(
                    "errors",
                    [],
                )
            ),
        )