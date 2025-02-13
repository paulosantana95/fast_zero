from uuid import uuid4

from fastapi import FastAPI, Query
from temporalio.client import Client

app = FastAPI()


@app.get('/')
async def read_root(name: str = Query(default=None)):
    client: Client = await Client.connect('localhost:7233')

    result = await client.execute_workflow(
        workflow='GreetingWorkflow',
        arg=name,
        id=str(uuid4()),
        task_queue='say_hello',
    )

    return {'name: ': name, 'result: ': result}
