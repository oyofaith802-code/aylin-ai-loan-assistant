from enum import Enum


class ApplicationStage(Enum):
    NEW = "new"
    COLLECTING_INFORMATION = "collecting_information"
    PROCESSING_APPLICATION = "processing_application"
    BUSINESS_DECISION = "business_decision"
    APPROVED = "approved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"
    COMPLETED = "completed"