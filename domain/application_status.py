from enum import Enum


class ApplicationStatus(Enum):
    REJECTED = 1
    PENDING = 2
    MANUAL_REVIEW = 3
    APPROVED = 4
