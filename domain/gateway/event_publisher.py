import abc

from domain.gateway.dto import LoanRequestEvaluatedEvent


class EventPublisher(abc.ABC):

    @abc.abstractmethod
    def notify_loan_request_evaluated(self, event: LoanRequestEvaluatedEvent) -> None:
        pass
