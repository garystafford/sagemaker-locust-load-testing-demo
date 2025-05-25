import json
import logging
import time

import boto3
from locust.contrib.fasthttp import FastHttpUser

from locust import task, events

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

region = "us-east-1"
content_type = "application/json"
endpoint_name = "<YOUR_SAGEMAKER_ENDPOINT_NAME>"


class BotoClient:
    def __init__(self, host):
        self.sagemaker_client = boto3.client("sagemaker-runtime", region_name=region)

    def send(self):

        request_meta = {
            "request_type": "InvokeEndpoint",
            "name": "SageMaker",
            "start_time": time.time(),
            "response_length": 0,
            "response": None,
            "context": {},
            "exception": None,
        }
        start_perf_counter = time.perf_counter()

        try:
            messages = [
                {
                    "role": "system",
                    "content": "Speak in a Medieval British style.",
                },
                {
                    "role": "user",
                    "content": "Name at least 200 popular places to visit in England, with descriptions.",
                },
            ]

            body = {
                "messages": messages,
                "repetition_penalty": 1.0,
                "temperature": 0.5,
                "max_tokens": 128,
            }

            response = self.sagemaker_client.invoke_endpoint(
                EndpointName=endpoint_name,
                Body=json.dumps(body),
                ContentType="application/json",
            )
            response_body = json.loads(response["Body"].read().decode("utf8"))
            content = response_body["choices"][0]["message"]["content"]
            logger.debug(content)
        except Exception as e:
            logger.error(e)
            request_meta["exception"] = e

        end_perf_counter = time.perf_counter()
        request_meta["response_time"] = (end_perf_counter - start_perf_counter) * 1000

        logger.debug(start_perf_counter)
        logger.debug(end_perf_counter)
        logger.debug(request_meta["response_time"])

        events.request.fire(**request_meta)


class BotoUser(FastHttpUser):
    abstract = True

    def __init__(self, env):
        super().__init__(env)
        self.client = BotoClient(self.host)


class MyUser(BotoUser):
    @task
    def send_request(self):
        self.client.send()
