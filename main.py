from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def home():
    return {'detail': 'Success'}
