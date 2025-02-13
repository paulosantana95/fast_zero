import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from temporal.activities.say_hello import say_hello
from temporal.workflows.greeting_workflow import GreetingWorkflow


async def main() -> None:
    client: Client = await Client.connect(
        'localhost:7233', namespace='default'
    )

    worker: Worker = Worker(
        client,
        task_queue='say_hello',
        workflows=[GreetingWorkflow],
        activities=[say_hello],
    )

    await worker.run()


asyncio.run(main())
