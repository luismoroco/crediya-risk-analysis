import json
import logging

from usecase import RiskAnalysisUseCase
from usecase.dto import AutomaticEvaluationLoanRequestStartedDTO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


def lambda_handler(event=None, context=None):
    fake_body = json.dumps(
        {
            "basicWaging": 5000,
            "application": {
                "applicationId": 1,
                "amount": 100000,
                "deadline": 12,
                "email": "usuario@example.com",
                "applicationStatusId": 1,
                "loanTypeId": 1,
            },
            "loanType": {
                "loanTypeId": 1,
                "name": "Personal Loan",
                "maximumAmount": 20000,
                "minimumAmount": 500,
                "interestRate": 0.02,
                "automaticValidation": True,
            },
            "minimalLoanDTOS": [
                {"loanId": 101, "amount": 2000, "deadline": 6, "interestRate": 0.01},
                {
                    "loanId": 102,
                    "amount": 3000,
                    "deadline": 12,
                    "interestRate": 0.015,
                },
            ],
        }
    )

    event = {"Records": [{"body": fake_body}]}

    records = event.get("Records", [])
    if not records:
        return {"statusCode": 400, "body": json.dumps("No Records found in the event")}

    for record in records:
        body_str = record.get("body", "")
        if not body_str:
            print("No body found in this record")
            continue

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            print("Body is not valid JSON:", body_str)
            continue

        use_case = RiskAnalysisUseCase()
        result = use_case.evaluate_loan_request(
            AutomaticEvaluationLoanRequestStartedDTO.from_dict(body)
        )

        print("Evaluación automática:", result.name)

    return {"statusCode": 200, "body": json.dumps("Event processed")}


if __name__ == "__main__":
    lambda_handler()
