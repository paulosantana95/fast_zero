from temporalio import activity


@activity.defn
async def sync_payments_activity(payments: list) -> str:
    return f'Starting sync payments workflow!: {payments}'
