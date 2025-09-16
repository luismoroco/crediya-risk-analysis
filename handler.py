import json
import logging

from usecase import RiskAnalysisUseCase
from usecase.dto import AutomaticEvaluationLoanRequestStartedDTO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


def lambda_handler(event, context):
    use_case = RiskAnalysisUseCase()

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

        use_case.evaluate_loan_request(
            AutomaticEvaluationLoanRequestStartedDTO.from_dict(body)
        )

    return {"statusCode": 200, "body": json.dumps("Event processed")}
