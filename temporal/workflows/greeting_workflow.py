from datetime import timedelta
from typing import List

from temporalio import workflow

from temporal.activities.say_hello import say_goodbye, say_hello


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self.name = None

    @workflow.run
    async def run(self) -> List[str]:
        await workflow.wait_condition(lambda: self.name is not None)

        return await workflow.execute_activity(
            activity=say_hello,
            arg=self.name,
            start_to_close_timeout=timedelta(seconds=10),
        )

    @workflow.signal
    async def set_name(self, name: str) -> None:
        self.name = name
