from typing import Optional

from domain.gateway import EventPublisher
from domain.gateway.dto import LoanRequestEvaluatedEvent


class DummyEventPublisher(EventPublisher):

    last_event: Optional[LoanRequestEvaluatedEvent] = None

    def notify_loan_request_evaluated(self, event: LoanRequestEvaluatedEvent) -> None:
        self.last_event = event
