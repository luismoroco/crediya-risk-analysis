from decimal import Decimal

import pytest

from domain import ApplicationStatus
from infrastructure.dummy_event_publisher import DummyEventPublisher
from usecase import RiskAnalysisUseCase
from usecase.dto import (
    Application,
    AutomaticEvaluationLoanRequestStartedDTO,
    LoanType,
    MinimalLoanDTO,
)


@pytest.fixture
def setup_dto_approved():
    app = Application(
        applicationId=1,
        amount=3000,
        deadline=12,
        email="a@b.com",
        applicationStatusId=0,
        loanTypeId=1,
    )
    loan_type = LoanType(
        loanTypeId=1,
        name="Personal",
        maximumAmount=5000,
        minimumAmount=1000,
        interestRate=Decimal("0.05"),
        automaticValidation=True,
    )
    minimal_loans = [
        MinimalLoanDTO(loanId=1, amount=500, deadline=12, interestRate=Decimal("0.05")),
        MinimalLoanDTO(loanId=2, amount=500, deadline=12, interestRate=Decimal("0.05")),
    ]
    return AutomaticEvaluationLoanRequestStartedDTO(
        basicWaging=10000,
        application=app,
        loanType=loan_type,
        minimalLoanDTOS=minimal_loans,
    )


@pytest.fixture
def setup_usecase(monkeypatch):
    use_case = RiskAnalysisUseCase()
    dummy_publisher = DummyEventPublisher()
    monkeypatch.setattr(use_case, "event_publisher", dummy_publisher)
    return use_case, dummy_publisher


def test_get_monthly_installment():
    result = RiskAnalysisUseCase._get_monthly_installment(
        Decimal("1200"), Decimal("0.05"), 12
    )
    assert isinstance(result, Decimal)
    assert result > 0


def test_loan_approved(setup_usecase, setup_dto_approved):
    usecase, publisher = setup_usecase
    usecase.evaluate_loan_request(setup_dto_approved)
    event = publisher.last_event
    assert event.applicationId == setup_dto_approved.application.applicationId
    assert event.applicationStatus == ApplicationStatus.APPROVED
