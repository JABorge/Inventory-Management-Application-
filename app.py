from typing import SupportsComplex
from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import (supplier_pydantic, supplier_pydanticIn, Supplier)

app = FastAPI()

@app.get('/')
def index():
    return {"Msg": "go to /docs for the API documentation"}

@app.post('/supplier')
async def add_supplier(supplier_info: supplier_pydanticIn):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "ok", "data": response}

@app.get('/supplier')
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}

@app.get('/supplier/{supplier_id}')
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "ok", "data":response}

@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    update_info = await Supplier.get(exclude_unset=True)
    supplier.name = update_info['name']
    supplier.company = update_info['company']
    supplier.phone = update_info['phone']
    supplier.email = update_info['email']
    await supplier.save()
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}

@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id: int):
    #removed await from the line below in the front of supplier 
    Supplier.get(id=supplier_id).delete()
    return {"status": "ok"}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
