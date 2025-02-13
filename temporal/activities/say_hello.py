from temporalio import activity


@activity.defn
async def say_hello(name: str) -> str:
    return f'Hello, {name}!'


@activity.defn
async def say_goodbye(name: str) -> str:
    return f'Goodbye, {name}!'
