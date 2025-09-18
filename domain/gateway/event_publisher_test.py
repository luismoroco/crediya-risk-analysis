import pytest

from domain import ApplicationStatus
from domain.gateway import EventPublisher
from domain.gateway.dto import LoanRequestEvaluatedEvent
from infrastructure.dummy_event_publisher import DummyEventPublisher


def test_event_publisher_is_abstract():
    with pytest.raises(TypeError):
        EventPublisher()


def test_dummy_sqs_event_publisher():
    publisher = DummyEventPublisher()

    event = LoanRequestEvaluatedEvent()
    event.applicationId = 101
    event.applicationStatus = ApplicationStatus.APPROVED

    publisher.notify_loan_request_evaluated(event)

    assert hasattr(publisher, "last_event")
    assert publisher.last_event is event
    assert publisher.last_event.applicationId == 101
    assert publisher.last_event.applicationStatus == ApplicationStatus.APPROVED
