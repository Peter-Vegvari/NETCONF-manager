from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

# uv run fastapi dev src/netconf_manager/main.py
app = FastAPI()
host = "localhost"
port = "80"
username = "admin"
password = "admin"

app = FastAPI()
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = f"http://{host}:{port}/restconf"


@app.get("/restconf/{path:path}")
def proxy_get(path: str):
    url = f"{DEVICE}/{path}"

    r = requests.get(
        url,
        headers={"Accept": "application/yang-data+json"},
        auth=(username, password),
        verify=False,
        timeout=10,
    )

    if not r.ok:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()
