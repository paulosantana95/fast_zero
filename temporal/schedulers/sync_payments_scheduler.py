from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
)

from temporal.workflows.sync_payments_workflow import SyncPaymentsWorkflow


async def sync_payments_scheduler(payments: list) -> None:
    client: Client = await Client.connect('localhost:7233')

    await client.create_schedule(
        id=f'sync_payments_scheduler_id:{payments[0]["id"]}',
        schedule=Schedule(
            action=ScheduleActionStartWorkflow(
                SyncPaymentsWorkflow.run,
                args=[payments],
                id=f'sync_payments_scheduler_id:{payments[0]["id"]}',
                task_queue='default-task-queue',
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(every=timedelta(seconds=30))],
            ),
            state=ScheduleState(note='Sync payments scheduler'),
        ),
    )
