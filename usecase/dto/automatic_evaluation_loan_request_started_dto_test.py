from decimal import Decimal

from usecase.dto import (
    Application,
    AutomaticEvaluationLoanRequestStartedDTO,
    LoanType,
    MinimalLoanDTO,
)


def test_application_creation():
    app = Application(
        applicationId=1,
        amount=1000,
        deadline=12,
        email="user@example.com",
        applicationStatusId=2,
        loanTypeId=3,
    )
    assert isinstance(app, Application)
    assert app.amount == 1000
    assert app.email == "user@example.com"


def test_loan_type_creation():
    loan_type = LoanType(
        loanTypeId=1,
        name="Personal",
        maximumAmount=5000,
        minimumAmount=1000,
        interestRate=Decimal("0.05"),
        automaticValidation=True,
    )
    assert isinstance(loan_type, LoanType)
    assert loan_type.interestRate == Decimal("0.05")
    assert loan_type.automaticValidation is True


def test_minimal_loan_dto_creation():
    minimal_loan = MinimalLoanDTO(
        loanId=1, amount=1000, deadline=12, interestRate=Decimal("0.05")
    )
    assert isinstance(minimal_loan, MinimalLoanDTO)
    assert minimal_loan.amount == 1000


def test_automatic_evaluation_loan_request_started_dto():
    app = Application(
        applicationId=1,
        amount=1000,
        deadline=12,
        email="user@example.com",
        applicationStatusId=2,
        loanTypeId=3,
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
        MinimalLoanDTO(
            loanId=1, amount=1000, deadline=12, interestRate=Decimal("0.05")
        ),
        MinimalLoanDTO(
            loanId=2, amount=1500, deadline=12, interestRate=Decimal("0.06")
        ),
    ]

    dto = AutomaticEvaluationLoanRequestStartedDTO(
        basicWaging=3000,
        application=app,
        loanType=loan_type,
        minimalLoanDTOS=minimal_loans,
    )

    assert isinstance(dto, AutomaticEvaluationLoanRequestStartedDTO)
    assert dto.basicWaging == 3000
    assert dto.application is app
    assert dto.loanType is loan_type
    assert len(dto.minimalLoanDTOS) == 2
    assert all(isinstance(m, MinimalLoanDTO) for m in dto.minimalLoanDTOS)
