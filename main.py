from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from core.routers import accounts, auth, manifests, vehicles

origins = [
    "http://127.0.0.1:1234",
    "http://localhost:1234",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tranzit")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(vehicles.router)
app.include_router(manifests.router)
