from domain import ApplicationStatus


class LoanRequestEvaluatedEvent:

    applicationId: int
    applicationStatus: ApplicationStatus

    def __init__(self):
        pass
