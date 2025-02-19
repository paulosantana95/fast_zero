import asyncio
from datetime import timedelta

from temporalio.client import Client
from temporalio.worker import Worker

from temporal.activities.say_hello import say_hello
from temporal.activities.sync_payments_activity import sync_payments_activity
from temporal.workflows.greeting_workflow import GreetingWorkflow
from temporal.workflows.sync_payments_workflow import SyncPaymentsWorkflow


async def main() -> None:
    client: Client = await Client.connect('localhost:7233')

    worker: Worker = Worker(
        client,
        task_queue='default-task-queue',
        workflows=[GreetingWorkflow, SyncPaymentsWorkflow],
        activities=[say_hello, sync_payments_activity],
    )

    await worker.run()


asyncio.run(main())
