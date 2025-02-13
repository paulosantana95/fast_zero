import asyncio

from temporalio.client import Client
from temporalio.worker import Worker


async def main() -> None:
    client: Client = await Client.connect(
        'localhost:7233', namespace='default'
    )

    worker: Worker = Worker(
        client,
        task_queue='say_hello',
        workflows=['say_hello_workflow'],
        activities=['say_hello_activity'],
    )

    await worker.run()


asyncio.run(main())
