import logging
from decimal import ROUND_HALF_UP, Decimal
from typing import ClassVar

from domain import ApplicationStatus
from domain.gateway import EventPublisher
from domain.gateway.dto import LoanRequestEvaluatedEvent
from infrastructure.sqs_event_publisher import SQSEventPublisher
from usecase.dto import AutomaticEvaluationLoanRequestStartedDTO

logger = logging.getLogger(__name__)


class RiskAnalysisUseCase:

    __WAGING_PERCENTAGE: ClassVar[Decimal] = Decimal("0.35")
    __MAXIMUM_SALARIES: ClassVar[int] = 5

    event_publisher: EventPublisher

    def __init__(self):
        self.event_publisher = SQSEventPublisher()

    def evaluate_loan_request(
        self, dto: AutomaticEvaluationLoanRequestStartedDTO
    ) -> None:
        logger.info(
            "Starting loan evaluation "
            "[basicWaging=%s][applicationAmount=%s][deadline=%s]",
            dto.basicWaging,
            dto.application.amount,
            dto.application.deadline,
        )

        max_debt_capacity = Decimal(dto.basicWaging) * self.__WAGING_PERCENTAGE
        logger.info(
            "Calculated max debt capacity [maxDebtCapacity=%s]", max_debt_capacity
        )

        current_debt_amount = Decimal(0)
        for loan in dto.minimalLoanDTOS:
            installment = self._get_monthly_installment(
                p=Decimal(loan.amount), i=loan.interestRate, n=loan.deadline
            )
            current_debt_amount += installment
            logger.info(
                "Processed existing loan "
                "[loanId=%s][amount=%s][deadline=%s][interestRate=%s][installment=%s]",
                loan.loanId,
                loan.amount,
                loan.deadline,
                loan.interestRate,
                installment,
            )

        logger.info(
            "Total current debt amount [currentDebtAmount=%s]", current_debt_amount
        )

        new_installment = self._get_monthly_installment(
            p=Decimal(dto.application.amount),
            i=dto.loanType.interestRate,
            n=dto.application.deadline,
        )
        logger.info("Calculated new installment [newInstallment=%s]", new_installment)

        debt_capacity = max_debt_capacity - current_debt_amount
        logger.info("Available debt capacity [debtCapacity=%s]", debt_capacity)

        application_status: ApplicationStatus
        if new_installment <= debt_capacity:
            if dto.application.amount > dto.basicWaging * self.__MAXIMUM_SALARIES:
                logger.info(
                    "Loan requires manual review [reason=amountExceedsMaximumSalaries]"
                )
                application_status = ApplicationStatus.MANUAL_REVIEW
            else:
                logger.info("Loan approved [status=APPROVED]")
                application_status = ApplicationStatus.APPROVED
        else:
            logger.info(
                "Loan rejected [status=REJECTED][reason=insufficientDebtCapacity]"
            )
            application_status = ApplicationStatus.REJECTED

        event = LoanRequestEvaluatedEvent()
        event.applicationId = dto.application.applicationId
        event.applicationStatus = application_status
        self.event_publisher.notify_loan_request_evaluated(event=event)

    @staticmethod
    def _get_monthly_installment(p: Decimal, i: Decimal, n: int) -> Decimal:
        if i == 0:
            result = p / n
        else:
            numerator = p * i
            denominator = Decimal(1) - (Decimal(1) + i) ** (-n)
            result = numerator / denominator

        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
