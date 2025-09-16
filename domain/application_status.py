from enum import Enum


class ApplicationStatus(Enum):
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    APPROVED = "APPROVED"
