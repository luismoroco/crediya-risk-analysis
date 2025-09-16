from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Application:
    applicationId: int
    amount: int
    deadline: int
    email: str
    applicationStatusId: int
    loanTypeId: int


@dataclass
class LoanType:
    loanTypeId: int
    name: str
    maximumAmount: int
    minimumAmount: int
    interestRate: Decimal
    automaticValidation: bool


@dataclass
class MinimalLoanDTO:
    loanId: int
    amount: int
    deadline: int
    interestRate: Decimal


@dataclass
class AutomaticEvaluationLoanRequestStartedDTO:
    basicWaging: int
    application: Application
    loanType: LoanType
    minimalLoanDTOS: List[MinimalLoanDTO]
