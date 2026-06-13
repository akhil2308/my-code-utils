import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import say_hello
from workflows import GreetingWorkflow

TEMPORAL_ADDRESS = "localhost:7233"
TASK_QUEUE = "greeting-task-queue"


async def main():
    client = await Client.connect(TEMPORAL_ADDRESS, namespace="default")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[GreetingWorkflow],
        activities=[say_hello],
    )

    print(f"Worker started, polling task queue '{TASK_QUEUE}'...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
