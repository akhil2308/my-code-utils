import asyncio

from temporalio.client import Client

from workflows import GreetingWorkflow
from worker import TASK_QUEUE, TEMPORAL_ADDRESS


async def main():
    client = await Client.connect(TEMPORAL_ADDRESS, namespace="default")

    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "World",
        id="greeting-workflow-id",
        task_queue=TASK_QUEUE,
    )

    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
