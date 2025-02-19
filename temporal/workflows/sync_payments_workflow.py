from datetime import timedelta

from temporalio import workflow

from temporal.activities.sync_payments_activity import sync_payments_activity


@workflow.defn
class SyncPaymentsWorkflow:
    @workflow.run
    async def run(self, payments: list) -> None:
        return await workflow.execute_activity(
            activity=sync_payments_activity,
            args=[payments],
            start_to_close_timeout=timedelta(seconds=10),
        )
