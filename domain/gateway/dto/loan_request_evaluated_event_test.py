from domain import ApplicationStatus
from domain.gateway.dto import LoanRequestEvaluatedEvent


def test_event_creation():
    event = LoanRequestEvaluatedEvent()
    assert isinstance(event, LoanRequestEvaluatedEvent)


def test_event_attributes_assignment():
    event = LoanRequestEvaluatedEvent()
    event.applicationId = 101
    event.applicationStatus = ApplicationStatus.APPROVED

    assert event.applicationId == 101
    assert event.applicationStatus == ApplicationStatus.APPROVED
    assert isinstance(event.applicationStatus, ApplicationStatus)
