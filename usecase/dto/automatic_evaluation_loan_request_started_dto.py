from dataclasses import dataclass
from decimal import Decimal
from typing import List

from helper import BaseModel


@dataclass
class Application(BaseModel):
    applicationId: int
    amount: int
    deadline: int
    email: str
    applicationStatusId: int
    loanTypeId: int


@dataclass
class LoanType(BaseModel):
    loanTypeId: int
    name: str
    maximumAmount: int
    minimumAmount: int
    interestRate: Decimal
    automaticValidation: bool


@dataclass
class MinimalLoanDTO(BaseModel):
    loanId: int
    amount: int
    deadline: int
    interestRate: Decimal


@dataclass
class AutomaticEvaluationLoanRequestStartedDTO(BaseModel):
    basicWaging: int
    application: Application
    loanType: LoanType
    minimalLoanDTOS: List[MinimalLoanDTO]
