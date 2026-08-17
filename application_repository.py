import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Text
)

from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///aylin.db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# ============================================================
# CONVERSATION MESSAGE
# ============================================================

class ConversationMessage(Base):

    __tablename__ = "conversation_messages"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    application_id = Column(
        String,
        nullable=False,
        index=True
    )

    phone = Column(
        String,
        nullable=False,
        index=True
    )

    sender = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ============================================================
# APPLICATION
# ============================================================

class Application(Base):

    __tablename__ = "applications"

    application_id = Column(
        String,
        primary_key=True
    )

    phone = Column(
        String,
        nullable=False,
        index=True
    )

    # ========================================================
    # VEHICLE
    # ========================================================

    car_model = Column(
        String,
        nullable=True
    )

    car_year = Column(
        Integer,
        nullable=True
    )

    car_value = Column(
        Float,
        nullable=True
    )

    # ========================================================
    # LOAN
    # ========================================================

    loan_amount = Column(
        Float,
        nullable=True
    )

    loan_program = Column(
        String,
        nullable=True
    )

    vehicle_possession = Column(
        String,
        nullable=True
    )

    # CUSTOMER
    # ========================================================

    registration_region = Column(
        String,
        nullable=True
    )

    # ========================================================
    # APPLICATION STATE
    # ========================================================

    stage = Column(
        String,
        nullable=False,
        default="new"
    )

    # ========================================================
    # DECISION
    # ========================================================

    decision = Column(
        String,
        nullable=True
    )

    decision_reason = Column(
        Text,
        nullable=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# ============================================================
# SAVE CONVERSATION MESSAGE
# ============================================================

def save_conversation_message(
    application_id: str,
    phone: str,
    sender: str,
    message: str
):

    db = SessionLocal()

    try:

        conversation_message = ConversationMessage(
            application_id=application_id,
            phone=phone,
            sender=sender,
            message=message
        )

        db.add(conversation_message)
        db.commit()
        db.refresh(conversation_message)

        return conversation_message

    finally:

        db.close()



# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

def get_conversation_messages(
    application_id: str
):

    db = SessionLocal()

    try:

        return (
            db.query(ConversationMessage)
            .filter(
                ConversationMessage.application_id
                == application_id
            )
            .order_by(
                ConversationMessage.id.asc()
            )
            .all()
        )

    finally:

        db.close()



# ============================================================
# CREATE TABLE
# ============================================================

def create_application_table():

    Base.metadata.create_all(
        bind=engine
    )


# ============================================================
# SAVE CUSTOMER
# ============================================================

def save_customer(
    customer
):
    """
    Save the complete CustomerCard.

    This includes:
        - customer information
        - vehicle information
        - loan information
        - application stage
        - business decision
        - decision reason
    """

    db = SessionLocal()

    try:

        application = db.query(
            Application
        ).filter(
            Application.application_id
            == customer.application_id
        ).first()

        # ----------------------------------------------------
        # Create new application
        # ----------------------------------------------------

        if application is None:

            application = Application(
                application_id=customer.application_id,
                phone=customer.phone
            )

            db.add(application)

        # ----------------------------------------------------
        # Basic customer information
        # ----------------------------------------------------

        application.phone = customer.phone

        # ----------------------------------------------------
        # Vehicle
        # ----------------------------------------------------

        application.car_model = (
            customer.car_model
        )

        application.car_year = (
            customer.car_year
        )

        application.car_value = (
            customer.car_value
        )

        # ----------------------------------------------------
        # Loan
        # ----------------------------------------------------

        application.loan_amount = (
            customer.loan_amount
        )

        application.loan_program = (
            customer.loan_program
        )

        application.vehicle_possession = (
            customer.vehicle_possession
        )

        # ----------------------------------------------------
        # Customer region
        # ----------------------------------------------------

        application.registration_region = (
            customer.registration_region
        )

        # ----------------------------------------------------
        # Application state
        # ----------------------------------------------------

        application.stage = (
            customer.stage
        )

        # ----------------------------------------------------
        # Decision
        #
        # getattr() protects us if an older CustomerCard
        # instance does not yet have these attributes.
        # ----------------------------------------------------

        application.decision = getattr(
            customer,
            "decision",
            None
        )

        application.decision_reason = getattr(
            customer,
            "decision_reason",
            None
        )

        # ----------------------------------------------------
        # Timestamp
        # ----------------------------------------------------

        application.updated_at = datetime.utcnow()

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        db.commit()

        # Refresh object with database values
        db.refresh(application)

        return application

    finally:

        db.close()


# ============================================================
# GET APPLICATION BY ID
# ============================================================

def get_application(
    application_id: str
):

    db = SessionLocal()

    try:

        return db.query(
            Application
        ).filter(
            Application.application_id
            == application_id
        ).first()

    finally:

        db.close()


# ============================================================
# GET LATEST APPLICATION BY PHONE
# ============================================================

def get_application_by_phone(
    phone: str
):

    db = SessionLocal()

    try:

        return db.query(
            Application
        ).filter(
            Application.phone == phone
        ).order_by(
            Application.updated_at.desc()
        ).first()

    finally:

        db.close()


# ============================================================
# GET ALL APPLICATIONS FOR CUSTOMER
# ============================================================

def get_applications_by_phone(
    phone: str
):

    db = SessionLocal()

    try:

        return db.query(
            Application
        ).filter(
            Application.phone == phone
        ).order_by(
            Application.updated_at.desc(),
            Application.created_at.desc()
        ).all()

    finally:

        db.close()


# ============================================================
# SAVE DECISION
# ============================================================

def save_decision(
    application_id: str,
    decision: str,
    reason: str
):
    """
    Save business decision separately.

    Useful when the decision engine completes
    after the CustomerCard has already been saved.
    """

    db = SessionLocal()

    try:

        application = db.query(
            Application
        ).filter(
            Application.application_id
            == application_id
        ).first()

        if application is None:
            return None

        application.decision = decision

        application.decision_reason = reason

        application.updated_at = datetime.utcnow()

        db.commit()

        db.refresh(application)

        return application

    finally:

        db.close()

# ============================================================
# GET CONVERSATION HISTORY
# ============================================================

def get_conversation_history(
    application_id: str
):

    db = SessionLocal()

    try:

        messages = (
            db.query(ConversationMessage)
            .filter(
                ConversationMessage.application_id
                == application_id
            )
            .order_by(
                ConversationMessage.id.asc()
            )
            .all()
        )

        return messages

    finally:

        db.close()

