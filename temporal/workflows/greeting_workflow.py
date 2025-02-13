from datetime import timedelta

from temporalio import workflow

from temporal.activities.say_hello import say_hello


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_activity(
            activity=say_hello,
            arg=name,
            start_to_close_timeout=timedelta(seconds=10),
        )

        return result
