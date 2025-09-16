import json
import logging
from typing import Any, ClassVar, Dict

import boto3
from botocore.client import BaseClient

from domain.gateway import EventPublisher
from domain.gateway.dto import LoanRequestEvaluatedEvent

logger = logging.getLogger(__name__)


class SQSEventPublisher(EventPublisher):

    __QUEUE_URL: ClassVar[str] = ""

    client: BaseClient

    def __init__(self):
        self.client = boto3.client("sqs", region_name="us-east-1")

    def notify_loan_request_evaluated(self, event: LoanRequestEvaluatedEvent) -> None:
        return self._send(
            body={
                "applicationId": event.applicationId,
                "applicationStatus": event.applicationStatus.name,
            }
        )

    def _send(self, body: Dict[str, Any]) -> None:
        logger.info("Sending event [sqsUrl=%s]", self.__QUEUE_URL)

        self.client.send_message(
            QueueUrl=self.__QUEUE_URL, MessageBody=json.dumps(body)
        )
