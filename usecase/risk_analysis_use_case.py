from decimal import Decimal
from typing import ClassVar

from domain import ApplicationStatus
from usecase.dto import AutomaticEvaluationLoanRequestStartedDTO


class RiskAnalysisUseCase:

    __WAGING_PERCENTAGE: ClassVar[Decimal] = Decimal("0.35")
    __MAXIMUM_SALARIES: ClassVar[int] = 5

    def __init__(self):
        pass

    def evaluate_loan_request(
        self, dto: AutomaticEvaluationLoanRequestStartedDTO
    ) -> ApplicationStatus:
        max_debt_capacity = Decimal(dto.basicWaging) * self.__WAGING_PERCENTAGE

        current_debt_amount = Decimal(0)
        for loan in dto.minimalLoanDTOS:
            current_debt_amount += self._get_monthly_installment(
                p=Decimal(loan.amount), i=loan.interestRate, n=loan.deadline
            )

        new_installment = self._get_monthly_installment(
            p=Decimal(dto.application.amount),
            i=dto.loanType.interestRate,
            n=dto.application.deadline,
        )

        debt_capacity = max_debt_capacity - current_debt_amount
        if new_installment <= debt_capacity:
            if dto.application.amount > dto.basicWaging * self.__MAXIMUM_SALARIES:
                return ApplicationStatus.MANUAL_REVIEW

            return ApplicationStatus.APPROVED

        return ApplicationStatus.REJECTED

    @staticmethod
    def _get_monthly_installment(p: Decimal, i: Decimal, n: int) -> Decimal:
        if i == 0:
            return p / n

        numerator = p * i
        denominator = Decimal(1) - (Decimal(1) + i) ** (-n)
        return numerator / denominator
