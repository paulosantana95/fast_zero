import os
from datetime import date
from enum import Enum
from uuid import uuid4

import requests
from dotenv import load_dotenv
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel
from temporalio.client import Client

from temporal.schedulers.sync_payments_scheduler import sync_payments_scheduler

load_dotenv()

app = FastAPI()


class BillingType(str, Enum):
    BOLETO = 'BOLETO'


class PaymentPayload(BaseModel):
    customer: str
    billingType: BillingType
    value: float
    dueDate: date
    description: str

    def to_json(self):
        return {
            'customer': self.customer,
            'billingType': self.billingType,
            'value': self.value,
            'dueDate': self.dueDate.isoformat(),
            'description': self.description,
        }


@app.get('/')
async def read_root(name: str = Query(default=None)):
    client: Client = await Client.connect('localhost:7233')

    result = await client.execute_workflow(
        workflow='GreetingWorkflow',
        arg=name,
        id=str(uuid4()),
        task_queue='default-task-queue',
    )

    return {'name: ': name, 'result: ': result}


def asaas_api():
    s = requests.Session()
    s.headers.update({
        # 'accept': 'application/json',
        # 'content-type': 'application/json',
        'access_token': os.getenv('ASAAS_API_KEY'),
    })
    s.base_url = os.getenv('ASAAS_API_URL')
    return s


async def get_asaas_customers():
    s = asaas_api()
    response = s.get(f'{s.base_url}/customers')

    return response.json()


async def get_asaas_payments():
    s = asaas_api()
    response = s.get(f'{s.base_url}/payments')

    return response.json()


async def post_asaas_create_payments(paylod: PaymentPayload):
    s = asaas_api()
    response = s.post(f'{s.base_url}/payments', json=paylod.to_json())

    return response.json()


@app.get('/customers')
async def get_clients():
    return await get_asaas_customers()


@app.get('/payments')
async def get_payments():
    payments = await get_asaas_payments()
    await sync_payments_scheduler(payments['data'])

    return payments


@app.post('/payments')
async def create_payments(payload: PaymentPayload = Body(...)):
    return await post_asaas_create_payments(payload)
