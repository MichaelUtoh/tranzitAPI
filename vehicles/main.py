from fastapi import FastAPI

from vehicles.schemas import Vehicle


app = FastAPI()


@app.post('/vehicles/add')
def add_vehicle(vehicle: Vehicle):
    return vehicle

