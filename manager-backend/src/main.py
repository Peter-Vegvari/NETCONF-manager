from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import Connection

# uv run fastapi dev manager_backend/main.py
app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection: Connection | None = None


@app.post("/connect")
async def connect(new_connection: Connection):
    global connection
    connection = new_connection
    connection.download_schemas()


@app.post("/netconf/get")
async def get():
    pass


@app.post("/netconf/get-config")
async def get_config():
    pass


@app.post("/netconf/get-schema")
async def get_schema():
    pass


@app.post("/netconf/dispatch")
async def dispatch():
    pass


@app.post("/netconf/edit-config")
async def edit_config():
    pass


@app.post("/netconf/copy-config")
async def copy_config():
    pass


@app.post("/netconf/validate")
async def validate():
    pass


@app.post("/netconf/commit")
async def commit():
    pass


@app.post("/netconf/discard-changes")
async def discard_changes():
    pass


@app.post("/netconf/cancel-commit")
async def cancel_commit():
    pass


@app.post("/netconf/delete-config")
async def delete_config():
    pass


@app.post("/netconf/lock")
async def lock():
    pass


@app.post("/netconf/unlock")
async def unlock():
    pass


@app.post("/netconf/create-subscription")
async def create_subscription():
    pass


@app.post("/netconf/close-session")
async def close_session():
    pass


@app.post("/netconf/kill-session")
async def kill_session():
    pass


@app.post("/netconf/poweroff-machine")
async def poweroff_machine():
    pass


@app.post("/netconf/reboot-machine")
async def reboot_machine():
    pass


@app.post("/netconf/rpc")
async def rpc():
    pass
